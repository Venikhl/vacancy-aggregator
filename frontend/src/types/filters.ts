export interface Filters {
  keyword?: string;
  region?: string;
  salary?: {
    min?: number;
    max?: number;
  };
  experience?: string[];
  sources?: string[];
}