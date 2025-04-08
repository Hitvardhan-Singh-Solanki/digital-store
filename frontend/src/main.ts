import { createApp, type App } from "vue";
import AppComponent from "./App.vue";

const app: App = createApp(AppComponent);
app.mount("#app");
