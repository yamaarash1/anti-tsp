"use client";

import { Location, SolveResult } from "@/lib/types";

interface Props {
  result: SolveResult;
  locations: Location[];
}

export default function ResultPanel({ result, locations }: Props) {
  const diff =
    result.shortest.distance_km > 0
      ? ((result.longest.distance_km - result.shortest.distance_km) /
          result.shortest.distance_km) *
        100
      : 0;

  const routeNames = (order: number[]) =>
    order.map((i) => locations[i].name).join(" → ") +
    ` → ${locations[order[0]].name}`;

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold">結果</h2>

      <div className="rounded border border-red-300 bg-red-50 p-3">
        <h3 className="font-semibold text-red-700">
          最長ルート (Anti-TSP) — {result.longest.distance_km} km
        </h3>
        <p className="mt-1 text-sm text-red-600">
          {routeNames(result.longest.order)}
        </p>
      </div>

      <div className="rounded border border-blue-300 bg-blue-50 p-3">
        <h3 className="font-semibold text-blue-700">
          最短ルート (TSP) — {result.shortest.distance_km} km
        </h3>
        <p className="mt-1 text-sm text-blue-600">
          {routeNames(result.shortest.order)}
        </p>
      </div>

      <p className="text-sm text-gray-600">
        差分: <span className="font-bold">{diff.toFixed(1)}%</span>{" "}
        (最長は最短より {(result.longest.distance_km - result.shortest.distance_km).toFixed(1)} km 長い)
      </p>
    </div>
  );
}
