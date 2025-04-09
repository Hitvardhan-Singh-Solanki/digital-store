<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Products</h1>
    </div>
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <ItemCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        cardType="ITEM"
        @purchase="handlePurchase"
      />
    </section>

    <!-- Confirmation Modal -->
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
            @click="closePurchaseModal"
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancel
          </button>
          <button
            @click="confirmPurchase"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ItemCard from '@/components/ItemCard.vue';
import { onMounted, ref } from 'vue';
import { authState } from '@/auth';
import { Item } from '@/types';

const items = ref<Item[]>([]);
const showPurchaseModal = ref(false);
const selectedItem = ref<Item | null>(null);

onMounted(async () => {
  const itemsRes = await fetch('http://localhost:8000/api/items');
  items.value = await itemsRes.json();
});

const handlePurchase = (item: Item) => {
  selectedItem.value = item;
  showPurchaseModal.value = true;
};

const closePurchaseModal = () => {
  selectedItem.value = null;
  showPurchaseModal.value = false;
};

const confirmPurchase = async () => {
  if (!selectedItem.value || !authState.userId) {
    alert('You must be logged in to make a purchase.');
    return;
  }

  try {
    const response = await fetch('http://localhost:8000/api/purchases', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: selectedItem.value.id,
        user_id: authState.userId, // Include the logged-in user's ID
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to register purchase');
    }

    const data = await response.json();
    alert(`Purchase of ${selectedItem.value.name} was successful!`);
    closePurchaseModal();
  } catch (error) {
    console.error(error);
    alert('Failed to complete the purchase. Please try again.');
  }
};
</script>
