import { createApp, type App } from "vue";
import AppComponent from "./App.vue";
import "./index.css";

const app: App = createApp(AppComponent);
app.mount("#app");
