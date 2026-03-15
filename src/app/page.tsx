"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Header from "@/components/Header";
import PointSelector from "@/components/PointSelector";
import GraphView from "@/components/GraphView";
import GraphResultPanel from "@/components/GraphResultPanel";
import { fetchGraphPoints, fetchGraphEdges, solveGraph } from "@/lib/api";
import { loadUser } from "@/lib/auth";
import { GraphPoint, GraphEdge, GraphSolveResult, User } from "@/lib/types";

export default function Home() {
  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [points, setPoints] = useState<GraphPoint[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [result, setResult] = useState<GraphSolveResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = loadUser();
    if (!user) { router.push("/login"); return; }
    setCurrentUser(user);

    Promise.all([fetchGraphPoints(), fetchGraphEdges()])
      .then(([pts, edgs]) => { setPoints(pts); setEdges(edgs); })
      .catch(() => setError("グラフデータの読み込みに失敗しました"));
  }, [router]);

  const handleSolve = async (start: string, end: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await solveGraph(start, end, currentUser?.username);
      setResult(res);
      if (res.points) setPoints(res.points);
      if (res.edges) setEdges(res.edges);
    } catch (e) {
      setError(e instanceof Error ? e.message : "経路計算に失敗しました");
    } finally {
      setLoading(false);
    }
  };

  if (!currentUser) return null;

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <Header user={currentUser} />

      <div className="grid gap-6 md:grid-cols-3">
        <div className="space-y-6">
          <PointSelector onSolve={handleSolve} loading={loading} />
          {result && <GraphResultPanel result={result} />}
        </div>

        <div className="md:col-span-2 space-y-4">
          {error && (
            <div className="rounded border border-red-300 bg-red-50 p-3 text-sm text-red-700">{error}</div>
          )}
          <GraphView points={points} edges={edges} result={result ?? undefined} />
        </div>
      </div>
    </div>
  );
}
