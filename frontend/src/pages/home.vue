<template>

    <v-container>
    <v-row no-gutters>
      <v-col cols="3" md="2" sm="1"> 
        <!-- 导航栏 -->
        <v-navigation-drawer v-model="drawer" app>
          <v-list>
            <v-list-item
              v-for="item in items"
              :key="item.title"
              :to="item.route"
              link
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-navigation-drawer>
      </v-col>
      <v-col cols="9" md="10" sm="11"> 
        <!-- 主内容 -->
        <v-main>
          <h1>欢迎来到首页</h1>
          <!-- 其他内容 -->
        </v-main>
      </v-col>
    </v-row>
  </v-container>
  </template>
  
  <script setup>
  import { ref, inject } from 'vue';

  const drawer = ref(null);
  const items = inject('items');

  </script>
  
  <style scoped>
  /* 这里可以添加一些针对home页面的特定样式 */
  </style>