<template>
  <v-app no-footer>
    <v-navigation-drawer
        v-model="showDrawer"
        temporary
      >
        <v-list-item title="猫猫">subtitle</v-list-item>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-login" title="登录" to="/login"></v-list-item>
          <v-list-item v-for="item in items"
            :prepend-icon="item.icon"
            :to="item.route"
            :title="item.title"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>
    <v-app-bar 
      elevation="20"
      dark
      prominent
    >
      <template #prepend>
        <v-btn icon="mdi-menu" @click="showDrawer = !showDrawer"></v-btn>
      </template>

      <v-app-bar-title>Beihang Cat Management System</v-app-bar-title>

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
import { ref, provide } from 'vue';

const showDrawer = ref(false);

const items = ref([
  { title: '首页', icon: 'mdi-home', route: '/' },
  { title: '论坛中心', icon: 'mdi-message-text', route: '/ForumCenter/forumCenter' },
  { title: '救助行动', icon: 'mdi-ambulance', route: '/rescueAction' },
  { title: '猫猫基地', icon: 'mdi-cat', route: '/catBase' },
  { title: '领养计划', icon: 'mdi-hand-heart', route: '/adoptionPlan' },
]);

</script>
