<template>
    <div class="auth-container">
        <h2>{{ isLogin ? 'Login' : 'Register' }}</h2>
        <AuthForm :isLogin="isLogin" @auth-success="handleAuthSuccess" @auth-error="handleAuthError" />
        <p v-if="error" class="error-message">{{ error }}</p>
        <p class="toggle-form" @click="toggleForm">
            {{ isLogin ? "Don't have an account? Register" : "Already have an account? Login" }}
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import AuthForm from './AuthForm.vue';

export default defineComponent({
    name: 'AuthPage',
    components: {
        AuthForm,
    },
    setup() {
        const isLogin = ref(true);
        const error = ref('');
        const router = useRouter();

        const toggleForm = () => {
            isLogin.value = !isLogin.value;
            error.value = '';
        };

        const handleAuthSuccess = () => {
            router.push('/chat');
        };

        const handleAuthError = (err: Error) => {
            error.value = isLogin.value
                ? 'Login failed. Please check your credentials and try again.'
                : 'Registration failed. Please try again.';
            console.error(isLogin.value ? 'Login failed:' : 'Registration failed:', err);
        };

        return {
            isLogin,
            error,
            toggleForm,
            handleAuthSuccess,
            handleAuthError
        };
    },
});
</script>

<style scoped>
.auth-container {
    max-width: 400px;
}

.toggle-form {
    cursor: pointer;
    color: #007bff;
}
</style>