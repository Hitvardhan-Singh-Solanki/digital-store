import { createApp, type App } from "vue";
import AppComponent from "./App.vue";
import "./index.css";
import router from "./router";

const app: App = createApp(AppComponent);
app.use(router);
app.mount("#app");
