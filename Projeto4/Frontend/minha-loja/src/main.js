import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import VueSSE from 'vue-sse';

const app = createApp(App);

// Registrar o plugin globalmente
app.use(VueSSE);

app.mount('#app');
