<template>
    <nav class="bg-gray-800 p-4 flex">
        <div class="flex-grow">
            <router-link to="/" class="text-white hover:underline"><Header/></router-link>
        </div>
        <ul class="flex space-x-4 flex-end">
            <li>
            <router-link to="/purchases" class="text-white hover:underline">Purchases</router-link>
            </li>
            <li>
            <router-link to="/cart" class="text-white hover:underline">Cart</router-link>
            </li>
        </ul>
    </nav>
</template>

<style scoped>
.navbar {
    background-color: #333;
    padding: 1rem;
}

.navbar-list {
    list-style: none;
    display: flex;
    gap: 1rem;
    margin: 0;
    padding: 0;
}

.navbar-item {
}

.navbar-link {
    color: white;
    text-decoration: none;
}

.navbar-link:hover {
    text-decoration: underline;
}
</style>

<script lang="ts">

import Header from './Header.vue'

export default {
  name: 'Navbar',
  components: {
    Header,
  },
};
</script>