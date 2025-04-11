<template>
  <div v-if="showDeleteModal" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-lg font-bold mb-4">Confirm Deletion</h2>
      <p class="mb-4">Enter your password to confirm deletion:</p>
      <input v-model="deletePassword" class="w-full border border-gray-300 rounded px-2 py-1 mb-4"
             placeholder="Password" type="password" />
      <div class="flex justify-end gap-2">
        <button class="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600" @click="cancelDelete">
          Cancel
        </button>
        <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600" @click="confirmDelete">
          Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, Ref} from "vue";

defineProps<{
  showDeleteModal: boolean;
}>()

const emit = defineEmits<{
  (e: 'closeDeleteModal'): void;
  (e: 'confirmDelete', deletePassword: Ref<string>): void
}>();

const deletePassword = ref('');

const cancelDelete = () => {
  deletePassword.value = '';
  emit('closeDeleteModal');
}

const confirmDelete = () => {
  emit('confirmDelete', deletePassword);
  deletePassword.value = ''
};
</script>
