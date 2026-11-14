export type DataKind =
  | "measured"              // lab/field measurement or official mandi arrival
  | "satellite_observed"    // derived from satellite retrievals (NDVI, IMERG)
  | "reanalysis_modelled"   // model-assimilated product (SMAP L4, POWER MERRA-2)
  | "user_entered"          // farm size entered by farmer
  | "user_entered_cost"     // custom expenditure entered by farmer (v3 extension)
  | "official_document"     // official government schemes, gazette, MSP policy (v3 extension)
  | "ai_estimate"           // ML/heuristic output
  | "scenario"              // what-if simulation (e.g. -20% rain)
  | "demo";                 // fallback demo fixture

export type ProvenanceMode = "live" | "cached" | "demo";

export interface DataProvenance {
  source: string;           // "NASA POWER", "AGMARKNET via data.gov.in"
  dataset?: string;         // e.g. "POWER Daily AG 2.0"
  kind: DataKind;
  mode: ProvenanceMode;
  observedAt?: string;      // YYYY-MM-DD
  fetchedAt: string;        // ISO timestamp
  spatialResolution?: string;
  uncertainty?: {
    low?: number;
    high?: number;
    note?: string;
  };
  url?: string;
}

export interface Provenanced<T> {
  value: T;
  provenance: DataProvenance;
}

export interface WeatherMetrics {
  temperature_c: number;
  temp_min_c: number;
  temp_max_c: number;
  precipitation_mm: number;
  soil_moisture_surface_percent: number;
  soil_moisture_rootzone_percent: number;
  solar_radiation_mj_m2: number;
  relative_humidity_percent: number;
}

export interface MandiRate {
  state: string;
  district: string;
  market: string;
  commodity: string;
  variety: string;
  min_price_inr: number;
  max_price_inr: number;
  modal_price_inr: number;
  arrival_date: string;
}
