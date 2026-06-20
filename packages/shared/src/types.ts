export type ApiStatus = "ok" | "degraded" | "unavailable";

export interface ApiResponse<T> {
  data: T;
  requestId?: string;
}

export interface ApiErrorResponse {
  error: {
    message: string;
    code?: string;
  };
}
