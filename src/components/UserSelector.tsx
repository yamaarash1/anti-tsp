"use client";

import { useState } from "react";
import { User } from "@/lib/types";
import { createUser, getUser } from "@/lib/api";

interface Props {
  currentUser: User | null;
  onLogin: (user: User) => void;
  onLogout: () => void;
}

export default function UserSelector({ currentUser, onLogin, onLogout }: Props) {
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = async () => {
    if (!username.trim()) return;
    setLoading(true);
    setError("");
    try {
      const user = await getUser(username.trim());
      onLogin(user);
      setUsername("");
    } catch {
      setError("ユーザーが見つかりません");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!username.trim()) return;
    setLoading(true);
    setError("");
    try {
      const user = await createUser(username.trim(), displayName.trim() || undefined);
      onLogin(user);
      setUsername("");
      setDisplayName("");
      setShowRegister(false);
    } catch (e) {
      setError(e instanceof Error ? e.message : "登録に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  if (currentUser) {
    return (
      <div className="flex items-center justify-between rounded bg-green-50 border border-green-200 px-4 py-2">
        <div>
          <span className="text-sm text-green-800">
            {currentUser.display_name || currentUser.username}
          </span>
          {currentUser.history_count !== undefined && (
            <span className="ml-3 text-xs text-gray-500">
              計算履歴: {currentUser.history_count}件 / 都市セット: {currentUser.city_sets_count}件
            </span>
          )}
        </div>
        <button
          onClick={onLogout}
          className="text-xs text-gray-500 hover:text-gray-700 underline"
        >
          ログアウト
        </button>
      </div>
    );
  }

  return (
    <div className="rounded border border-gray-200 bg-gray-50 p-3 space-y-2">
      <div className="flex gap-2">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="ユーザー名"
          className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm"
          onKeyDown={(e) => { if (e.key === "Enter" && !showRegister) handleLogin(); }}
        />
        {showRegister && (
          <input
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="表示名 (任意)"
            className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm"
            onKeyDown={(e) => { if (e.key === "Enter") handleRegister(); }}
          />
        )}
        {!showRegister ? (
          <>
            <button
              onClick={handleLogin}
              disabled={loading || !username.trim()}
              className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
            >
              ログイン
            </button>
            <button
              onClick={() => setShowRegister(true)}
              className="rounded bg-gray-200 px-4 py-2 text-sm hover:bg-gray-300"
            >
              新規作成
            </button>
          </>
        ) : (
          <>
            <button
              onClick={handleRegister}
              disabled={loading || !username.trim()}
              className="rounded bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700 disabled:opacity-50"
            >
              登録
            </button>
            <button
              onClick={() => { setShowRegister(false); setError(""); }}
              className="rounded bg-gray-200 px-4 py-2 text-sm hover:bg-gray-300"
            >
              戻る
            </button>
          </>
        )}
      </div>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  );
}
