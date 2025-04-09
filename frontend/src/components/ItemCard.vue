<template>
  <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow">
    <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ item.name }}</h2>
    <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">{{ item.description }}</p>
    <p class="text-lg font-bold text-gray-900 dark:text-gray-100 mt-4">${{ item.price }}</p>
    <button @click="handlePurchase(item)"
      class="mt-4 w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
      Buy Now
    </button>
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

const handlePurchase = (item: Item) => {
  console.log(`Purchasing item: ${item.name}`);
};
</script>