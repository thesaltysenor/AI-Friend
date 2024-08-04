// src/types/ApiResponses.ts
import type { User } from "./User";
import type { Character } from "./Character";

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface LoginResponse extends AuthTokens {
  user: User;
}

export interface ChatResponse {
  choices: Array<{
    message: {
      content: string;
    };
  }>;
  adaptive_traits?: Record<string, number>;
}

export interface CharacterResponse {
  characters: Character[];
}

export interface ErrorResponse {
  error: string;
  message: string;
  statusCode: number;
}

export interface RegisterResponse extends AuthTokens {
  user: User;
}

export interface UserProfileResponse {
  user: User;
}

export interface UpdateProfileResponse {
  user: User;
}