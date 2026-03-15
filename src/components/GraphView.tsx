"use client";

import { GraphPoint, GraphEdge, GraphSolveResult } from "@/lib/types";

interface Props {
  points: GraphPoint[];
  edges: GraphEdge[];
  result?: GraphSolveResult;
}

const W = 600, H = 400, PAD = 50;

function sx(x: number, minX: number, maxX: number) {
  return maxX === minX ? W / 2 : PAD + ((x - minX) / (maxX - minX)) * (W - 2 * PAD);
}

function sy(y: number, minY: number, maxY: number) {
  return maxY === minY ? H / 2 : PAD + ((maxY - y) / (maxY - minY)) * (H - 2 * PAD);
}

function inPath(from: string, to: string, path: string[]) {
  for (let i = 0; i < path.length - 1; i++) {
    if ((path[i] === from && path[i + 1] === to) || (path[i] === to && path[i + 1] === from)) return true;
  }
  return false;
}

export default function GraphView({ points, edges, result }: Props) {
  if (!points.length) return <div className="h-64 flex items-center justify-center text-gray-400">読み込み中...</div>;

  const xs = points.map(p => p.x), ys = points.map(p => p.y);
  const [minX, maxX, minY, maxY] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
  const pm = new Map(points.map(p => [p.name, p]));
  const sp = result?.shortest.path || [];
  const lp = result?.longest.path || [];

  return (
    <div className="rounded border bg-white p-2">
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" style={{ maxHeight: 400 }}>
        {edges.map(e => {
          const a = pm.get(e.from), b = pm.get(e.to);
          if (!a || !b) return null;
          const x1 = sx(a.x, minX, maxX), y1 = sy(a.y, minY, maxY);
          const x2 = sx(b.x, minX, maxX), y2 = sy(b.y, minY, maxY);
          const inS = inPath(e.from, e.to, sp), inL = inPath(e.from, e.to, lp);
          let stroke = "#d1d5db", sw = 1.5, op = result ? 0.25 : 1;
          if (inS && inL) { stroke = "#8b5cf6"; sw = 3; op = 1; }
          else if (inS) { stroke = "#3b82f6"; sw = 3; op = 1; }
          else if (inL) { stroke = "#ef4444"; sw = 3; op = 1; }
          return (
            <g key={`${e.from}-${e.to}`}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={stroke} strokeWidth={sw} opacity={op} />
              <text x={(x1+x2)/2} y={(y1+y2)/2-5} textAnchor="middle" fontSize={9} fill="#9ca3af" opacity={op}>{e.distance}</text>
            </g>
          );
        })}
        {points.map(p => {
          const cx = sx(p.x, minX, maxX), cy = sy(p.y, minY, maxY);
          const isStart = sp[0] === p.name, isEnd = sp[sp.length-1] === p.name;
          let fill = "#6b7280", r = 8;
          if (result) {
            if (isStart) { fill = "#22c55e"; r = 12; }
            else if (isEnd) { fill = "#f97316"; r = 12; }
            else if (sp.includes(p.name) || lp.includes(p.name)) { fill = "#3b82f6"; r = 9; }
          }
          return (
            <g key={p.name}>
              <circle cx={cx} cy={cy} r={r} fill={fill} stroke="#fff" strokeWidth={2} />
              <text x={cx} y={cy - r - 4} textAnchor="middle" fontSize={12} fontWeight={isStart || isEnd ? "bold" : "normal"} fill="#1f2937">
                {p.name}
              </text>
            </g>
          );
        })}
      </svg>
      {result && (
        <div className="flex gap-4 mt-1 text-xs text-gray-500 justify-center">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-green-500 inline-block" /> 始点</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-orange-500 inline-block" /> 終点</span>
          <span className="flex items-center gap-1"><span className="w-4 h-0.5 bg-blue-500 inline-block" /> 最短</span>
          <span className="flex items-center gap-1"><span className="w-4 h-0.5 bg-red-500 inline-block" /> 最長</span>
          <span className="flex items-center gap-1"><span className="w-4 h-0.5 bg-purple-500 inline-block" /> 共通</span>
        </div>
      )}
    </div>
  );
}
