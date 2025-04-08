<template>
  <div class="rounded-xl border bg-white dark:bg-primary-800 dark:border-primary-700 p-6 shadow-sm">
    <h2 class="mb-6 text-2xl font-semibold text-primary-900 dark:text-primary-100">Available Items</h2>
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div v-if="items.length">
        <ItemCard v-for="item in items" :key="item.id" :item="item" @purchase="onPurchase(item)" />
      </div>
      <div v-else class="col-span-full">
        <p class="text-center text-primary-500 dark:text-primary-400">Loading items...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ItemCard from './ItemCard.vue';

interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}

defineProps<{
  items: Item[];
}>();

const emit = defineEmits<{
  (e: 'purchase', item: Item): void;
}>();

const onPurchase = (item: Item) => {
  emit('purchase', item);
};
</script>