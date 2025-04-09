import { createRouter, createWebHistory } from "vue-router";
import Users from "./pages/Users.vue";
import Items from "./pages/Items.vue";

const routes = [
  { path: "/users", name: "users", component: Users },
  {
    path: "/items",
    name: "items",
    component: Items,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
