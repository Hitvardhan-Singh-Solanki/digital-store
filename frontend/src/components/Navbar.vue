<template>
    <nav class="bg-gray-800 p-4">
        <div class="max-w-7xl mx-auto flex">
            <div class="flex-grow">
                <Header />
            </div>
            <ul class="flex space-x-4 flex-end">
                <li>
                    <router-link to="/users" class="text-white hover:underline">Users</router-link>
                </li>
                <li>
                    <router-link to="/items" class="text-white hover:underline">Items</router-link>
                </li>
                <li>
                    <router-link to="/purchases" class="text-white hover:underline">Purchases</router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script lang="ts">

import Header from './Header.vue'

export default {
    name: 'Navbar',
    components: {
        Header,
    },
};
</script>