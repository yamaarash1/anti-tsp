"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { User } from "@/lib/types";
import { clearUser } from "@/lib/auth";

interface Props {
  user: User | null;
}

export default function Header({ user }: Props) {
  const router = useRouter();

  const handleLogout = () => {
    clearUser();
    router.push("/login");
  };

  return (
    <header className="mb-6 flex items-center justify-between border-b border-gray-200 pb-4">
      <Link href="/" className="text-2xl font-bold hover:text-blue-600">
        Anti-TSP
      </Link>
      {user ? (
        <div className="flex items-center gap-4 text-sm">
          <span className="text-gray-600">
            {user.display_name || user.username}
          </span>
          <Link
            href="/settings"
            className="rounded bg-gray-100 px-3 py-1.5 hover:bg-gray-200"
          >
            設定
          </Link>
          <button
            onClick={handleLogout}
            className="text-gray-500 hover:text-gray-700 underline"
          >
            ログアウト
          </button>
        </div>
      ) : (
        <Link
          href="/login"
          className="rounded bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700"
        >
          ログイン
        </Link>
      )}
    </header>
  );
}
