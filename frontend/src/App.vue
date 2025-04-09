<template>
  <Navbar />
  <div class="max-w-7xl mx-auto">
    <RouterView />
  </div>
  <PurchaseNotification />
</template>

<script setup lang="ts">
import Navbar from './components/Navbar.vue';
import PurchaseNotification from './components/PurchaseNotification.vue';
</script>
