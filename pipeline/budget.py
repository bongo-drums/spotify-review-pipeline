"""Persistent spend ledger that enforces the hard API spend cap.

Every paid call must `reserve()` its worst-case cost first and then `commit()`
the actual cost (or `release()` the reservation if nothing was billed). The
ledger lives in one shared DB (runs/ledger.sqlite by default), so pilots,
the full run and later stages all draw from the same cap across processes.

  spent        = sum of 'commit' rows (all runs)
  outstanding  = 'reserve' rows not yet closed by a 'commit' or 'release'
  reserve(x) fails when spent + outstanding + x > cap
"""
from __future__ import annotations

import argparse
import json
import os
import threading
import uuid
from dataclasses import dataclass

from . import config
from .state import SPEND_LEDGER_DDL, connect, utc_now


class BudgetExceeded(RuntimeError):
    """Raised when a reservation would push total spend past the cap."""


@dataclass(frozen=True)
class Reservation:
    reservation_id: str
    amount_usd: float
    run_id: str | None
    call_id: str | None


class SpendLedger:
    """DB-backed, thread-safe spend ledger. Cross-process safe via BEGIN IMMEDIATE."""

    def __init__(self, path=None, cap_usd: float | None = None, run_id: str | None = None):
        self.path = path or config.LEDGER_DB_PATH
        self.cap_usd = float(config.SPEND_CAP_USD if cap_usd is None else cap_usd)
        self.run_id = run_id
        self.conn = connect(self.path, schema=SPEND_LEDGER_DDL)
        self.lock = threading.Lock()

    def close(self) -> None:
        self.conn.close()

    # ---- totals -----------------------------------------------------------

    def _totals(self) -> tuple[float, float]:
        spent = self.conn.execute(
            "SELECT COALESCE(SUM(amount_usd),0) FROM spend_ledger WHERE kind='commit'"
        ).fetchone()[0]
        outstanding = self.conn.execute(
            """SELECT COALESCE(SUM(r.amount_usd),0) FROM spend_ledger r
               WHERE r.kind='reserve' AND NOT EXISTS (
                   SELECT 1 FROM spend_ledger x
                   WHERE x.reservation_id=r.reservation_id AND x.kind IN ('commit','release'))"""
        ).fetchone()[0]
        return float(spent), float(outstanding)

    def summary(self) -> dict:
        with self.lock:
            spent, outstanding = self._totals()
        return {
            "cap_usd": self.cap_usd,
            "committed_usd": round(spent, 6),
            "outstanding_reservations_usd": round(outstanding, 6),
            "remaining_usd": round(self.cap_usd - spent - outstanding, 6),
            "ledger_path": str(self.path),
        }

    # ---- reserve / commit / release --------------------------------------

    def _insert(self, kind: str, amount: float, reservation_id: str, call_id: str | None, run_id: str | None):
        self.conn.execute(
            "INSERT INTO spend_ledger(run_id,kind,amount_usd,call_id,reservation_id,created_at) "
            "VALUES (?,?,?,?,?,?)",
            (run_id, kind, amount, call_id, reservation_id, utc_now()),
        )

    def reserve(self, est_max_usd: float, call_id: str | None = None) -> Reservation:
        """Reserve a worst-case amount before dispatching a paid call."""
        if est_max_usd < 0:
            raise ValueError("reservation must be >= 0")
        with self.lock:
            self.conn.execute("BEGIN IMMEDIATE")  # serializes against other processes
            try:
                spent, outstanding = self._totals()
                if spent + outstanding + est_max_usd > self.cap_usd + 1e-9:
                    raise BudgetExceeded(
                        f"reserve ${est_max_usd:.4f} refused: committed ${spent:.4f} + "
                        f"outstanding ${outstanding:.4f} would exceed cap ${self.cap_usd:.2f}"
                    )
                res = Reservation(uuid.uuid4().hex, float(est_max_usd), self.run_id, call_id)
                self._insert("reserve", res.amount_usd, res.reservation_id, call_id, self.run_id)
                self.conn.execute("COMMIT")
                return res
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise

    def _close(self, kind: str, res: Reservation, amount: float, call_id: str | None) -> None:
        with self.lock:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                closed = self.conn.execute(
                    "SELECT 1 FROM spend_ledger WHERE reservation_id=? AND kind IN ('commit','release')",
                    (res.reservation_id,),
                ).fetchone()
                if closed:
                    raise ValueError(f"reservation {res.reservation_id} already closed")
                self._insert(kind, amount, res.reservation_id, call_id or res.call_id, res.run_id)
                self.conn.execute("COMMIT")
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise

    def commit(self, reservation: Reservation, actual_usd: float, call_id: str | None = None) -> None:
        """Record the actual billed cost and close the reservation.

        actual_usd may exceed the reservation (the money is already spent); it is
        recorded as-is so the ledger stays truthful, and later reserves see it.
        """
        self._close("commit", reservation, float(actual_usd), call_id)

    def release(self, reservation: Reservation) -> None:
        """Close a reservation with no spend (e.g. request never sent)."""
        self._close("release", reservation, 0.0, None)

    def release_orphans(self, run_id: str | None = None) -> int:
        """Release open reservations left by a crashed process. Call only when no other
        process is spending (e.g. at the start of a resume). Returns how many were released."""
        with self.lock:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                sql = """SELECT reservation_id, call_id, run_id FROM spend_ledger r
                         WHERE kind='reserve' AND NOT EXISTS (
                             SELECT 1 FROM spend_ledger x WHERE x.reservation_id=r.reservation_id
                             AND x.kind IN ('commit','release'))"""
                params: tuple = ()
                if run_id is not None:
                    sql += " AND run_id=?"
                    params = (run_id,)
                rows = self.conn.execute(sql, params).fetchall()
                for rid, call_id, rrun in rows:
                    self._insert("release", 0.0, rid, call_id, rrun)
                self.conn.execute("COMMIT")
                return len(rows)
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Show the shared spend ledger status.")
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    args = ap.parse_args(argv)
    ledger = SpendLedger(args.ledger)
    print(json.dumps(ledger.summary(), indent=2))
    ledger.close()


if __name__ == "__main__":
    main()
