<template>
  <div class="chat-container">
    <div class="character-info" v-if="characterStore.selectedCharacter">
      <img :src="getCharacterImage(characterStore.selectedCharacter)" :alt="characterStore.selectedCharacter.name"
        class="character-avatar">
      <h2>{{ characterStore.selectedCharacter.name }}</h2>
      <p>{{ characterStore.selectedCharacter.description }}</p>
    </div>
    <div class="chat-history" ref="chatHistory">
      <div v-for="message in formattedMessages" :key="message.timestamp"
        :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']">
        <div class="message-content">{{ message.content }}</div>
        <div class="message-timestamp">{{ formatTimestamp(message.timestamp) }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input type="text" v-model="newMessage" @keyup.enter="sendMessage" :disabled="chatStore.isWaitingForAI"
        placeholder="Type your message...">
      <button @click="sendMessage" :disabled="!canSendMessage">
        {{ chatStore.isWaitingForAI ? 'Waiting...' : 'Send' }}
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch, computed, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useCharacterStore, useChatStore } from '@/store';
import Message from '@/services/MessageService';
import { handleError } from '@/utils/errorHandler';

export default defineComponent({
  name: 'ChatWindow',
  setup() {
    const route = useRoute();
    const characterStore = useCharacterStore();
    const chatStore = useChatStore();
    const newMessage = ref('');
    const chatHistory = ref<HTMLElement | null>(null);

    const getCharacterImage = (character: any) => {
      console.log('Getting character image for:', character);
      return `/images/${character.characterType.toLowerCase()}.png`;
    };

    const formatTimestamp = (timestamp: number) => {
      return new Date(timestamp).toLocaleTimeString();
    };

    const formattedMessages = computed(() => {
      return chatStore.messages.map(message => ({
        ...message,
        content: typeof message.content === 'string' ? message.content : JSON.stringify(message.content)
      }));
    });

    const canSendMessage = computed(() => !chatStore.isWaitingForAI && newMessage.value.trim() !== '');

    const sendMessage = async () => {
      console.log('Attempting to send message');
      if (canSendMessage.value && characterStore.selectedCharacter) {
        console.log('Conditions met for sending message');
        const userMessage = new Message({
          role: 'user',
          content: newMessage.value,
          timestamp: Date.now(),
          user_id: 'test_user'
        });

        console.log('Created user message:', userMessage);
        newMessage.value = ''; // Clear input immediately

        try {
          console.log('Sending message to chat store');
          await chatStore.sendMessage(userMessage, characterStore.selectedCharacter.id);
        } catch (error) {
          console.error('Error in sendMessage:', error);
          handleError(error, 'Failed to send message');
        }
      } else {
        console.log('Cannot send message. canSendMessage:', canSendMessage.value, 'selectedCharacter:', characterStore.selectedCharacter);
      }
    };

    const scrollToBottom = () => {
      console.log('Scrolling to bottom');
      if (chatHistory.value) {
        chatHistory.value.scrollTop = chatHistory.value.scrollHeight;
      }
    };

    onMounted(async () => {
      console.log('ChatWindow mounted');
      const characterId = Number(route.params.characterId);
      console.log('Character ID from route:', characterId);
      if (characterId) {
        console.log('Fetching characters');
        await characterStore.fetchCharacters();
        const character = characterStore.characters.find(c => c.id === characterId);
        if (character) {
          console.log('Setting selected character:', character);
          characterStore.setSelectedCharacter(character);
          chatStore.clearMessages();
        } else {
          console.log('Character not found for ID:', characterId);
        }
      } else {
        console.log('No character ID in route');
      }
      scrollToBottom();
    });

    watch(() => chatStore.messages, (newMessages) => {
      console.log('Chat messages updated:', newMessages);
      newMessages.forEach((message, index) => {
        console.log(`Message ${index}:`, message);
        console.log(`Message ${index} content type:`, typeof message.content);
        console.log(`Message ${index} content:`, message.content);
      });
      nextTick(() => {
        scrollToBottom();
      });
    }, { deep: true });

    return {
      characterStore,
      chatStore,
      newMessage,
      sendMessage,
      canSendMessage,
      getCharacterImage,
      formatTimestamp,
      chatHistory,
      formattedMessages
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