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
    <purchase-confirmation-modal :selected-item="selectedItem" :show-purchase-modal="showPurchaseModal" @close-purchase-modal="closePurchaseModal" @confirm-purchase="confirmPurchase" />
  </div>
</template>

<script setup lang="ts">
import ItemCard from '@/components/ItemCard.vue';
import { appConfig } from '../../app.config';
import { onMounted, ref } from 'vue';
import { authState } from '@/auth';
import { Item } from '@/types';
import PurchaseConfirmationModal from "@/components/modals/PurchaseConfirmationModal.vue";

const items = ref<Item[]>([]);
const showPurchaseModal = ref(false);
const selectedItem = ref<Item | null>(null);

onMounted(async () => {
  const itemsRes = await fetch(`${appConfig().backend}/items`);
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
    const response = await fetch(`${appConfig().backend}/purchases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        item_id: selectedItem.value.id,
        user_id: authState.userId,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to register purchase');
    }

    const data = await response.json();
    alert(
      `Purchase of ${selectedItem.value.name} was initiated we will let you know once the payment was successful!`,
    );
    closePurchaseModal();
  } catch (error) {
    console.error(error);
    alert('Failed to complete the purchase. Please try again.');
  }
};
</script>
