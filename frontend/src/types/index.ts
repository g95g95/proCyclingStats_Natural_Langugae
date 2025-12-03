// Rider types
export interface RiderSpecialties {
  gc?: number;
  time_trial?: number;
  sprint?: number;
  climber?: number;
  one_day_races?: number;
}

export interface RiderData {
  name: string;
  slug?: string;
  nationality?: string;
  nationality_code?: string;
  birthdate?: string;
  age?: number;
  height?: number;
  weight?: number;
  team?: string;
  team_url?: string;
  pcs_points?: number;
  uci_points?: number;
  rank?: number;
  specialties?: RiderSpecialties;
  victories_count?: number;
  photo_url?: string;
}

// Race types
export interface RaceResultEntry {
  rank: number;
  rider_name: string;
  rider_url?: string;
  team?: string;
  time?: string;
  gap?: string;
  points?: number;
}

export interface RaceResult {
  name: string;
  slug?: string;
  year: number;
  winner?: string;
  gc_results?: RaceResultEntry[];
}

// Team types
export interface TeamRider {
  name: string;
  rider_url?: string;
  nationality?: string;
  age?: number;
}

export interface TeamInfo {
  name: string;
  slug?: string;
  year: number;
  roster?: TeamRider[];
  wins_count?: number;
  ranking?: number;
}

// Ranking types
export interface RankingEntry {
  rank: number;
  prev_rank?: number;
  rider_name?: string;
  rider_url?: string;
  team_name?: string;
  nationality?: string;
  points: number;
}

// Chat types
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface VisualizationData {
  type: 'bar_chart' | 'line_chart' | 'radar_chart' | 'pie_chart' | 'table';
  data: {
    series?: Array<Record<string, unknown>>;
    xKey?: string;
    yKey?: string;
  };
  title?: string;
}

export interface ChatResponse {
  message: string;
  data?: Record<string, unknown>;
  visualization?: VisualizationData;
}
