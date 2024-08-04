<template>
  <div id="app">
    <nav v-if="shouldShowNav">
      <router-link to="/">Home</router-link> |
      <router-link to="/characters">Characters</router-link> |
      <router-link to="/chat">Chat</router-link> |
      <router-link to="/profile">Profile</router-link> |
      <a href="#" @click.prevent="logout" v-if="userStore.user">Logout</a>
      <router-link to="/auth" v-else>Login/Register</router-link>
    </nav>
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <ImageGenerator v-if="userStore.user && route.name !== 'Auth'" />
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useUserStore } from '@/store';
import { useRoute, useRouter } from 'vue-router';
import ImageGenerator from '@/components/ImageGenerator.vue';

export default defineComponent({
  name: 'App',
  components: {
    ImageGenerator,
  },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const route = useRoute();

    const shouldShowNav = computed(() => {
      // Hide nav on auth page
      return route.name !== 'Auth';
    });

    const logout = () => {
      userStore.logout();
      router.push('/');
    };

    onMounted(() => {
      // Simulate fetching user profile
      if (!userStore.user) {
        userStore.setUser({
          id: 1,
          username: 'test_user',
          email: 'test@example.com',
          is_active: true
        });
      }
    });

    return { userStore, logout, shouldShowNav, route };
  }
});
</script>

<style scoped>
/* Add any styles you need here */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>