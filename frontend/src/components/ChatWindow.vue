<template>
  <div class="chat-container">
    <div class="character-info" v-if="characterStore.selectedCharacter">
      <img :src="getCharacterImage(characterStore.selectedCharacter)" :alt="characterStore.selectedCharacter.name"
        class="character-avatar">
      <h2>{{ characterStore.selectedCharacter.name }}</h2>
      <p>{{ characterStore.selectedCharacter.description }}</p>
    </div>
    <div class="chat-history" ref="chatHistory">
      <div v-for="message in chatStore.messages" :key="message.timestamp"
        :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
        <div class="message-content">{{ message.content }}</div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input type="text" v-model="newMessage" @keyup.enter="sendMessage" :disabled="chatStore.isLoading"
        placeholder="Type your message...">
      <button @click="sendMessage" :disabled="chatStore.isLoading">
        {{ chatStore.isLoading ? 'Sending...' : 'Send' }}
      </button>
    </div>
  </div>
  <ImageGenerator :aiPersonalityId="characterStore.selectedCharacter?.id" @image-generated="handleImageGenerated" />
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useCharacterStore, useChatStore } from '@/store';
import Message from '@/services/MessageService';
import { handleError } from '@/utils/errorHandler';
import ImageGenerator from '@/components/ImageGenerator.vue';

export default defineComponent({
  name: 'ChatWindow',
  setup() {
    const route = useRoute();
    const characterStore = useCharacterStore();
    const chatStore = useChatStore();
    const newMessage = ref('');
    const chatHistory = ref<HTMLElement | null>(null);

    const getCharacterImage = (character: any) => {
      return `/images/${character.characterType.toLowerCase()}.png`;
    };

    const formatTimestamp = (timestamp: number) => {
      return new Date(timestamp).toLocaleTimeString();
    };

    const handleImageGenerated = (imageUrl: string) => {
      // Add the generated image to the chat
      chatStore.addMessage(new Message({
        role: 'assistant',
        content: `Here's the image you requested: ${imageUrl}`,
        timestamp: Date.now(),
      }));
    };

    const sendMessage = async () => {
      if (newMessage.value.trim() && characterStore.selectedCharacter) {
        const userMessage = new Message({
          role: 'user',
          content: newMessage.value,
          timestamp: Date.now(),
          user_id: 'test_user'
        });

        try {
          const aiMessage = await chatStore.sendMessage(userMessage, characterStore.selectedCharacter.id);
          console.log('AI message in component:', aiMessage);
          newMessage.value = '';
        } catch (error) {
          handleError(error, 'Failed to send message');
        }
      }
    };

    const scrollToBottom = () => {
      if (chatHistory.value) {
        chatHistory.value.scrollTop = chatHistory.value.scrollHeight;
      }
    };

    onMounted(async () => {
      const characterId = Number(route.params.characterId);
      if (characterId) {
        await characterStore.fetchCharacters();
        const character = characterStore.characters.find(c => c.id === characterId);
        if (character) {
          characterStore.setSelectedCharacter(character);
          chatStore.clearMessages();
        }
      }
      scrollToBottom();
    });

    watch(() => chatStore.messages, () => {
      scrollToBottom();
    }, { deep: true });

    return {
      characterStore,
      chatStore,
      newMessage,
      sendMessage,
      getCharacterImage,
      formatTimestamp,
      chatHistory,
      handleImageGenerated
    };
  },
});
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.character-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 10px;
}

.character-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 15px;
}

.chat-history {
  height: 400px;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 5px;
  max-width: 80%;
}

.user-message {
  background-color: #dcf8c6;
  align-self: flex-end;
  margin-left: auto;
}

.ai-message {
  background-color: #e6e6e6;
  align-self: flex-start;
}

.message-timestamp {
  font-size: 0.8em;
  color: #888;
  text-align: right;
  margin-top: 5px;
}

.chat-input {
  display: flex;
}

.chat-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px 0 0 5px;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.chat-input button:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}
</style>