<template>
  <div class="character-selection">
    <h2>Choose Your Character</h2>
    <div v-if="characterStore.isLoading" class="loading">Loading characters...</div>
    <div v-else-if="availableCharacters.length === 0" class="no-characters">No characters available.</div>
    <div v-else class="character-grid">
      <div v-for="character in availableCharacters" :key="character.id" class="character-card"
        :class="{ 'selected': character.id === selectedCharacterId }" @click="selectCharacter(character)">
        <img :src="getCharacterImage(character)" :alt="character.name">
        <h3>{{ character.name }}</h3>
        <p>{{ character.description }}</p>
        <p><strong>Traits:</strong> {{ character.personalityTraits }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useCharacterStore } from '@/store';
import type { Character } from '@/types/Character';
import { handleError } from '@/utils/errorHandler';

export default defineComponent({
  name: 'CharacterSelection',
  props: {
    selectedCharacterId: {
      type: Number,
      default: null
    }
  },
  emits: ['character-selected'],
  setup(props, { emit }) {
    const characterStore = useCharacterStore();

    const availableCharacters = computed(() =>
      characterStore.characters.filter((char: Character) => char.available)
    );

    const fetchCharacters = async () => {
      try {
        await characterStore.fetchCharacters();
      } catch (error) {
        handleError(error, 'Failed to fetch characters');
      }
    };

    const selectCharacter = (character: Character) => {
      characterStore.setSelectedCharacter(character);
      emit('character-selected', character.id);
    };

    const getCharacterImage = (character: Character) => {
      return `/images/${character.characterType}.png`;
    };

    onMounted(fetchCharacters);

    return { characterStore, availableCharacters, selectCharacter, getCharacterImage };
  },
});
</script>

<style scoped>
.character-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.character-card {
  border: 1px solid #ccc;
  padding: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.character-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.character-card.selected {
  border-color: #0066cc;
  background-color: #e6f2ff;
}

.character-card img {
  max-width: 100%;
  height: auto;
}

.loading,
.no-characters {
  text-align: center;
  margin-top: 2rem;
  font-size: 1.2rem;
}
</style>