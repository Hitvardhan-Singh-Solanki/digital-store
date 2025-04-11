<template>
  <div
    v-if="showPurchaseModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
  >
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Confirm Purchase</h2>
      <p class="mb-4">
        Are you sure you want to purchase
        <strong>{{ selectedItem?.name }}</strong> for ${{
          selectedItem?.price
        }}?
      </p>
      <div class="flex justify-end gap-2">
        <button
          @click="$emit('closePurchaseModal')"
          class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Cancel
        </button>
        <button
          @click="$emit('confirmPurchase')"
          class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Item} from "@/types";

defineProps<{
  showPurchaseModal: boolean;
  selectedItem: Item | null
}>()

defineEmits<{
  (e: 'closePurchaseModal'): void;
  (e: 'confirmPurchase'): void;
}>()
</script>
