"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import AddressForm from "@/components/AddressForm";
import ResultPanel from "@/components/ResultPanel";
import CitySetManager from "@/components/CitySetManager";
import { Location, SolveResult } from "@/lib/types";
import { geocodeAddresses, solveRoutes } from "@/lib/api";

const RouteMap = dynamic(() => import("@/components/RouteMap"), { ssr: false });

export default function Home() {
  const [locations, setLocations] = useState<Location[] | null>(null);
  const [result, setResult] = useState<SolveResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (addresses: string[]) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const locs = await geocodeAddresses(addresses);
      const failed = locs.filter((l) => l.lat === null);
      if (failed.length > 0) {
        setError(
          `以下の住所が見つかりませんでした: ${failed.map((l) => l.name).join(", ")}`
        );
        setLoading(false);
        return;
      }
      setLocations(locs);
      const res = await solveRoutes(locs);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  const handleLoadCitySet = async (locs: Location[]) => {
    setLocations(locs);
    setError(null);
    setLoading(true);
    try {
      const res = await solveRoutes(locs);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "エラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="mb-6 text-2xl font-bold">
        Anti-TSP — 最長巡回ルート探索
      </h1>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-6">
          <AddressForm onSubmit={handleSubmit} loading={loading} />
          <CitySetManager locations={locations} onLoad={handleLoadCitySet} />
        </div>

        <div className="space-y-6">
          {error && (
            <div className="rounded border border-red-300 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}
          {result && locations && (
            <>
              <ResultPanel result={result} locations={locations} />
              <RouteMap locations={locations} result={result} />
              <div className="flex gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1">
                  <span className="inline-block h-0.5 w-4 bg-red-500" /> 最長
                </span>
                <span className="flex items-center gap-1">
                  <span className="inline-block h-0.5 w-4 border-t-2 border-dashed border-blue-500" /> 最短
                </span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
