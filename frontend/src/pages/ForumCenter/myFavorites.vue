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
    <v-col cols="9" md="13" sm="12">
      <!-- 主内容区域 -->
      <v-container>
        <v-list>
          <v-list-item
            v-for="post in posts"
            :key="post.id"
            class="my-2"
          >
            <v-list-item-content>
              <v-list-item-title class="headline">{{ post.title }}</v-list-item-title>
              <v-list-item-subtitle style="margin-top: 10px;margin-bottom: 10px;">{{ post.content }}</v-list-item-subtitle>
              <v-list-item-subtitle class="grey--text">
                post at {{ new Date(post.created_at).toLocaleString() }}
              </v-list-item-subtitle>
              <v-list-item-subtitle>
                {{ post.likes_number }} likes
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn icon @click="toggleFavorite(post)">
                <v-icon>{{ post.like_status ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-container>
    </v-col>
  </v-row>
</v-container>
</template>
  
  <script setup>
  import { getPosts, likePost, unlikePost } from '@/api/post';
  import { inject } from 'vue';
  const items = inject('items');
  const drawer = ref(null);
  const posts = ref([]); 
  // 获取帖子列表
  const fetchPosts = async () => {
    try {
      const response = await getPosts();
      posts.value = response.posts.filter(post => post.like_status);
    } catch (error) {
      console.error('获取帖子列表失败:', error);
    }
  };
  // 改变收藏状态
  const toggleFavorite = async (post) => {
    if (post.like_status) {
      await unlikePost(post.id);
    } else {
      await likePost(post.id);
    }
    post.like_status = !post.like_status;
  };
  // 组件挂载时获取帖子列表
  onMounted(() => {
    fetchPosts();
  });
  </script>
  
  <style scoped>
  /* 页面的特定样式 */
  </style>