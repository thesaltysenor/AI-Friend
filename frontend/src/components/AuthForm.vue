<!-- src/components/AuthForm.vue -->
<template>
    <div class="auth-form">
        <p>Authentication is currently disabled.</p>
        <button @click="simulateAuth">Simulate {{ isLogin ? 'Login' : 'Register' }}</button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useUserStore } from '@/store';
import router from '@/router';

export default defineComponent({
    name: 'AuthForm',
    props: {
        isLogin: {
            type: Boolean,
            required: true
        }
    },
    setup() {
        const userStore = useUserStore();

        const simulateAuth = () => {
            // Simulate a successful authentication
            userStore.setUser({
                id: 1,
                username: 'test_user',
                email: 'test@example.com',
                is_active: true
            });
            router.push('/chat');
        };

        return { simulateAuth };
    },
});
</script>