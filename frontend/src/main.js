/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

import axios from 'axios'
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://127.0.0.1:8000/"
// Composables
import { createApp } from 'vue'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
