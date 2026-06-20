export const logLevels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] as const;
export type LogLevel = (typeof logLevels)[number];
