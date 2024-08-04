// src/types/Character.ts
export interface Character {
  id: number;
  name: string;
  description: string;
  personalityTraits: string;
  characterType: string;
  available: boolean;
  imageUrl: string;
  isAdaptive: boolean;
}

export const DEFAULT_CHARACTER: Character = {
  id: 0,
  name: "Adaptive AI Friend",
  imageUrl: "/path/to/adaptive-avatar.png",
  description: "I'm an AI Friend that adapts my personality based on our conversation.",
  personalityTraits: "Adaptive, Observant, Evolving",
  available: true,
  isAdaptive: true,
  characterType: "adaptive"
  
};