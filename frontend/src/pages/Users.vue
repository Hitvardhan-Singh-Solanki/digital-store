<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Users</h1>
      <button class="flex items-center bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        @click="showCreateUserModal = true">
        <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
        </svg>
        Create a User
      </button>
    </div>

    <UserList v-if="!isLoading" :users="users" @deleteUser="openDeleteModal" @loginUser="showLoginModal = true" />

    <create-user-modal :show-create-user-modal="showCreateUserModal" @create-user="createUser"
      @closeCreateUserModal="closeCreateUserModal" />

    <delete-user-confirmation-modal :show-delete-modal="showDeleteModal" @close-delete-modal="closeDeleteModal"
      @confirm-delete="confirmDelete" />

    <login-user-modal :show-login-modal="showLoginModal" @login="loginUser" @close-login-modal="closeLoginModal" />
  </div>
</template>

<script lang="ts" setup>
import { onMounted, Ref, ref } from 'vue';
import { useRouter } from 'vue-router';
import UserList from '../components/UserList.vue';
import { login } from '@/auth';
import { LoginData, User } from '@/types';
import { appConfig } from '../../app.config';
import CreateUserModal from "@/components/modals/CreateUserModal.vue";
import DeleteUserConfirmationModal from "@/components/modals/DeleteUserConfirmationModal.vue";
import LoginUserModal from "@/components/modals/LoginUserModal.vue";

const users = ref<User[]>([]);
const isLoading = ref(true);
const showCreateUserModal = ref(false);
const showLoginModal = ref(false);
const showDeleteModal = ref(false);
const deleteUserId = ref<string | null>(null);

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

const createUser = async (newUser: Ref<User>): Promise<void> => {
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
    closeCreateUserModal();
  } catch (error) {
    console.error(error);
  }
};

const openDeleteModal = (userId: string) => {
  deleteUserId.value = userId;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  deleteUserId.value = null;
};

const closeCreateUserModal = () => {
  showCreateUserModal.value = false;
};

const closeLoginModal = () => {
  showLoginModal.value = false;
};

const confirmDelete = async (deletePassword: Ref<string>) => {
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

    users.value = users.value.filter((user: User) => user.id !== deleteUserId.value);
    closeDeleteModal();
  } catch (error) {
    console.error(error);
    alert('Failed to delete user. Please check your password.');
  }
};

const loginUser = async (loginData: Ref<LoginData>) => {
  const urlSearchParams = new URLSearchParams();
  urlSearchParams.set('username', loginData.value.username);
  urlSearchParams.set('password', loginData.value.password);

  try {
    const response = await fetch(`${appConfig().backend}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: urlSearchParams.toString(),
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
