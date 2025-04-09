<template>
    <div class="p-4">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-2xl font-bold">Users</h1>
            <button @click="showCreateUserModal = true"
                class="flex items-center bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create a User
            </button>
        </div>

        <UserList v-if="!isLoading" :users="users" @deleteUser="openDeleteModal" @loginUser="showLoginModal = true" />

        <!-- Create User Modal -->
        <!-- TODO: create a seperate component -->
        <div v-if="showCreateUserModal"
            class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded shadow-lg w-96">
                <h2 class="text-lg font-bold mb-4">Create User</h2>
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
                    <div class="flex justify-end gap-2">
                        <button type="button" @click="closeCreateUserModal"
                            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">Cancel</button>
                        <button type="submit"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Submit</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <!-- TODO: create a seperate component -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded shadow-lg w-96">
                <h2 class="text-lg font-bold mb-4">Confirm Deletion</h2>
                <p class="mb-4">Enter your password to confirm deletion:</p>
                <input v-model="deletePassword" type="password" placeholder="Password"
                    class="w-full border border-gray-300 rounded px-2 py-1 mb-4" />
                <div class="flex justify-end gap-2">
                    <button @click="closeDeleteModal"
                        class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">Cancel</button>
                    <button @click="confirmDelete"
                        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">Delete</button>
                </div>
            </div>
        </div>

        <!-- Login Modal -->
        <!-- TODO: create a seperate component -->
        <div v-if="showLoginModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-6 rounded shadow-lg w-96">
                <h2 class="text-lg font-bold mb-4">Login</h2>
                <form @submit.prevent="loginUser">
                    <div class="mb-2">
                        <label for="login-username" class="block text-sm font-medium">Username</label>
                        <input v-model="loginData.username" id="login-username" type="text"
                            class="w-full border border-gray-300 rounded px-2 py-1" required />
                    </div>
                    <div class="mb-2">
                        <label for="login-password" class="block text-sm font-medium">Password</label>
                        <input v-model="loginData.password" id="login-password" type="password"
                            class="w-full border border-gray-300 rounded px-2 py-1" required />
                    </div>
                    <div class="flex justify-end gap-2">
                        <button type="button" @click="closeLoginModal"
                            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600">Cancel</button>
                        <button type="submit"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import UserList from "../components/UserList.vue";
import { login } from "@/auth";
import { User } from "@/types"


const users = ref<User[]>([]);
const isLoading = ref(true);
const showCreateUserModal = ref(false);
const showLoginModal = ref(false);
const showDeleteModal = ref(false);
const deleteUserId = ref<string | null>(null);
const deletePassword = ref("");
const newUser = ref({ username: "", password: "" });
const loginData = ref({ username: "", password: "" });

onMounted(async () => {
    try {
        const usersRes = await fetch('http://localhost:8000/api/users');
        if (!usersRes.ok) {
            throw new Error(`HTTP error! status: ${usersRes.status}`);
        }
        const data = await usersRes.json();
        users.value = data;
    } catch (error) {
        console.error('Error fetching users:', error);
    } finally {
        isLoading.value = false;
    }
});

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
        closeCreateUserModal();
    } catch (error) {
        console.error(error);
    }
};

const openDeleteModal = (userId: string) => {
    deleteUserId.value = userId;
    deletePassword.value = "";
    showDeleteModal.value = true;
};

const closeDeleteModal = () => {
    showDeleteModal.value = false;
    deleteUserId.value = null;
    deletePassword.value = "";
};

const closeCreateUserModal = () => {
    showCreateUserModal.value = false;
    newUser.value = { username: "", password: "" };
};


const closeLoginModal = () => {
    showLoginModal.value = false;
    loginData.value = { username: "", password: "" };
};


const confirmDelete = async () => {
    if (!deleteUserId.value || !deletePassword.value) return;

    try {
        const response = await fetch(`http://localhost:8000/api/users/${deleteUserId.value}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password: deletePassword.value }),
        });

        if (!response.ok) {
            throw new Error("Failed to delete user");
        }

        users.value = users.value.filter((user) => user.id !== deleteUserId.value);
        closeDeleteModal();
    } catch (error) {
        console.error(error);
        alert("Failed to delete user. Please check your password.");
    }
};

const loginUser = async () => {
    try {
        const response = await fetch("http://localhost:8000/api/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams(loginData.value).toString(),
        });

        if (!response.ok) {
            throw new Error("Failed to log in");
        }

        const data = await response.json();
        console.log("Login successful:", data);
        login(data.user_id, loginData.value.username);
        closeLoginModal();
    } catch (error) {
        console.error(error);
        alert("Failed to log in. Please check your credentials.");
    }
};
</script>