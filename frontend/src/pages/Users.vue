<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold">Users</h1>
            <button @click="showCreateUserForm = true"
                class="flex items-center bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create a User
            </button>
        </div>

        <div v-if="showCreateUserForm" class="mb-4 p-4 border border-gray-300 rounded">
            <h2 class="text-lg font-bold mb-2">Create User</h2>
            <form @submit.prevent="createUser">
                <div class="mb-2">
                    <label for="username" class="block text-sm font-medium">Username</label>
                    <input v-model="newUser.username" id="username" type="text"
                        class="w-full border border-gray-300 rounded px-2 py-1" required />
                </div>
                <div class="mb-2">
                    <label for="password" class="block text-sm font-medium">Password</label>
                    <input v-model="newUser.password" id="password" type="password"
                        class="w-full border border-gray-300 rounded px-2 py-1" required />
                </div>
                <div class="flex justify-end">
                    <button type="button" @click="showCreateUserForm = false"
                        class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 mr-2">Cancel</button>
                    <button type="submit"
                        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Submit</button>
                </div>
            </form>
        </div>

        <table class="table-auto w-full border-collapse border border-gray-300">
            <thead>
                <tr class="bg-gray-100">
                    <th class="border border-gray-300 px-4 py-2 text-left">Username</th>
                    <th class="border border-gray-300 px-4 py-2 text-left">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-2">{{ user.username }}</td>
                    <td class="border border-gray-300 px-4 py-2">
                        <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Login</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

interface User {
    id: string,
    username: string,
}

const users = ref<User[]>([]);

onMounted(async () => {
    const usersRes = await fetch('http://localhost:8000/api/users');

    users.value = await usersRes.json();
});

const showCreateUserForm = ref(false);
const newUser = ref({ username: "", password: "" });

const createUser = async () => {
    try {
        const response = await fetch("http://localhost:8000/api/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newUser.value),
        });

        if (!response.ok) {
            throw new Error("Failed to create user");
        }

        const createdUser = await response.json();
        users.value.push(createdUser);
        newUser.value = { username: "", password: "" };
        showCreateUserForm.value = false;
    } catch (error) {
        console.error(error);
    }
};
</script>
