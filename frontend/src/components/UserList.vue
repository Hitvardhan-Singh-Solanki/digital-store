<template>
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
                    <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                        @click="$emit('deleteUser', user.id)">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<script setup lang="ts">
interface User {
    id: string;
    username: string;
}

defineProps<{
    users: User[];
}>();
</script>