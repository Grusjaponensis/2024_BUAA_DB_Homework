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
        <v-toolbar-title>我的收藏</v-toolbar-title>
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
          @keyup.enter="searchPosts"
        ></v-text-field>
      </v-app-bar>
  
      <!-- 主内容区域 -->
      <v-main>
        <view-router-view></view-router-view>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        drawer: null,
        items: [
          { title: '首页', icon: 'mdi-home', route: '/home' },
          { title: '论坛中心', icon: 'mdi-message-text', route: '/forum-center' },
          { title: '我的帖子', icon: 'mdi-account-circle', route: '/forum-center/my-posts' },
          { title: '我的收藏', icon: 'mdi-heart', route: '/forum-center/my-favorites' },
          { title: '救助行动', icon: 'mdi-ambulance', route: '/rescue-action' },
          { title: '猫猫基地', icon: 'mdi-cat', route: '/cat-base' },
          { title: '领养计划', icon: 'mdi-hand-heart', route: '/adoption-plan' },
        ],
      };
    },
    methods: {
      clearSearch() {
        // 清空搜索框逻辑
      },
      searchPosts() {
        // 搜索帖子逻辑
      },
    }
  };
  </script>
  
  <style scoped>
  /* 页面的特定样式 */
  </style>