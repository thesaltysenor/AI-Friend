// src/types/User.ts
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegistrationData {
  username: string;
  email: string;
  password: string;
}

export interface UserUpdateData {
  username?: string;
  email?: string;
  password?: string;
}