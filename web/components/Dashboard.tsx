"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import BarChart from "./BarChart";
import type { Issue, RecordRow } from "@/lib/data";

type Overview = { source: string; run: any; aggregates: any };
type IssueDetail = { issue: Issue; reviews: RecordRow[]; member_count: number };

const fmt = (n: number | null | undefined) => (n == null ? "–" : n.toLocaleString("en-US"));
const pct = (x: number | null | undefined) => (x == null ? "–" : `${(x * 100).toFixed(1)}%`);

export default function Dashboard() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [issues, setIssues] = useState<Issue[]>([]);
  const [memo, setMemo] = useState<any>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [detail, setDetail] = useState<IssueDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async (url: string) => {
      const r = await fetch(url, { cache: "no-store" });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || r.statusText);
      return j;
    };
    Promise.all([load("/api/overview"), load("/api/issues"), load("/api/memo")])
      .then(([o, i, m]) => {
        setOverview(o);
        setIssues(i.issues);
        setMemo(m);
        if (i.issues.length) setSelected(i.issues[0].issue_id);
      })
      .catch((e) => setError(String(e.message || e)));
  }, []);

  useEffect(() => {
    if (!selected) return;
    fetch(`/api/issues/${encodeURIComponent(selected)}`, { cache: "no-store" })
      .then((r) => r.json())
      .then(setDetail)
      .catch(() => setDetail(null));
  }, [selected]);

  if (error) return <div className="card">Backend error: {error}</div>;
  if (!overview) return <div className="card">Loading from the backend…</div>;

  const agg = overview.aggregates;
  const rec = agg.records ?? {};
  const complaints = agg.complaints ?? { total: 0, by_topic: {} };
  const topics = Object.entries(complaints.by_topic as Record<string, number>)
    .filter(([, v]) => v > 0)
    .sort((a, b) => b[1] - a[1])
    .map(([label, value]) => ({ label, value }));
  const months = Object.entries(agg.complaints_by_month_topic ?? {}).map(([month, byTopic]: [string, any]) => ({
    label: month,
    value: Object.values(byTopic as Record<string, number>).reduce((a, b) => a + b, 0),
  }));
  const recJson = memo?.memo?.json;

  return (
    <>
      <section className="tiles" aria-label="Overall metrics">
        <div className="tile"><div className="label">Reviews</div><div className="value">{fmt(rec.total)}</div>
          <div className="sub">run {overview.run.run_id}</div></div>
        <div className="tile"><div className="label">Classified</div><div className="value">{fmt(rec.completed)}</div>
          <div className="sub">{pct(rec.completed_fraction)} of rows</div></div>
        <div className="tile"><div className="label">Quarantined</div><div className="value">{fmt(rec.quarantined)}</div>
          <div className="sub">{Object.entries(rec.quarantine_reasons ?? {}).map(([k, v]) => `${k}: ${v}`).join(", ") || "none"}</div></div>
        <div className="tile"><div className="label">Complaints + cancellations</div><div className="value">{fmt(complaints.total)}</div>
          <div className="sub">{agg.issues} issues</div></div>
        <div className="tile"><div className="label">Needs review</div><div className="value">{pct(agg.needs_review?.fraction)}</div>
          <div className="sub">{fmt(agg.needs_review?.count)} flagged by the classifier</div></div>
        <div className="tile"><div className="label">Mean sentiment</div><div className="value">{agg.mean_sentiment ?? "–"}</div>
          <div className="sub">scale −1 to 1</div></div>
      </section>

      <div className="grid2">
        <section className="card">
          <h2 style={{ marginTop: 0 }}>Complaints by topic</h2>
          <BarChart data={topics} orientation="horizontal" />
        </section>
        <section className="card">
          <h2 style={{ marginTop: 0 }}>Complaints per month</h2>
          <BarChart data={months} orientation="vertical" compactLabels />
        </section>
      </div>

      <h2>Where should the next quarter go?</h2>
      <div className="table-wrap card">
        <table>
          <thead><tr><th>focus area</th><th>topics</th><th className="num">complaints</th><th className="num">severity sum</th>
            <th className="num">mean severity</th><th className="num">share</th></tr></thead>
          <tbody>
            {Object.entries(agg.focus_areas ?? {}).map(([area, f]: [string, any]) => (
              <tr key={area}><td><strong>{area}</strong></td><td>{f.topics.join(", ")}</td><td className="num">{fmt(f.complaint_count)}</td>
                <td className="num">{fmt(f.severity_sum)}</td><td className="num">{f.mean_severity ?? "–"}</td><td className="num">{pct(f.share_of_complaints)}</td></tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Issue ranking (baseline)</h2>
      <div className="grid2">
        <div className="table-wrap card">
          <table>
            <thead><tr><th>#</th><th>issue</th><th className="num">complaints</th><th className="num">mean sev.</th><th className="num">priority</th></tr></thead>
            <tbody>
              {issues.map((i) => (
                <tr key={i.issue_id} className={`clickable ${selected === i.issue_id ? "selected" : ""}`} onClick={() => setSelected(i.issue_id)}>
                  <td>{i.rank}</td>
                  <td>{i.name}<br /><span className="muted"><code>{i.issue_id}</code></span></td>
                  <td className="num">{fmt(i.complaint_count)}</td><td className="num">{i.mean_severity}</td><td className="num">{fmt(i.priority_score)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          {detail ? (
            <>
              <h3 style={{ marginTop: 0 }}>#{detail.issue.rank} {detail.issue.name}</h3>
              <p className="muted"><code>{detail.issue.issue_id}</code> · {fmt(detail.member_count)} member reviews · severity sum {fmt(detail.issue.severity_sum)}</p>
              {detail.issue.summary && <p>{detail.issue.summary}</p>}
              <h3>Evidence (verbatim quotes, traceable review IDs)</h3>
              <ul className="evidence">
                {(detail.reviews.length ? detail.reviews : []).slice(0, 12).map((r) => (
                  <li key={r.review_id}>
                    <span className={`pill sev${r.severity}`}>severity {r.severity}</span><span className="pill">{r.intent}</span>
                    <code>{r.review_id}</code>
                    <blockquote>{r.evidence_quote}</blockquote>
                  </li>
                ))}
                {!detail.reviews.length && detail.issue.examples.map((e) => (
                  <li key={e.review_id}><code>{e.review_id}</code><blockquote>{e.quote}</blockquote></li>
                ))}
              </ul>
            </>
          ) : <p className="muted">Select an issue to see its evidence.</p>}
        </div>
      </div>

      <h2>Recommendation (AI-generated from the saved aggregates)</h2>
      <div className="card memo">
        {memo?.memo?.status && (
          <p className="muted">
            Status <span className={`status ${memo.memo.status === "validated" ? "ok" : "warn"}`}>{memo.memo.status}</span>{" "}
            · model <code>{memo.memo.model}</code> · every issue-level number is substituted from <code>claims.csv</code> and shown with its claim ID.
            {recJson?.recommendation?.focus_area && <> · Focus area: <strong>{recJson.recommendation.focus_area}</strong></>}
          </p>
        )}
        {memo?.memo?.markdown ? <ReactMarkdown remarkPlugins={[remarkGfm]}>{memo.memo.markdown}</ReactMarkdown>
                              : <p className="muted">No memo published for this run.</p>}
      </div>
      <p className="muted">Data source: {overview.source}. Published {overview.run.published_at}.</p>
    </>
  );
}
