/**
 * OCEGS Frontend - Vue Application Entry
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'

import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

// State management
app.use(createPinia())

// Routing
app.use(router)

// UI Components
app.use(Antd)

app.mount('#app')
