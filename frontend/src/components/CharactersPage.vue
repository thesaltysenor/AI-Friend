<template>
  <div class="characters-page">
    <main>
      <h1>Choose Your Character</h1>
      <div v-if="characterStore.isLoading" class="loading">
        Loading characters...
      </div>
      <div v-else-if="characterStore.characters.length === 0" class="no-characters">
        No characters available at the moment.
      </div>
      <div v-else class="character-grid">
        <div v-for="character in characterStore.characters" :key="character.id" class="character-card">
          <img :src="getCharacterImage(character)" :alt="character.name" class="character-image">
          <h2>{{ character.name }}</h2>
          <p>{{ character.description }}</p>
          <p><strong>Traits:</strong></p>
          <ul>
            <li v-for="(trait, index) in formatTraits(character.personalityTraits)" :key="index">
              {{ trait }}
            </li>
          </ul>
          <router-link :to="`/chat/${character.id}`" class="select-btn">Select</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useCharacterStore } from '@/store';
import { handleError } from '@/utils/errorHandler';
import type { Character } from '@/types/Character';

export default defineComponent({
  name: 'CharactersPage',
  setup() {
    const characterStore = useCharacterStore();

    onMounted(async () => {
      try {
        await characterStore.fetchCharacters();
      } catch (error) {
        handleError(error, 'Failed to fetch characters');
      }
    });

    const getCharacterImage = (character: Character) => {
      return `/images/${character.characterType.toLowerCase()}.png`;
    };

    const formatTraits = (traits: string) => {
      return traits.split('.').map(trait => trait.trim()).filter(trait => trait.length > 0);
    };

    return { characterStore, getCharacterImage, formatTraits };
  }
});
</script>


<style scoped>
.characters-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.character-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: transform 0.3s ease;
}

.character-card:hover {
  transform: translateY(-5px);
}

.character-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.select-btn {
  display: inline-block;
  background-color: #0066cc;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  text-decoration: none;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

.select-btn:hover {
  background-color: #0056b3;
}

.loading,
.no-characters {
  text-align: center;
  margin-top: 2rem;
  font-size: 1.2rem;
}
</style>