"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { User } from "@/lib/types";
import { getCurrentUser, updateProfile } from "@/lib/api";
import { loadUser, saveUser } from "@/lib/auth";
import Header from "@/components/Header";

export default function SettingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [profileMsg, setProfileMsg] = useState("");
  const [passwordMsg, setPasswordMsg] = useState("");
  const [profileError, setProfileError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const stored = loadUser();
    if (!stored) {
      router.push("/login");
      return;
    }
    getCurrentUser(stored.username)
      .then((u) => {
        setUser(u);
        setDisplayName(u.display_name || "");
      })
      .catch(() => router.push("/login"));
  }, [router]);

  const handleProfileUpdate = async () => {
    if (!user) return;
    setProfileMsg("");
    setProfileError("");
    setLoading(true);
    try {
      const updated = await updateProfile(user.username, {
        display_name: displayName,
      });
      setUser(updated);
      saveUser(updated);
      setProfileMsg("プロフィールを更新しました");
    } catch (e) {
      setProfileError(e instanceof Error ? e.message : "更新に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async () => {
    if (!user) return;
    setPasswordMsg("");
    setPasswordError("");

    if (newPassword.length < 6) {
      setPasswordError("新しいパスワードは6文字以上にしてください");
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError("新しいパスワードが一致しません");
      return;
    }

    setLoading(true);
    try {
      await updateProfile(user.username, {
        current_password: currentPassword,
        new_password: newPassword,
      });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setPasswordMsg("パスワードを変更しました");
    } catch (e) {
      setPasswordError(e instanceof Error ? e.message : "変更に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="mx-auto max-w-2xl px-4 py-8">
      <Header user={user} />

      <h2 className="mb-6 text-xl font-bold">アカウント設定</h2>

      {/* アカウント情報 */}
      <section className="mb-8 rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">アカウント情報</h3>
        <dl className="space-y-2 text-sm">
          <div className="flex">
            <dt className="w-32 text-gray-500">ユーザー名</dt>
            <dd>{user.username}</dd>
          </div>
          <div className="flex">
            <dt className="w-32 text-gray-500">メール</dt>
            <dd>{user.email}</dd>
          </div>
          <div className="flex">
            <dt className="w-32 text-gray-500">登録日</dt>
            <dd>{new Date(user.created_at).toLocaleDateString("ja-JP")}</dd>
          </div>
          {user.history_count !== undefined && (
            <div className="flex">
              <dt className="w-32 text-gray-500">計算履歴</dt>
              <dd>{user.history_count} 件</dd>
            </div>
          )}
          {user.city_sets_count !== undefined && (
            <div className="flex">
              <dt className="w-32 text-gray-500">都市セット</dt>
              <dd>{user.city_sets_count} 件</dd>
            </div>
          )}
        </dl>
      </section>

      {/* プロフィール編集 */}
      <section className="mb-8 rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">プロフィール編集</h3>
        <div className="space-y-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              表示名
            </label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="w-full rounded border border-gray-300 px-3 py-2"
            />
          </div>
          {profileMsg && (
            <p className="text-sm text-green-600">{profileMsg}</p>
          )}
          {profileError && (
            <p className="text-sm text-red-600">{profileError}</p>
          )}
          <button
            onClick={handleProfileUpdate}
            disabled={loading}
            className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 disabled:opacity-50"
          >
            保存
          </button>
        </div>
      </section>

      {/* パスワード変更 */}
      <section className="rounded-lg border border-gray-200 bg-white p-6">
        <h3 className="mb-4 text-lg font-semibold">パスワード変更</h3>
        <div className="space-y-3">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              現在のパスワード
            </label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              className="w-full rounded border border-gray-300 px-3 py-2"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              新しいパスワード
            </label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="w-full rounded border border-gray-300 px-3 py-2"
              placeholder="6文字以上"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              新しいパスワード（確認）
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full rounded border border-gray-300 px-3 py-2"
            />
          </div>
          {passwordMsg && (
            <p className="text-sm text-green-600">{passwordMsg}</p>
          )}
          {passwordError && (
            <p className="text-sm text-red-600">{passwordError}</p>
          )}
          <button
            onClick={handlePasswordChange}
            disabled={loading || !currentPassword || !newPassword}
            className="rounded bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700 disabled:opacity-50"
          >
            パスワードを変更
          </button>
        </div>
      </section>
    </div>
  );
}
