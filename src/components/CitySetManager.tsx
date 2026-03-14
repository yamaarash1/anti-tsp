"use client";

import { useState, useEffect } from "react";
import { CitySet, Location } from "@/lib/types";
import { listCitySets, saveCitySet, deleteCitySet } from "@/lib/api";

interface Props {
  locations: Location[] | null;
  onLoad: (locations: Location[]) => void;
}

export default function CitySetManager({ locations, onLoad }: Props) {
  const [sets, setSets] = useState<CitySet[]>([]);
  const [saveName, setSaveName] = useState("");
  const [loading, setLoading] = useState(false);

  const refresh = async () => {
    try {
      setSets(await listCitySets());
    } catch {
      // API未起動時は無視
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleSave = async () => {
    if (!saveName.trim() || !locations || locations.length < 3) return;
    setLoading(true);
    try {
      await saveCitySet(saveName.trim(), locations);
      setSaveName("");
      await refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "保存に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteCitySet(id);
      await refresh();
    } catch (e) {
      alert(e instanceof Error ? e.message : "削除に失敗しました");
    }
  };

  return (
    <div className="space-y-3">
      <h2 className="text-lg font-bold">都市セット</h2>

      {/* 保存 */}
      {locations && locations.length >= 3 && (
        <div className="flex gap-2">
          <input
            type="text"
            value={saveName}
            onChange={(e) => setSaveName(e.target.value)}
            placeholder="セット名"
            className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm"
          />
          <button
            onClick={handleSave}
            disabled={loading || !saveName.trim()}
            className="rounded bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700 disabled:opacity-50"
          >
            保存
          </button>
        </div>
      )}

      {/* 一覧 */}
      {sets.length > 0 && (
        <ul className="space-y-1">
          {sets.map((s) => (
            <li
              key={s.id}
              className="flex items-center justify-between rounded bg-gray-50 px-3 py-2 text-sm"
            >
              <button
                onClick={() => onLoad(s.locations)}
                className="text-left hover:text-blue-600"
              >
                {s.name}{" "}
                <span className="text-gray-400">
                  ({s.locations.length}都市)
                </span>
              </button>
              <button
                onClick={() => handleDelete(s.id)}
                className="text-red-400 hover:text-red-600"
              >
                削除
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
