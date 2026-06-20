import type { ApiStatus } from "./types";

export interface HealthCheckDto {
  status: ApiStatus;
}

export interface StoreContextDto {
  storeId: string;
  shopDomain: string;
}
