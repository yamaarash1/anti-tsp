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
  created_at: string;
}
