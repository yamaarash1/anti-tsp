"use client";

import { useState } from "react";

interface Props {
  onSubmit: (addresses: string[]) => void;
  loading: boolean;
}

export default function AddressForm({ onSubmit, loading }: Props) {
  const [addresses, setAddresses] = useState<string[]>(["", "", ""]);

  const updateAddress = (index: number, value: string) => {
    const next = [...addresses];
    next[index] = value;
    setAddresses(next);
  };

  const addField = () => {
    if (addresses.length < 8) setAddresses([...addresses, ""]);
  };

  const removeField = (index: number) => {
    if (addresses.length > 3) {
      setAddresses(addresses.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const filled = addresses.filter((a) => a.trim());
    if (filled.length >= 3) onSubmit(filled);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <h2 className="text-lg font-bold">住所入力</h2>
      {addresses.map((addr, i) => (
        <div key={i} className="flex gap-2">
          <input
            type="text"
            value={addr}
            onChange={(e) => updateAddress(i, e.target.value)}
            placeholder={`都市 ${i + 1} (例: 東京駅)`}
            className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm"
          />
          {addresses.length > 3 && (
            <button
              type="button"
              onClick={() => removeField(i)}
              className="rounded bg-red-100 px-2 text-red-600 hover:bg-red-200"
            >
              ✕
            </button>
          )}
        </div>
      ))}
      <div className="flex gap-2">
        {addresses.length < 8 && (
          <button
            type="button"
            onClick={addField}
            className="rounded bg-gray-100 px-4 py-2 text-sm hover:bg-gray-200"
          >
            + 追加
          </button>
        )}
        <button
          type="submit"
          disabled={loading || addresses.filter((a) => a.trim()).length < 3}
          className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "計算中..." : "ルート計算"}
        </button>
      </div>
    </form>
  );
}
