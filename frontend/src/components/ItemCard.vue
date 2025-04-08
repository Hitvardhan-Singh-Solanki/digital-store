<template>
  <div class="group relative overflow-hidden rounded-lg border bg-white dark:bg-primary-900 dark:border-primary-700 p-4 transition-all hover:shadow-md">
    <div class="flex h-full flex-col justify-between space-y-4">
      <div>
        <h3 class="text-lg font-semibold text-primary-800 dark:text-primary-100">{{ item.name }}</h3>
        <p class="mt-2 text-sm text-primary-600 dark:text-primary-300">{{ item.description }}</p>
      </div>
      <div class="flex items-center justify-between">
        <span class="rounded-full bg-accent-50 dark:bg-accent-900 px-3 py-1 text-sm font-medium text-accent-700 dark:text-accent-100">
          {{ item.price }} coins
        </span>
        <button @click="$emit('purchase')" class="rounded-md bg-primary-600 px-3 py-1 text-sm font-medium text-white transition-colors hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600">
          Purchase
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}

defineProps<{
  item: Item;
}>();

defineEmits<{
  (e: 'purchase'): void;
}>();
</script>