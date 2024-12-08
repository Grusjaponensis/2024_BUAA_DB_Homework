<template>
  <v-app no-footer>
    <v-navigation-drawer v-model="showDrawer" temporary>
      <v-btn class="cat-btn" icon="mdi-cat" @click="showDrawer = false"></v-btn>

      <v-list density="compact" nav>
        <v-list-item v-for="item in items"
          :key="item.title"
          :prepend-icon="item.icon"
          :to="item.route"
          :title="item.title"
          @click="handleItemClick(item)">
        </v-list-item>

        <v-list-item prepend-icon="mdi-logout" title="退出登录"  to="/" v-if="isLoggedIn" @click="handleLogout"></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar elevation="20" dark prominent>
      <template #prepend>
        <v-btn icon="mdi-menu" @click="showDrawer = !showDrawer"></v-btn>
      </template>

      <v-app-bar-title>北航猫咪管理系统</v-app-bar-title>

      <template v-slot:append>
        <v-btn icon="mdi-heart"></v-btn>
        <v-btn icon="mdi-magnify"></v-btn>
        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useUserStore } from './stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();

const items = ref([
  { title: '首页', icon: 'mdi-home', route: '/home' },
  { title: '论坛中心', icon: 'mdi-message-text', route: '/ForumCenter/forumCenter' },
  { title: '救助行动', icon: 'mdi-ambulance', route: '/RescueAction/rescueAction' },
  { title: '猫猫基地', icon: 'mdi-cat', route: '/cats/catBase' },
  { title: '领养计划', icon: 'mdi-hand-heart', route: '/adoptionPlan' }
]);

const showDrawer = ref(false);

const isLoggedIn = computed(() => userStore.isLoggedIn);


const handleItemClick = (item) => {
  if (item.title === '退出登录') {
    handleLogout();
  }
};

const handleLogout = () => {
  userStore.logout();
  router.push('/');
  showDrawer.value = false;
};

</script>

<style scoped>
.cat-btn {
  margin-top: 5px;
  margin-left: 5px;
}
</style>
