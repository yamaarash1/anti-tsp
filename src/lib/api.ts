import { Location, SolveResult, CitySet, User, CalculationHistory } from "./types";

const API_BASE = "/api";

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: `サーバーに接続できません (HTTP ${res.status})` }));
    throw new Error(err.error || `サーバーエラー (HTTP ${res.status})`);
  }
  return res.json();
}

// === Geocode ===

export async function geocodeAddresses(addresses: string[]): Promise<Location[]> {
  const data = await fetchJSON<{ locations: Location[] }>("/geocode", {
    method: "POST",
    body: JSON.stringify({ addresses }),
  });
  return data.locations;
}

// === Solve ===

export async function solveRoutes(locations: Location[], userId?: string): Promise<SolveResult> {
  const body: Record<string, unknown> = { locations };
  if (userId) body.user_id = userId;
  return fetchJSON<SolveResult>("/solve", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

// === City Sets ===

export async function listCitySets(userId?: string): Promise<CitySet[]> {
  const params = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
  const data = await fetchJSON<{ city_sets: CitySet[] }>(`/cities${params}`);
  return data.city_sets;
}

export async function saveCitySet(name: string, locations: Location[], userId?: string): Promise<CitySet> {
  const body: Record<string, unknown> = { name, locations };
  if (userId) body.user_id = userId;
  return fetchJSON<CitySet>("/cities", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function deleteCitySet(id: string): Promise<void> {
  await fetchJSON(`/cities?id=${id}`, { method: "DELETE" });
}

// === Users ===

export async function createUser(username: string, displayName?: string): Promise<User> {
  return fetchJSON<User>("/users", {
    method: "POST",
    body: JSON.stringify({ username, display_name: displayName }),
  });
}

export async function getUser(username: string): Promise<User> {
  return fetchJSON<User>(`/users?username=${encodeURIComponent(username)}`);
}

export async function listUsers(): Promise<User[]> {
  const data = await fetchJSON<{ users: User[] }>("/users");
  return data.users;
}

// === History ===

export async function getHistory(userId: string, limit: number = 50): Promise<CalculationHistory[]> {
  const data = await fetchJSON<{ history: CalculationHistory[] }>(
    `/history?user_id=${encodeURIComponent(userId)}&limit=${limit}`
  );
  return data.history;
}
