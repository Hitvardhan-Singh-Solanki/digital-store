import { createRouter, createWebHistory } from "vue-router";
import ItemsList from "./components/ItemsList.vue";
import PurchasesList from "./components/PurchasesList.vue";

const routes = [
  { path: "/", name: "home", component: ItemsList },
  { path: "/purchases", name: "purchases", component: PurchasesList },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
