<template>
  <section class="mt-12">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6">Your Purchases</h2>
    <div v-if="purchases.length" class="space-y-4">
      <div v-for="purchase in purchases" :key="purchase.id" class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <p class="text-gray-900 dark:text-gray-100 font-semibold">{{ purchase.item_name }}</p>
        <p class="text-sm text-gray-700 dark:text-gray-300">Purchased on: {{ formatDate(purchase.timestamp) }}</p>
      </div>
    </div>
    <p v-else class="text-gray-700 dark:text-gray-300">No purchases yet. Start shopping!</p>
  </section>
</template>

<script setup lang="ts">
import { Purchase } from "@/types"

const props = defineProps<{ purchases: Purchase[] }>();

const formatDate = (ts: string): string => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(ts));
};
</script>