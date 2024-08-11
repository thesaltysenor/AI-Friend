// src/config.ts

// For Vite, use import.meta.env instead of process.env
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
export const APP_NAME = 'AI-Friend';
export const DEFAULT_LOCALE = 'en';