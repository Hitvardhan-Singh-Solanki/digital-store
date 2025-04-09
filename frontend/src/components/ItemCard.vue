<template>
  <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow">
    <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">{{ item.name }}</h2>
    <p class="text-sm text-gray-700 dark:text-gray-300 mt-2">{{ item.description }}</p>
    <p class="text-lg font-bold text-gray-900 dark:text-gray-100 mt-4">${{ item.price }}</p>
    <button v-if="cardType === 'ITEM'" @click="handlePurchase(item)"
      class="mt-4 w-full py-2 px-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
      Buy Now
    </button>
    <p v-if="purchaseDate" class="text-gray-300">Purchase Date: {{ formattedPurchaseDate }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, withDefaults } from "vue";

interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}

const props = withDefaults(
  defineProps<{
    item: Item;
    cardType: 'ITEM' | 'PURCHASE';
    purchaseDate?: string | null;
  }>(),
  {
    purchaseDate: null, // Default value for purchaseDate
  }
);

const emit = defineEmits<{
  (e: 'purchase', item: Item): void;
}>();

const handlePurchase = (item: Item) => {
  emit('purchase', item);
};

const formattedPurchaseDate = computed(() => {
  if (!props.purchaseDate) return "N/A"; // Default display if no purchase date is provided
  const date = new Date(props.purchaseDate); // Convert string to Date object
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
});
</script>