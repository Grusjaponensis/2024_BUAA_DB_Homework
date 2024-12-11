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
import { createPinia } from 'pinia'

import VueMarkdownEditor from '@kangc/v-md-editor';
import '@kangc/v-md-editor/lib/style/base-editor.css';
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js';
import '@kangc/v-md-editor/lib/theme/style/vuepress.css';
import Prism from 'prismjs';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';

axios.defaults.withCredentials = true
axios.defaults.baseURL = "http://127.0.0.1:8000"

// Composables
import { createApp } from 'vue';
const app = createApp(App)

registerPlugins(app)

VueMarkdownEditor.use(vuepressTheme, {
    Prism,
});

VMdPreview.use(githubTheme, {
    Prism,
});

app.use(VueMarkdownEditor);
app.use(VMdPreview);

app.mount('#app')
