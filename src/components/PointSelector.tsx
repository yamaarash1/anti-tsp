"use client";

import { useEffect, useState } from "react";
import { GraphPoint } from "@/lib/types";
import { fetchGraphPoints } from "@/lib/api";

interface Props {
  onSolve: (start: string, end: string) => void;
  loading: boolean;
}

export default function PointSelector({ onSolve, loading }: Props) {
  const [points, setPoints] = useState<GraphPoint[]>([]);
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");

  useEffect(() => {
    fetchGraphPoints().then((pts) => {
      setPoints(pts);
      if (pts.length >= 2) {
        setStart(pts[0].name);
        setEnd(pts[pts.length - 1].name);
      }
    }).catch(() => {});
  }, []);

  const canSolve = start && end && start !== end && !loading;

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-bold">地点選択</h2>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">始点</label>
        <select
          value={start}
          onChange={(e) => setStart(e.target.value)}
          className="w-full rounded border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">選択してください</option>
          {points.map((p) => (
            <option key={p.name} value={p.name}>
              {p.name} ({p.label})
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">終点</label>
        <select
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          className="w-full rounded border border-gray-300 px-3 py-2 text-sm"
        >
          <option value="">選択してください</option>
          {points.map((p) => (
            <option key={p.name} value={p.name}>
              {p.name} ({p.label})
            </option>
          ))}
        </select>
      </div>
      {start === end && start !== "" && (
        <p className="text-sm text-orange-500">始点と終点は異なるポイントを選んでください</p>
      )}
      <button
        onClick={() => onSolve(start, end)}
        disabled={!canSolve}
        className="w-full rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "計算中..." : "経路計算"}
      </button>
    </div>
  );
}
