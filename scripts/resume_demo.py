#!/usr/bin/env python3
"""Interruption/resume demonstration (GRADING_CONTRACT.md): start a run, send it SIGINT (what Ctrl-C sends)
after two committed batches, show the saved checkpoint, run the same command again and show it resuming.

    asciinema rec --command "python scripts/resume_demo.py" runs/resume_demo/resume_demo.cast
    python scripts/resume_demo.py --selftest        # no API: checks SIGINT delivery only
"""
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "resume_demo"
CMD = [sys.executable, "-m", "pipeline.run", "--input", "data/raw/extracted/checkpoint_500.csv", "--out", str(OUT.relative_to(ROOT)),
       "--max-usd", "0.10", "--stages", "enrich"]


def say(line=""):
    print(line, flush=True)


def run_until(cmd, stop_after_lines: int, log: Path):
    """Run cmd, echo its output, send SIGINT once `stop_after_lines` progress lines were seen; return exit code."""
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    seen, sent = 0, False
    with open(log, "w", encoding="utf-8") as f:
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            f.write(line)
            if line.startswith("cold") and not sent:
                seen += 1
                if seen >= stop_after_lines:
                    say(f"^C   (SIGINT sent to pid {proc.pid} after {seen} committed batches)")
                    proc.send_signal(signal.SIGINT)
                    sent = True
    return proc.wait()


def main():
    if "--selftest" in sys.argv:
        code = run_until([sys.executable, "-u", "-c",
                          "import signal,time,sys\nsignal.signal(signal.SIGINT, signal.default_int_handler)\n"
                          "print('cold: fake batch 1', flush=True)\ntime.sleep(0.2)\nprint('cold: fake batch 2', flush=True)\n"
                          "try:\n    time.sleep(30)\nexcept KeyboardInterrupt:\n    print('interrupted cleanly'); sys.exit(0)"],
                         2, Path("/tmp/resume_selftest.log"))
        say(f"selftest exit code {code}")
        sys.exit(0 if code == 0 else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    say("$ " + " ".join(CMD[1:]).replace("-m pipeline.run", "python -m pipeline.run"))
    code = run_until(CMD, 2, OUT / "run1.log")
    say(f"(exit code {code})")
    before = json.loads((OUT / "checkpoints" / "checkpoint_before.json").read_text())
    say()
    say(f"$ cat {OUT.relative_to(ROOT)}/checkpoints/checkpoint_before.json | head  ->  {before['completed_count']} completed ids saved before the interruption, counts {before['counts']}")
    say("$ python -m pipeline.budget")
    subprocess.run([sys.executable, "-m", "pipeline.budget"], cwd=ROOT)
    say()
    say("$ (same command again)   # resumes: completed texts are never re-sent, new calls are phase=resume")
    time.sleep(1)
    subprocess.run(CMD, cwd=ROOT)
    after = json.loads((OUT / "checkpoints" / "checkpoint_after.json").read_text())
    sb, sa = set(before["completed_ids"]), set(after["completed_ids"])
    say()
    say(f"checkpoint_before: {len(sb)} ids   checkpoint_after: {len(sa)} ids   before < after: {sb < sa}")
    say(f"$ ls {OUT.relative_to(ROOT)}/checkpoints -> {sorted(p.name for p in (OUT / 'checkpoints').iterdir())}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
