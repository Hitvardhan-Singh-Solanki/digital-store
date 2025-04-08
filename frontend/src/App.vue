<template>
  <div class="container">
    <h1>🛒 Digital Game Store</h1>

    <section>
      <h2>Available Items</h2>
      <ul v-if="items.length">
        <li v-for="item in items" :key="item.id">
          <strong>{{ item.name }}</strong> - {{ item.description }} ({{
            item.price
          }}
          coins)
        </li>
      </ul>
      <p v-else>Loading items...</p>
    </section>

    <section>
      <h2>Your Purchases</h2>
      <ul v-if="purchases.length">
        <li v-for="purchase in purchases" :key="purchase.id">
          Bought <strong>{{ purchase.item_name }}</strong> on
          {{ formatDate(purchase.timestamp) }}
        </li>
      </ul>
      <p v-else>No purchases yet.</p>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const items = ref([]);
const purchases = ref([]);

onMounted(async () => {
  const [itemsRes, purchasesRes] = await Promise.all([
    fetch("/api/items"),
    fetch("/api/purchases"),
  ]);

  items.value = await itemsRes.json();
  purchases.value = await purchasesRes.json();
});

const formatDate = (ts) => new Date(ts).toLocaleString();
</script>

<style>
body {
  font-family: sans-serif;
  padding: 2rem;
  background: #f9f9f9;
}

.container {
  max-width: 700px;
  margin: auto;
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1,
h2 {
  margin-bottom: 1rem;
}

ul {
  padding-left: 1.2rem;
}

li {
  margin-bottom: 0.5rem;
}
</style>
