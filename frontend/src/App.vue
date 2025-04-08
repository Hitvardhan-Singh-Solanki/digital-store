<template>
  <Navbar/>
  <router-view />
  <main class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="container mx-auto max-w-6xl px-6">
      <ItemList :items="items" @purchase="handlePurchase" />
      <PurchaseList :purchases="purchases" />
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Navbar from './components/Navbar.vue';
import ItemList from './components/ItemList.vue';
import PurchaseList from './components/PurchaseList.vue';

interface Item {
  id: number;
  name: string;
  description: string;
  price: number;
}

interface Purchase {
  id: number;
  item_name: string;
  timestamp: string;
}

const items = ref<Item[]>([]);
const purchases = ref<Purchase[]>([]);

onMounted(async () => {
  const [itemsRes, purchasesRes] = await Promise.all([
    fetch("http://localhost:8000/api/items"),
    fetch("http://localhost:8000/api/purchases"),
  ]);

  items.value = await itemsRes.json();
  purchases.value = await purchasesRes.json();
});

const handlePurchase = async (item: Item) => {
  try {
    const res = await fetch("http://localhost:8000/api/purchases", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ item_id: item.id }),
    });

    if (!res.ok) {
      throw new Error('Purchase failed');
    }

    const newPurchase = await res.json();
    purchases.value = [...purchases.value, newPurchase];
  } catch (error) {
    console.error('Failed to purchase item:', error);
    alert('Failed to purchase item. Please try again.');
  }
};

const formatDate = (ts: string): string => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(ts));
};
</script>
