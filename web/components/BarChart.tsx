"use client";

import { useState } from "react";

type Datum = { label: string; value: number };

/** One-series bar chart: single sequential hue, thin bars, rounded data-end, hairline grid, hover tooltip, table fallback. */
export default function BarChart({ data, orientation, compactLabels }: { data: Datum[]; orientation: "horizontal" | "vertical"; compactLabels?: boolean }) {
  const [hover, setHover] = useState<{ i: number; x: number; y: number } | null>(null);
  if (!data.length) return <p className="muted">No data.</p>;
  const max = Math.max(...data.map((d) => d.value), 1);
  const W = 520;
  const fmt = (n: number) => n.toLocaleString("en-US");

  if (orientation === "horizontal") {
    const row = 28, left = 96, right = 56, H = data.length * row + 8;
    const x = (v: number) => left + ((W - left - right) * v) / max;
    return (
      <div className="chart" style={{ position: "relative" }}>
        <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Complaints by topic">
          {[0.25, 0.5, 0.75, 1].map((t) => <line key={t} className="grid" x1={x(max * t)} x2={x(max * t)} y1={0} y2={H - 8} />)}
          {data.map((d, i) => {
            const y = i * row + 4, h = 20, w = Math.max(x(d.value) - left, 0);
            return (
              <g key={d.label} onMouseEnter={(e) => setHover({ i, x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY })}
                 onMouseMove={(e) => setHover({ i, x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY })} onMouseLeave={() => setHover(null)}>
                <rect x={left - 96} y={y - 4} width={W} height={row} fill="transparent" />
                <text x={left - 8} y={y + h / 2 + 4} textAnchor="end">{d.label}</text>
                <path className="bar" d={roundedRight(left, y, w, h, 4)} />
                <text className="value" x={left + w + 6} y={y + h / 2 + 4}>{fmt(d.value)}</text>
              </g>
            );
          })}
        </svg>
        {hover && <div className="tooltip" style={{ left: hover.x + 12, top: hover.y + 12 }}>{data[hover.i].label}: {fmt(data[hover.i].value)}</div>}
        <details><summary className="muted">Table view</summary><table><tbody>{data.map((d) => <tr key={d.label}><td>{d.label}</td><td className="num">{fmt(d.value)}</td></tr>)}</tbody></table></details>
      </div>
    );
  }

  const H = 220, bottom = 36, top = 12, left = 44;
  const slot = (W - left - 8) / data.length;
  const bw = Math.min(24, slot - 2);
  const y = (v: number) => top + (H - top - bottom) * (1 - v / max);
  const peak = data.reduce((m, d, i) => (d.value > data[m].value ? i : m), 0);
  return (
    <div className="chart" style={{ position: "relative" }}>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Complaints per month">
        {[0.5, 1].map((t) => (
          <g key={t}><line className="grid" x1={left} x2={W - 8} y1={y(max * t)} y2={y(max * t)} />
            <text x={left - 6} y={y(max * t) + 4} textAnchor="end">{compact(max * t)}</text></g>
        ))}
        <line className="grid" x1={left} x2={W - 8} y1={y(0)} y2={y(0)} />
        {data.map((d, i) => {
          const bx = left + i * slot + (slot - bw) / 2, by = y(d.value), bh = y(0) - by;
          const showLabel = !compactLabels || data.length <= 8 || i % Math.ceil(data.length / 8) === 0;
          return (
            <g key={d.label} onMouseEnter={(e) => setHover({ i, x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY })}
               onMouseMove={(e) => setHover({ i, x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY })} onMouseLeave={() => setHover(null)}>
              <rect x={left + i * slot} y={top} width={slot} height={H - top} fill="transparent" />
              <path className="bar" d={roundedTop(bx, by, bw, bh, 4)} />
              {i === peak && <text className="value" x={bx + bw / 2} y={by - 6} textAnchor="middle">{fmt(d.value)}</text>}
              {showLabel && <text x={bx + bw / 2} y={H - bottom + 16} textAnchor="middle">{d.label.slice(2)}</text>}
            </g>
          );
        })}
      </svg>
      {hover && <div className="tooltip" style={{ left: hover.x + 12, top: hover.y + 12 }}>{data[hover.i].label}: {fmt(data[hover.i].value)}</div>}
      <details><summary className="muted">Table view</summary><table><tbody>{data.map((d) => <tr key={d.label}><td>{d.label}</td><td className="num">{fmt(d.value)}</td></tr>)}</tbody></table></details>
    </div>
  );
}

function compact(n: number) {
  return n >= 1000 ? `${Math.round(n / 100) / 10}K` : String(Math.round(n));
}
function roundedRight(x: number, y: number, w: number, h: number, r: number) {
  const rr = Math.min(r, w, h / 2);
  return `M${x},${y} H${x + w - rr} Q${x + w},${y} ${x + w},${y + rr} V${y + h - rr} Q${x + w},${y + h} ${x + w - rr},${y + h} H${x} Z`;
}
function roundedTop(x: number, y: number, w: number, h: number, r: number) {
  const rr = Math.min(r, h, w / 2);
  return `M${x},${y + h} V${y + rr} Q${x},${y} ${x + rr},${y} H${x + w - rr} Q${x + w},${y} ${x + w},${y + rr} V${y + h} Z`;
}
