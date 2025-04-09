<template>
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <ItemCard v-for="item in items" :key="item.id" :item="item" />
    </section>
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