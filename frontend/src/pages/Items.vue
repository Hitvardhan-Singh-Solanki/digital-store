<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold">Products</h1>
        </div>
        <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
            <ItemCard v-for="item in items" :key="item.id" :item="item" />
        </section>
    </div>
</template>

<script setup lang="ts">
import ItemCard from "@/components/ItemCard.vue";
import { onMounted, ref } from "vue";

interface Item {
    id: number;
    name: string;
    description: string;
    price: number;
}

const items = ref<Item[]>([]);

onMounted(async () => {
    const itemsRes = await fetch('http://localhost:8000/api/items');

    items.value = await itemsRes.json();
});


</script>