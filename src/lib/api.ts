import { Location, SolveResult, CitySet } from "./types";

const API_BASE = "/api";

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: "Unknown error" }));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

export async function geocodeAddresses(
  addresses: string[]
): Promise<Location[]> {
  const data = await fetchJSON<{ locations: Location[] }>("/geocode", {
    method: "POST",
    body: JSON.stringify({ addresses }),
  });
  return data.locations;
}

export async function solveRoutes(
  locations: Location[]
): Promise<SolveResult> {
  return fetchJSON<SolveResult>("/solve", {
    method: "POST",
    body: JSON.stringify({ locations }),
  });
}

export async function listCitySets(): Promise<CitySet[]> {
  const data = await fetchJSON<{ city_sets: CitySet[] }>("/cities");
  return data.city_sets;
}

export async function saveCitySet(
  name: string,
  locations: Location[]
): Promise<CitySet> {
  return fetchJSON<CitySet>("/cities", {
    method: "POST",
    body: JSON.stringify({ name, locations }),
  });
}

export async function deleteCitySet(id: string): Promise<void> {
  await fetchJSON(`/cities?id=${id}`, { method: "DELETE" });
}
