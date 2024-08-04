<template>
    <div class="not-found">
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for doesn't exist or has been moved.</p>
        <router-link to="/" class="home-link">Go back to home</router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'NotFound',
    setup() {
        // If you need to add any reactive logic in the future, you can do it here
        return {};
    }
});
</script>

<style scoped>
.not-found {
    text-align: center;
    padding: 50px;
    font-family: Arial, sans-serif;
}

h1 {
    font-size: 48px;
    color: #333;
    margin-bottom: 20px;
}

p {
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.home-link {
    display: inline-block;
    color: #007bff;
    text-decoration: none;
    font-size: 16px;
    padding: 10px 20px;
    border: 1px solid #007bff;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

.home-link:hover,
.home-link:focus {
    background-color: #007bff;
    color: #fff;
}
</style>