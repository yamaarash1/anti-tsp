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
  display_name?: string;
  created_at: string;
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
