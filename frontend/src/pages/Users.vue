<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Users</h1>
      <button
        class="flex items-center bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        @click="showCreateUserModal = true"
      >
        <svg
          class="h-5 w-5 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 4v16m8-8H4"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          />
        </svg>
        Create a User
      </button>
    </div>

    <UserList
      v-if="!isLoading"
      :users="users"
      @deleteUser="openDeleteModal"
      @loginUser="showLoginModal = true"
    />

    <!-- Create User Modal -->
    <!-- TODO: create a seperate component -->
    <div
      v-if="showCreateUserModal"
      class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Create User</h2>
        <form @submit.prevent="createUser">
          <div class="mb-2">
            <label class="block text-sm font-medium" for="username"
              >Username</label
            >
            <input
              id="username"
              v-model="newUser.username"
              class="w-full border border-gray-300 rounded px-2 py-1"
              required
              type="text"
            />
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium" for="password"
              >Password</label
            >
            <input
              id="password"
              v-model="newUser.password"
              class="w-full border border-gray-300 rounded px-2 py-1"
              required
              type="password"
            />
          </div>
          <div class="flex justify-end gap-2">
            <button
              class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              type="button"
              @click="closeCreateUserModal"
            >
              Cancel
            </button>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              type="submit"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <!-- TODO: create a seperate component -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Confirm Deletion</h2>
        <p class="mb-4">Enter your password to confirm deletion:</p>
        <input
          v-model="deletePassword"
          class="w-full border border-gray-300 rounded px-2 py-1 mb-4"
          placeholder="Password"
          type="password"
        />
        <div class="flex justify-end gap-2">
          <button
            class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            @click="closeDeleteModal"
          >
            Cancel
          </button>
          <button
            class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            @click="confirmDelete"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Login Modal -->
    <!-- TODO: create a seperate component -->
    <div
      v-if="showLoginModal"
      class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h2 class="text-lg font-bold mb-4">Login</h2>
        <form @submit.prevent="loginUser">
          <div class="mb-2">
            <label class="block text-sm font-medium" for="login-username"
              >Username</label
            >
            <input
              id="login-username"
              v-model="loginData.username"
              class="w-full border border-gray-300 rounded px-2 py-1"
              required
              type="text"
            />
          </div>
          <div class="mb-2">
            <label class="block text-sm font-medium" for="login-password"
              >Password</label
            >
            <input
              id="login-password"
              v-model="loginData.password"
              class="w-full border border-gray-300 rounded px-2 py-1"
              required
              type="password"
            />
          </div>
          <div class="flex justify-end gap-2">
            <button
              class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              type="button"
              @click="closeLoginModal"
            >
              Cancel
            </button>
            <button
              class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              type="submit"
            >
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import UserList from '../components/UserList.vue';
import { login } from '@/auth';
import { User } from '@/types';
import { appConfig } from '../../app.config';

const users = ref<User[]>([]);
const isLoading = ref(true);
const showCreateUserModal = ref(false);
const showLoginModal = ref(false);
const showDeleteModal = ref(false);
const deleteUserId = ref<string | null>(null);
const deletePassword = ref('');
const newUser = ref({ username: '', password: '' });
const loginData = ref({ username: '', password: '' });

const router = useRouter();

onMounted(async () => {
  try {
    const usersRes = await fetch(`${appConfig().backend}/users`);
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
    const response = await fetch(`${appConfig().backend}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUser.value),
    });

    if (!response.ok) {
      throw new Error('Failed to create user');
    }

    const createdUser = await response.json();
    users.value.push(createdUser);
    newUser.value = { username: '', password: '' };
    closeCreateUserModal();
  } catch (error) {
    console.error(error);
  }
};

const openDeleteModal = (userId: string) => {
  deleteUserId.value = userId;
  deletePassword.value = '';
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  deleteUserId.value = null;
  deletePassword.value = '';
};

const closeCreateUserModal = () => {
  showCreateUserModal.value = false;
  newUser.value = { username: '', password: '' };
};

const closeLoginModal = () => {
  showLoginModal.value = false;
  loginData.value = { username: '', password: '' };
};

const confirmDelete = async () => {
  if (!deleteUserId.value || !deletePassword.value) return;

  try {
    const response = await fetch(
      `${appConfig().backend}/users/${deleteUserId.value}`,
      {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: deletePassword.value }),
      },
    );

    if (!response.ok) {
      throw new Error('Failed to delete user');
    }

    users.value = users.value.filter((user) => user.id !== deleteUserId.value);
    closeDeleteModal();
  } catch (error) {
    console.error(error);
    alert('Failed to delete user. Please check your password.');
  }
};

const loginUser = async () => {
  try {
    const response = await fetch(`${appConfig().backend}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(loginData.value).toString(),
    });

    if (!response.ok) {
      throw new Error('Failed to log in');
    }

    const data = await response.json();
    login(data.user_id, loginData.value.username);
    closeLoginModal();
    router.push('/items');
  } catch (error) {
    console.error(error);
    alert('Failed to log in. Please check your credentials.');
  }
};
</script>
