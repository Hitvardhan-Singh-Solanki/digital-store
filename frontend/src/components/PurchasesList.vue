<template>
  <div class="rounded-xl border bg-white dark:bg-primary-800 dark:border-primary-700 p-6 shadow-sm">
    <h2 class="mb-6 text-2xl font-semibold text-primary-900 dark:text-primary-100">Your Purchases</h2>
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-if="purchases.length">
        <div v-for="purchase in purchases" :key="purchase.id"
          class="rounded-lg border bg-primary-50 dark:bg-primary-900 dark:border-primary-700 p-4">
          <h3 class="font-medium text-primary-900 dark:text-primary-100">{{ purchase.item_name }}</h3>
          <time class="mt-2 block text-sm text-primary-500 dark:text-primary-400">{{ formatDate(purchase.timestamp)
            }}</time>
        </div>
      </div>
      <div v-else class="col-span-full">
        <p class="text-center text-primary-500 dark:text-primary-400">No purchases yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Purchase } from "@/types"

defineProps<{
  purchases: Purchase[];
}>();

const formatDate = (ts: string): string => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(ts));
};
</script>