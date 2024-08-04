<template>
  <header>
    <nav>
      <div class="logo">YOUR WEBSITE</div>
      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li class="characters-dropdown">
          <router-link to="/characters">Characters</router-link>
          <ul class="dropdown-content">
            <li v-for="character in characterStore.characters" :key="character.id">
              <router-link :to="`/chat?character=${character.id}`">
                {{ character.name }}
              </router-link>
            </li>
          </ul>
        </li>
        <li><router-link to="/profile">Profile</router-link></li>
      </ul>
      <div class="auth-buttons">
        <template v-if="userStore.user">
          <span class="user-greeting">Welcome, {{ userStore.user.username }}!</span>
          <button @click="logout" class="logout-btn">Logout</button>
        </template>
        <template v-else>
          <router-link to="/auth" class="get-started-btn">Get Started</router-link>
        </template>
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useCharacterStore, useUserStore } from '@/store';
import { handleError } from '@/utils/errorHandler';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'HeaderNav',
  setup() {
    const characterStore = useCharacterStore();
    const userStore = useUserStore();
    const router = useRouter();

    onMounted(async () => {
      try {
        await characterStore.fetchCharacters();
      } catch (error) {
        handleError(error, 'Failed to fetch characters');
      }
    });

    const logout = async () => {
      try {
        await userStore.logout();
        router.push('/');
      } catch (error) {
        handleError(error, 'Failed to logout');
      }
    };

    return { characterStore, userStore, logout };
  }
});
</script>

<style scoped>
header {
  background-color: #f8f9fa;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  font-weight: bold;
  color: #0066cc;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  list-style-type: none;
  gap: 20px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-links a:hover {
  color: #0066cc;
}

.get-started-btn,
.logout-btn {
  background-color: #ff4d6d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.get-started-btn:hover,
.logout-btn:hover {
  background-color: #ff3057;
}

.characters-dropdown {
  position: relative;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #fff;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
  border-radius: 4px;
  overflow: hidden;
}

.characters-dropdown:hover .dropdown-content {
  display: block;
}

.dropdown-content a {
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  color: #333;
  transition: background-color 0.3s ease;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.user-greeting {
  margin-right: 10px;
  font-weight: 500;
}

.auth-buttons {
  display: flex;
  align-items: center;
}

@media (max-width: 768px) {
  nav {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    margin-top: 1rem;
  }

  .auth-buttons {
    margin-top: 1rem;
  }
}
</style>