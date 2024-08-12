// src/services/ChatService.ts
import Message from './MessageService';
import axios from 'axios';
import {DEFAULT_CHARACTER, type Character } from '@/types/Character';

const API_URL = 'http://localhost:8000/api/v1';

export const ChatService = {
  async getCharacters(): Promise<Character[]> {
    try {
      const response = await axios.get<Character[]>(`${API_URL}/characters`);
      return [DEFAULT_CHARACTER, ...response.data];
    } catch (error) {
      console.error('Error fetching characters:', error);
      return [DEFAULT_CHARACTER];
    }
  },

  async postChatMessage(messages: Message[], characterId: number): Promise<any> {
    const payload = {
      model: 'mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf',
      messages: messages.map((message) => message.model_dump()),
      temperature: 0.7,
      max_tokens: 150,
      ai_personality_id: characterId
    };
    try {
      const response = await axios.post(`${API_URL}/chat/completions`, payload, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log('Raw response from backend:', response.data);
      // Extract the nested content
      const content = response.data.choices[0].message.content.content;
      return {
        content: content,
        adaptive_traits: response.data.adaptive_traits
      };
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  async generateImage(prompt: string, aiPersonalityId: number): Promise<string> {
    try {
      const response = await axios.post(`${API_URL}/image/generate`, { prompt, ai_personality_id: aiPersonalityId });
      return response.data.prompt_id;
    } catch (error) {
      console.error('Error generating image:', error);
      throw error;
    }
  },

  async getAdaptiveTraits(characterId: number): Promise<Record<string, number> | null> {
    try {
      const response = await axios.get(`${API_URL}/chat/adaptive-traits/${characterId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching adaptive traits:', error);
      return null;
    }
  }
};

