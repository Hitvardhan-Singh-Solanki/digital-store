<template>
  <div v-if="showCreateUserModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Create User</h2>
      <form @submit.prevent="$emit('createUser', newUser)">
        <div class="mb-2">
          <label class="block text-sm font-medium" for="username">Username</label>
          <input id="username" v-model="newUser.username" class="w-full border border-gray-300 rounded px-2 py-1"
                 required type="text" />
        </div>
        <div class="mb-2">
          <label class="block text-sm font-medium" for="password">Password</label>
          <input id="password" v-model="newUser.password" class="w-full border border-gray-300 rounded px-2 py-1"
                 required type="password" />
        </div>
        <div class="flex justify-end gap-2">
          <button class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600" type="button"
                  @click="closeCreateUserModal">
            Cancel
          </button>
          <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" type="submit">
            Submit
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {Ref, ref} from "vue";
  import {User} from "@/types";

  defineProps<{
    showCreateUserModal: boolean;
  }>()

  const emit = defineEmits<{
    (e: 'closeCreateUserModal'): void;
    (e: 'createUser', newUser: Ref<User>): Promise<void>
  }>();

  const newUser = ref<{ username: string; password: string }>({ username: '', password: '' });

  const closeCreateUserModal = () => {
    newUser.value = { username: '', password: '' };
    emit('closeCreateUserModal');
  };
</script>
