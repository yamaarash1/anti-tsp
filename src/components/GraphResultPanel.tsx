"use client";

import { GraphSolveResult } from "@/lib/types";

interface Props {
  result: GraphSolveResult;
}

export default function GraphResultPanel({ result }: Props) {
  const { shortest, longest } = result;
  const diff = shortest.distance > 0
    ? ((longest.distance - shortest.distance) / shortest.distance * 100).toFixed(1)
    : "0";

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold">結果</h2>

      <div className="rounded border border-blue-300 bg-blue-50 p-3">
        <h3 className="font-semibold text-blue-700">
          最短経路 — {shortest.distance}
        </h3>
        <p className="mt-1 text-sm text-blue-600">{shortest.path.join(" → ")}</p>
        <p className="text-xs text-blue-400">{shortest.path.length} ノード</p>
      </div>

      <div className="rounded border border-red-300 bg-red-50 p-3">
        <h3 className="font-semibold text-red-700">
          最長経路 (ビットDP) — {longest.distance}
        </h3>
        <p className="mt-1 text-sm text-red-600">{longest.path.join(" → ")}</p>
        <p className="text-xs text-red-400">{longest.path.length} ノード</p>
      </div>

      <p className="text-sm text-gray-600">
        差分: <span className="font-bold">{diff}%</span>
        {" "}(最長は最短より {(longest.distance - shortest.distance).toFixed(1)} 長い)
      </p>
    </div>
  );
}
