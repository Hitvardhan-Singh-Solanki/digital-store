<template>
  <div v-if="showLoginModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Login</h2>
      <form @submit.prevent="loginUser">
        <div class="mb-2">
          <label class="block text-sm font-medium" for="login-username">Username</label>
          <input id="login-username" v-model="loginData.username"
                 class="w-full border border-gray-300 rounded px-2 py-1" required type="text" />
        </div>
        <div class="mb-2">
          <label class="block text-sm font-medium" for="login-password">Password</label>
          <input id="login-password" v-model="loginData.password"
                 class="w-full border border-gray-300 rounded px-2 py-1" required type="password" />
        </div>
        <div class="flex justify-end gap-2">
          <button class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600" type="button"
                  @click="closeLoginModal">
            Cancel
          </button>
          <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" type="submit">
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
import {ref, Ref} from "vue";
import {LoginData} from "@/types";

defineProps<{
  showLoginModal: boolean;
}>()

const emit = defineEmits<{
  (e: 'closeLoginModal'): void;
  (e: 'login', loginData: Ref<LoginData>): void;
}>()

const loginData = ref<LoginData>({ username: '', password: '' })

const loginUser = () => {
  emit('login', loginData);
}

const closeLoginModal = () => {
  emit('closeLoginModal');
  loginData.value = { username: '', password: '' }
}
</script>
