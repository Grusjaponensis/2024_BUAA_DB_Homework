<template>
  <v-app>
    <v-app-bar 
    elevation="20"
    image = "https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
    dark
    prominent
    >
      <template v-slot:prepend>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
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

const items = ref([
  { title: '首页', icon: 'mdi-home', route: '/home' },
  { title: '论坛中心', icon: 'mdi-message-text', route: '/ForumCenter/forumCenter' },
  { title: '救助行动', icon: 'mdi-ambulance', route: '/rescueAction' },
  { title: '猫猫基地', icon: 'mdi-cat', route: '/catBase' },
  { title: '领养计划', icon: 'mdi-hand-heart', route: '/adoptionPlan' },
]);

provide('items', items);
</script>
