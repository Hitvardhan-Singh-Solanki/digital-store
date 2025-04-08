<template>
  <main class="min-h-screen bg-gradient-to-b from-primary-50 to-primary-100 py-8 test">
    <div class="container mx-auto max-w-5xl px-4">
      <header class="mb-8 text-center">
        <h1 class="text-4xl font-bold tracking-tight text-primary-900">🛒 Digital Game Store</h1>
      </header>

      <section class="space-y-8">
        <div class="rounded-xl border bg-white p-6 shadow-sm">
          <h2 class="mb-6 text-2xl font-semibold text-primary-900">Available Items</h2>
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div v-if="items.length">
              <div v-for="item in items" :key="item.id" 
                   class="group relative overflow-hidden rounded-lg border bg-white p-4 transition-all hover:shadow-md">
                <div class="flex h-full flex-col justify-between space-y-4">
                  <div>
                    <h3 class="text-lg font-semibold text-primary-800">{{ item.name }}</h3>
                    <p class="mt-2 text-sm text-primary-600">{{ item.description }}</p>
                  </div>
                  <div class="flex items-center justify-between">
                    <span class="rounded-full bg-accent-50 px-3 py-1 text-sm font-medium text-accent-700">
                      {{ item.price }} coins
                    </span>
                    <button class="rounded-md bg-primary-600 px-3 py-1 text-sm font-medium text-white transition-colors hover:bg-primary-700">
                      Purchase
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="col-span-full">
              <p class="text-center text-primary-500">Loading items...</p>
            </div>
          </div>
        </div>

        <div class="rounded-xl border bg-white p-6 shadow-sm">
          <h2 class="mb-6 text-2xl font-semibold text-primary-900">Your Purchases</h2>
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div v-if="purchases.length">
              <div v-for="purchase in purchases" :key="purchase.id" 
                   class="rounded-lg border bg-primary-50 p-4">
                <h3 class="font-medium text-primary-900">{{ purchase.item_name }}</h3>
                <time class="mt-2 block text-sm text-primary-500">{{ formatDate(purchase.timestamp) }}</time>
              </div>
            </div>
            <div v-else class="col-span-full">
              <p class="text-center text-primary-500">No purchases yet.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { cn } from "@/lib/utils";

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

const formatDate = (ts: string): string => {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(ts));
};
</script>
