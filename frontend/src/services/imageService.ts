import { ref } from 'vue';
import api from './api';

export const useImageService = () => {
  const isGenerating = ref(false);
  const generatedImageUrl = ref('');

  const generateImage = async (prompt: string, characterId?: number) => {
    isGenerating.value = true;
    try {
      const response = await api.post('/image/generate', { prompt, character_id: characterId });
      return response.data.prompt_id;
    } catch (error) {
      console.error('Error generating image:', error);
      throw error;
    } finally {
      isGenerating.value = false;
    }
  };

  const getImage = async (promptId: string) => {
    try {
      const response = await api.get(`/image/${promptId}`, { responseType: 'blob' });
      const imageUrl = URL.createObjectURL(response.data);
      generatedImageUrl.value = imageUrl;
      return imageUrl;
    } catch (error) {
      console.error('Error getting image:', error);
      throw error;
    }
  };

  return {
    isGenerating,
    generatedImageUrl,
    generateImage,
    getImage,
  };
};