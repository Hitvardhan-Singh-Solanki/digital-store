<template>
  <div
    v-if="notification"
    class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg"
  >
    <div class="flex items-center">
      <svg
        class="w-6 h-6 mr-2"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 13l4 4L19 7"
        />
      </svg>
      <div>
        <h4 class="font-bold">Purchase Successful!</h4>
        <p class="text-sm">
          {{ notification.items.map((item: Item) => item.name).join(', ') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { authState } from '@/auth';
import { appConfig } from '../../app.config';
import { Item } from '@/types';
const notification = ref<any>(null);
let ws: WebSocket;

onMounted(() => {
  connectWebSocket();
});

onUnmounted(() => {
  ws?.close();
});

function connectWebSocket() {
  ws = new WebSocket(`${appConfig().backendWS}`);

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'purchase_success' && data.user_id === authState.userId) {
      notification.value = data;
      setTimeout(() => {
        notification.value = null;
      }, 5000);
    }
  };

  ws.onclose = () => {
    setTimeout(connectWebSocket, 1000);
  };
}
</script>
