<template>
  <div class="landing-page">
    <main>
      <div class="content">
        <h1>Chat Bot Messenger</h1>
        <p>
          Experience the future of communication with our AI-powered chat bot.
          Engage in intelligent conversations, get instant answers, and explore
          endless possibilities.
        </p>
        <router-link to="/chat" class="cta-button">Start Chatting</router-link>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LandingPage',
  setup() {
    // If you need to add any reactive logic in the future, you can do it here
    return {};
  }
});
</script>

<style scoped>
.landing-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f4f8;
}

.content {
  text-align: center;
  max-width: 600px;
  padding: 2rem;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
}

p {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.cta-button {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.cta-button:hover,
.cta-button:focus {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .content {
    padding: 1.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  p {
    font-size: 1rem;
  }
}
</style>