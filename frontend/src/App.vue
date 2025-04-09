<template>
  <Navbar />
  <div class="max-w-7xl mx-auto">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import Navbar from './components/Navbar.vue';
</script>
