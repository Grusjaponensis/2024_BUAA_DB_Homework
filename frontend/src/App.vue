<template>
  <v-app no-footer :theme="theme">
    <v-navigation-drawer v-model="showDrawer" temporary>
      <v-icon icon="mdi-cat" size="40px" class="mx-4 mt-3" @click="showDrawer = false"></v-icon>

      <v-list density="compact" nav>
        <v-list-item v-for="item in items"
          :key="item.title"
          :prepend-icon="item.icon"
          :to="item.route"
          :title="item.title">
        </v-list-item>
        <v-list-item prepend-icon="mdi-account" title="个人资料" to="/profile" v-if="finishLoadingProfile && user.login && !user.is_superuser"></v-list-item>
        <v-list-item prepend-icon="mdi-shield-account" title="管理账户信息" to="/admin" v-if="finishLoadingProfile && user.is_superuser"></v-list-item>
        <v-list-item prepend-icon="mdi-logout" title="退出登录" v-if="finishLoadingProfile && user.login" @click="handleLogout"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar elevation="5" dark prominent>
      <template #prepend>
        <v-btn icon="mdi-menu" @click="showDrawer = !showDrawer"></v-btn>
      </template>

      <v-app-bar-title>北航猫咪管理系统</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-magnify"></v-btn>
        <v-btn :icon="theme === 'light' ? 'mdi-weather-night' : 'mdi-white-balance-sunny'" @click="toggleTheme"></v-btn>
        <v-btn icon="mdi-home-outline" @click="router.push('/')"></v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
    <v-bottom-navigation v-if="finishLoadingProfile && !user.login">
      <v-btn to="/">
        <v-icon>mdi-home</v-icon>
        <span>首页</span>
      </v-btn>

      <v-btn to="/login">
        <v-icon>mdi-login</v-icon>
        <span>登录</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
  <v-snackbar 
    v-model="snackbar.show" 
    :color="snackbar.color" 
    :text="snackbar.text" 
    :timeout="snackbar.timeout" 
    >
    <template #actions>
      <v-btn
        prepend-icon="mdi-close"
        @click="snackbar.show = false"
      >
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref } from 'vue';
import { snackbar } from './stores/app';
import snackbar_ from './api/snackbar'
import { user } from './api/user'
import { useRouter } from 'vue-router';
import { getProfile } from './api/user'

const finishLoadingProfile = ref(false)

onMounted(async() => {
  await getProfile();
  console.log("Finish Loading Profile . User Login = " + user.login)
  finishLoadingProfile.value = true;
})

const router = useRouter()

const items = ref([
  { title: '首页', icon: 'mdi-home', route: '/' },
  { title: '论坛中心', icon: 'mdi-message-text', route: '/ForumCenter/forumCenter' },
  { title: '救助行动', icon: 'mdi-ambulance', route: '/RescueAction/rescueAction' },
  { title: '猫猫基地', icon: 'mdi-cat', route: '/cats/catBase' }
]);

const showDrawer = ref(false);

const handleLogout = () => {
  user.login = false;
  user.email = '';
  user.nickname = '';
  user.is_superuser = false;
  user.is_volunteer = false;
  user.avatar_url = '';
  user.password = '';
  
  document.cookie = "access_token=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC";
  // window.location.href = "/";
  router.push("/")
  showDrawer.value = false;
  console.log("成功推出登录！")
  snackbar_.success("成功退出登录！")
}

const theme = ref('light')
// 检测系统是否处于深色模式
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
// 根据系统深色模式设置主题
const setSystemTheme = () => {
  theme.value = prefersDark.matches ? 'dark' : 'light'
  localStorage.setItem('oo_theme', theme.value)
}
// 监听系统主题的变化
prefersDark.addEventListener('change', setSystemTheme)
const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('oo_theme', theme.value)
}

onMounted(async () => {
  //const showSnackbar = route.path !== '/user/login';
  if (localStorage.getItem('oo_theme')) {
    theme.value = localStorage.getItem('oo_theme');
  } else {
    setSystemTheme();
  }
});
</script>

