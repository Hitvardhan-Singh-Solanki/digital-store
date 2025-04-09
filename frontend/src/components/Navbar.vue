<template>
    <nav class="bg-gray-800 p-4">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <Header />
            <ul class="flex space-x-4 items-center">
                <li v-if="authState.isLoggedIn">
                    <span class="text-white">Welcome, {{ authState.username }}</span>
                </li>
                <li>
                    <router-link to="/users" class="text-white hover:underline">Users</router-link>
                </li>
                <li>
                    <router-link to="/items" class="text-white hover:underline">Items</router-link>
                </li>
                <li>
                    <router-link to="/purchases" class="text-white hover:underline">Purchases</router-link>
                </li>
                <li v-if="authState.isLoggedIn">
                    <button @click="handleLogout" class="text-white hover:underline">Logout</button>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script setup lang="ts">
import Header from "./Header.vue";
import { authState, logout } from "../auth";
import { useRouter } from "vue-router";

const router = useRouter();

const handleLogout = () => {
    logout();
    router.push("/users");
};
</script>