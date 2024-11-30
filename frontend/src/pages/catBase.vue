<template>
    <v-app>
      <!-- 左侧导航栏 -->
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
  
      <!-- 应用栏 -->
      <v-app-bar app>
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>
        <v-toolbar-title>论坛中心</v-toolbar-title>
        <v-spacer></v-spacer>
        <!-- 搜索框 -->
        <v-text-field
          solo
          flat
          label="搜索"
          prepend-inner-icon="mdi-magnify"
          hide-details
          clearable
          @click:clear="clearSearch"
          @keyup.enter="searchAnimals"
        ></v-text-field>
        <!-- 发帖按钮 -->
        <v-btn text to="/create-post" color="primary">
          <v-icon left>mdi-pencil</v-icon>
          发帖
        </v-btn>
      </v-app-bar>
  
      <!-- 主内容区域 -->
      <v-main>
        <router-view></router-view>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data: () => ({
      drawer: null,
      items: [
        { title: '首页', icon: 'mdi-home', route: '/home' },
        { title: '论坛中心', icon: 'mdi-message-text', route: '/forum-center' },
        { title: '救助行动', icon: 'mdi-ambulance', route: '/rescue-action' },
        { title: '猫猫基地', icon: 'mdi-cat', route: '/cat-base' },
        { title: '领养计划', icon: 'mdi-hand-heart', route: '/adoption-plan' },
      ],
    }),
    methods: {
      clearSearch() {
        // 清空搜索框逻辑
      },
      searchAnimals() {
        // 搜索动物逻辑
      },
    },
  };
  </script>
  
  <style scoped>
  /* 这里可以添加一些针对home页面的特定样式 */
  </style>