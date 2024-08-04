// src/services/CharacterService.ts
import axios from 'axios';
import type { Character } from '@/types/Character';

const API_URL = 'http://localhost:8000/api/v1';

export const CharacterService = {
  async getCharacters(): Promise<Character[]> {
    try {
      const response = await axios.get<any[]>(`${API_URL}/ai_personalities`);
      console.log('API response:', response.data);
      const characters = response.data.map(char => ({
        id: char.id,
        name: char.name,
        description: char.description,
        personalityTraits: char.personality_traits,
        characterType: char.character_type,
        available: char.available,
        imageUrl: `/images/${char.character_type.toLowerCase()}.png`,
        isAdaptive: char.character_type.toLowerCase() === 'adaptive'
      }));
      console.log('Mapped characters:', characters);
      return characters;
    } catch (error) {
      console.error('Error fetching characters:', error);
      return [];
    }
  }
};