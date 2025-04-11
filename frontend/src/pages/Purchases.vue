<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Purchases</h1>
    </div>
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <ItemCard
        v-for="purchase in purchases"
        :key="purchase.order_id"
        :item="purchase.item"
        cardType="PURCHASE"
        :purchaseDate="purchase.timestamp"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import ItemCard from '@/components/ItemCard.vue';
import { authState } from '@/auth';
import { Purchase } from '@/types';
import { appConfig } from '../../app.config';

const purchases = ref<Purchase[]>([]);

onMounted(async () => {
  if (!authState.userId) {
    console.error('User is not logged in.');
    return;
  }

  try {
    const purchasesRes = await fetch(
      `${appConfig().backend}/purchases?user_id=${authState.userId}`,
    );
    if (!purchasesRes.ok) {
      throw new Error('Failed to fetch purchases');
    }
    purchases.value = await purchasesRes.json();
  } catch (error) {
    console.error('Error fetching purchases:', error);
  }
});
</script>
