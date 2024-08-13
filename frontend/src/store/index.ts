// store/index.ts

import { defineStore } from 'pinia';
import type { Character } from '@/types/Character';
import Message from '@/services/MessageService';
import type { User, LoginCredentials, RegistrationData, UserUpdateData } from '@/types/User';
import { CharacterService } from '@/services/CharacterService';
import { ChatService } from '@/services/ChatService';
import { useImageService } from '@/services/imageService';
import api from '@/services/api';
import router from '@/router';
import { handleError } from '@/utils/errorHandler';
import type { LoginResponse, RegisterResponse, UserProfileResponse, UpdateProfileResponse } from '@/types/ApiResponses';

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [] as Character[],
    selectedCharacter: null as Character | null,
    adaptiveTraits: null as Record<string, number> | null,
    isLoading: false,
  }),
  actions: {
    setCharacters(characters: Character[]) {
      console.log('Setting characters:', characters);
      this.characters = characters;
      if (!this.selectedCharacter && this.characters.length > 0) {
        this.setSelectedCharacter(this.characters[0]);
      }
    },
    setSelectedCharacter(character: Character) {
      this.selectedCharacter = character;
    },
    async fetchCharacters() {
      this.isLoading = true;
      try {
        const characters = await CharacterService.getCharacters();
        console.log('Fetched characters:', characters);
        this.setCharacters(characters);
      } catch (error) {
        console.error('Error fetching characters:', error);
        handleError(error, 'Error fetching characters');
      } finally {
        this.isLoading = false;
      }
    },
    async fetchAdaptiveTraits(characterId: number) {
      this.isLoading = true;
      try {
        const traits = await ChatService.getAdaptiveTraits(characterId);
        this.adaptiveTraits = traits;
      } catch (error) {
        handleError(error, 'Error fetching adaptive traits');
        this.adaptiveTraits = null;
      } finally {
        this.isLoading = false;
      }
    },
    updateAdaptiveTraits(traits: Record<string, number> | null) {
      this.adaptiveTraits = traits;
    },
  },
});

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [] as Message[],
    isLoading: false,
    isWaitingForAI: false,
  }),
  actions: {
    addMessage(message: Message) {
      this.messages.push(message);
    },
    clearMessages() {
      this.messages = [];
    },
    async sendMessage(message: Message, characterId: number) {
      if (this.isWaitingForAI) return; // Prevent sending if waiting for AI
      
      this.isLoading = true;
      this.isWaitingForAI = true;
      try {
        this.addMessage(message); // Add user message immediately
        const response = await ChatService.postChatMessage([message], characterId);
        console.log('Response in store:', response);
        
        // Create and add AI message
        const aiMessage = new Message({
          role: 'assistant',
          content: response.content,
          timestamp: Date.now(),
          user_id: 'assistant'
        });
        console.log('AI message created:', aiMessage);
        this.addMessage(aiMessage);

        if (response.adaptive_traits) {
          useCharacterStore().updateAdaptiveTraits(response.adaptive_traits);
        }
        return aiMessage;
      } catch (error) {
        handleError(error, 'Error sending message');
        throw error;
      } finally {
        this.isLoading = false;
        this.isWaitingForAI = false;
      }
    },
    async generateImage(prompt: string, aiPersonalityId: number) {
      this.isLoading = true;
      try {
        const imageService = useImageService();
        const promptId = await imageService.generateImage(prompt, aiPersonalityId);
        const imageUrl = await imageService.getImage(promptId);
        this.addMessage(new Message({
          role: 'assistant',
          content: `Generated image: ${imageUrl}`,
          timestamp: Date.now(),
        }));
        return imageUrl;
      } catch (error) {
        handleError(error, 'Error generating image');
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
  },
});

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isLoading: false,
  }),
  actions: {
    setUser(user: User) {
      this.user = user;
    },
    async login(credentials: LoginCredentials) {
      this.isLoading = true;
      try {
        const response = await api.post<LoginResponse>('/auth/login', credentials);
        this.setUser(response.data.user);
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
        router.push('/chat');
      } catch (error) {
        handleError(error, 'Login failed');
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    async register(data: RegistrationData) {
      this.isLoading = true;
      try {
        const response = await api.post<RegisterResponse>('/auth/register', data);
        this.setUser(response.data.user);
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('refreshToken', response.data.refresh_token);
        router.push('/chat');
      } catch (error) {
        handleError(error, 'Registration failed');
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    async fetchUserProfile() {
      this.isLoading = true;
      try {
        const response = await api.get<UserProfileResponse>('/users/me');
        this.setUser(response.data.user);
      } catch (error) {
        handleError(error, 'Error fetching user profile');
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    async updateProfile(updateData: UserUpdateData) {
      if (!this.user) throw new Error('No user logged in');
      this.isLoading = true;
      try {
        const response = await api.put<UpdateProfileResponse>(`/users/${this.user.id}`, updateData);
        this.setUser(response.data.user);
      } catch (error) {
        handleError(error, 'Error updating profile');
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    async logout() {
      this.isLoading = true;
      try {
        await api.post('/auth/logout');
      } catch (error) {
        handleError(error, 'Logout failed');
      } finally {
        this.user = null;
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        this.isLoading = false;
        router.push('/');
      }
    },
  },
});

export { useCharacterStore as characterStore };
export { useChatStore as chatStore };
export { useUserStore as userStore };