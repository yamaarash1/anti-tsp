"use client";

import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  Polyline,
  CircleMarker,
  Tooltip,
  useMap,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { Location, SolveResult } from "@/lib/types";

interface Props {
  locations: Location[];
  result: SolveResult;
}

function FitBounds({ locations }: { locations: Location[] }) {
  const map = useMap();
  useEffect(() => {
    if (locations.length > 0) {
      const bounds = locations.map(
        (l) => [l.lat, l.lng] as [number, number]
      );
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [locations, map]);
  return null;
}

function RouteMapInner({ locations, result }: Props) {
  const toLatLngs = (order: number[]) => {
    const pts = order.map((i) => [locations[i].lat, locations[i].lng] as [number, number]);
    pts.push(pts[0]); // 始点に戻る
    return pts;
  };

  const longestPath = toLatLngs(result.longest.order);
  const shortestPath = toLatLngs(result.shortest.order);

  return (
    <MapContainer
      center={[36.5, 137.5]}
      zoom={5}
      className="h-[400px] w-full rounded border"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <FitBounds locations={locations} />

      {/* 最長 = 赤実線 */}
      <Polyline positions={longestPath} color="red" weight={3} />

      {/* 最短 = 青点線 */}
      <Polyline
        positions={shortestPath}
        color="blue"
        weight={3}
        dashArray="8 8"
      />

      {locations.map((loc, i) => (
        <CircleMarker
          key={i}
          center={[loc.lat, loc.lng]}
          radius={6}
          fillColor="#333"
          fillOpacity={0.8}
          color="#fff"
          weight={2}
        >
          <Tooltip permanent direction="top" offset={[0, -8]}>
            {loc.name}
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}

// SSR無効化のため dynamic import で使う
export default RouteMapInner;
