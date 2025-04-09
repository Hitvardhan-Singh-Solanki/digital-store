import { createRouter, createWebHistory } from "vue-router";
import Users from "./pages/Users.vue";
import Items from "./pages/Items.vue";
import Purchases from "./pages/Purchases.vue";
import { authState } from "./auth";

const routes = [
  { path: "/users", name: "users", component: Users },
  { path: "/items", name: "items", component: Items },
  { path: "/purchases", name: "purchases", component: Purchases },
  { path: "/:pathMatch(.*)*", redirect: "/users" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (!authState.isLoggedIn && to.path !== "/users") {
    alert("Please log in to access this page.");
    next("/users");
  } else {
    next();
  }
});

export default router;
