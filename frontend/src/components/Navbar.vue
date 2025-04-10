<template>
  <nav class="bg-gray-800 p-4">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <Header/>
      <ul v-if="authState.isLoggedIn" class="flex space-x-4 items-center">
        <li>
          <span class="text-white">Welcome, {{ authState.username }}</span>
        </li>
        <li>
          <router-link class="text-white hover:underline" to="/items"
          >Items
          </router-link
          >
        </li>
        <li>
          <router-link class="text-white hover:underline" to="/purchases"
          >Purchases
          </router-link
          >
        </li>
        <li>
          <button class="text-white hover:underline" @click="handleLogout">
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts">
import Header from './Header.vue';
import { authState, logout } from '../auth';
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogout = () => {
  logout();
  router.push('/users');
};
</script>
