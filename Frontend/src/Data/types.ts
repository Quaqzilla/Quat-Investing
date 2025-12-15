export interface StockApiResponse {
  Anomaly: boolean;
  Close: number;
  Date: string;
  RSI: number | null;
  "Z-score": number;
}

export interface ChartDataPoint {
  date: string;
  close: number;
  zscore: number;
  anomaly: boolean; 
}

export interface StockApiPayLoad {
  signal: string;
  data: StockApiResponse[];
}