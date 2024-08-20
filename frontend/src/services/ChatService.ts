// src/services/ChatService.ts

import Message from './MessageService';
import axios from 'axios';
import { DEFAULT_CHARACTER, type Character } from '@/types/Character';

const API_URL = 'http://localhost:8000/api/v1';

interface LMStudioResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export const ChatService = {
  async getCharacters(): Promise<Character[]> {
    try {
      const response = await axios.get<Character[]>(`${API_URL}/character`);
      return [DEFAULT_CHARACTER, ...response.data];
    } catch (error) {
      console.error('Error fetching characters:', error);
      return [DEFAULT_CHARACTER];
    }
  },

  async postChatMessage(messages: Message[], characterId: number): Promise<Message> {
    const payload = {
      model: 'mlabonne/AlphaMonarch-7B-GGUF/alphamonarch-7b.Q2_K.gguf',
      messages: messages.map((message) => message.model_dump()),
      temperature: 0.7,
      max_tokens: 50,
      character_id: characterId
    };
    try {
      const response = await axios.post<LMStudioResponse>(`${API_URL}/chat/completions`, payload);
      console.log('Raw response from backend:', response.data);
      
      if (response.data.choices && response.data.choices.length > 0) {
        const aiMessage = response.data.choices[0].message;
        return new Message({
          role: aiMessage.role,
          content: aiMessage.content,
          timestamp: response.data.created * 1000, // Convert to milliseconds
          user_id: 'assistant'
        });
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  async generateImage(prompt: string, characterId: number): Promise<string> {
    try {
      const response = await axios.post(`${API_URL}/image/generate`, { prompt, ai_personality_id: characterId });
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

