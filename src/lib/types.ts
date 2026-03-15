export interface Location {
  name: string;
  lat: number;
  lng: number;
  error?: string;
}

export interface Route {
  order: number[];
  distance_km: number;
}

export interface SolveResult {
  longest: Route;
  shortest: Route;
}

export interface CitySet {
  id: string;
  name: string;
  locations: Location[];
  user_id?: string;
  created_at: string;
}

export interface User {
  username: string;
  email: string;
  display_name?: string;
  created_at: string;
  updated_at?: string;
  history_count?: number;
  city_sets_count?: number;
}

export interface CalculationHistory {
  _id: string;
  user_id: string;
  locations: Location[];
  result: SolveResult;
  city_count: number;
  calculated_at: string;
  user?: User;
}

// === Graph ===

export interface GraphPoint {
  name: string;
  label?: string;
  x: number;
  y: number;
}

export interface GraphEdge {
  from: string;
  to: string;
  distance: number;
}

export interface GraphPath {
  path: string[];
  distance: number;
}

export interface GraphSolveResult {
  shortest: GraphPath;
  longest: GraphPath;
  points: GraphPoint[];
  edges: GraphEdge[];
}
