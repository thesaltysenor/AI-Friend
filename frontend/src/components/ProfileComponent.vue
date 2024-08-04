<template>
  <div class="profile-container">
    <h2>User Profile</h2>
    <div v-if="userStore.user">
      <p><strong>Username:</strong> {{ userStore.user.username }}</p>
      <p><strong>Email:</strong> {{ userStore.user.email }}</p>
      <p><strong>Active:</strong> {{ userStore.user.is_active ? 'Yes' : 'No' }}</p>
    </div>
    <div v-else>
      <p>No user data available. Please simulate login.</p>
    </div>
    <h3>Update Profile (Simulated)</h3>
    <form @submit.prevent="simulateUpdateProfile" class="mt-3">
      <div class="form-group">
        <label for="newUsername">New Username</label>
        <input type="text" v-model="newUsername" id="newUsername" />
      </div>
      <div class="form-group">
        <label for="newEmail">New Email</label>
        <input type="email" v-model="newEmail" id="newEmail" />
      </div>
      <button type="submit" class="btn btn-primary">Simulate Update</button>
    </form>
    <p v-if="updateMessage" class="mt-2">{{ updateMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useUserStore } from '@/store';

export default defineComponent({
  name: 'ProfileComponent',
  setup() {
    const userStore = useUserStore();
    const newUsername = ref('');
    const newEmail = ref('');
    const updateMessage = ref('');

    const simulateUpdateProfile = () => {
      if (userStore.user) {
        userStore.setUser({
          ...userStore.user,
          username: newUsername.value || userStore.user.username,
          email: newEmail.value || userStore.user.email,
        });
        updateMessage.value = 'Profile updated successfully (simulated)';
        newUsername.value = '';
        newEmail.value = '';
      } else {
        updateMessage.value = 'No user logged in';
      }
    };

    return {
      userStore,
      newUsername,
      newEmail,
      updateMessage,
      simulateUpdateProfile
    };
  }
});
</script>

<style scoped>
.profile-container {
  max-width: 600px;
}
</style>