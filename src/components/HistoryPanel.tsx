"use client";

import { useEffect, useState } from "react";
import { CalculationHistory, Location, SolveResult } from "@/lib/types";
import { getHistory } from "@/lib/api";

interface Props {
  userId: string;
  refreshKey: number;
  onLoadHistory: (locations: Location[], result: SolveResult) => void;
}

export default function HistoryPanel({ userId, refreshKey, onLoadHistory }: Props) {
  const [history, setHistory] = useState<CalculationHistory[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!userId) return;
    setLoading(true);
    getHistory(userId)
      .then(setHistory)
      .catch(() => setHistory([]))
      .finally(() => setLoading(false));
  }, [userId, refreshKey]);

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString("ja-JP", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-bold">計算履歴</h2>
      {loading && <p className="text-sm text-gray-400">読み込み中...</p>}
      {!loading && history.length === 0 && (
        <p className="text-sm text-gray-400">まだ計算履歴がありません</p>
      )}
      <ul className="space-y-1 max-h-64 overflow-y-auto">
        {history.map((h) => (
          <li
            key={h._id}
            onClick={() => onLoadHistory(h.locations, h.result)}
            className="flex items-center justify-between rounded bg-gray-50 px-3 py-2 text-sm cursor-pointer hover:bg-blue-50"
          >
            <div>
              <span className="font-medium">{h.city_count}都市</span>
              <span className="ml-2 text-xs text-gray-400">{formatDate(h.calculated_at)}</span>
            </div>
            <div className="flex gap-3 text-xs">
              <span className="text-red-500">{h.result.longest.distance_km} km</span>
              <span className="text-blue-500">{h.result.shortest.distance_km} km</span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
