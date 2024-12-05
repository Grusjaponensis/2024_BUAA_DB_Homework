<template>
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
          <v-btn icon @click="removePost(post)">
              <v-icon>mdi-delete</v-icon>
          </v-btn>
          <v-btn icon @click="editPost(post.id)">
              <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>
  
  <script setup>
  import { getMyPosts, likePost, unlikePost, deletePost } from '@/api/post';
  import { useRouter } from 'vue-router';
  const router = useRouter();
  const posts = ref([]); 
  // 获取帖子列表
  const fetchPosts = async () => {
    try {
      const response = await getMyPosts();
      posts.value = response.posts;
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

  // 删除帖子的方法
  const removePost = async (post) => {
    try {
      await deletePost(post.id);
      posts.value = posts.value.filter(p => p.id !== post.id);
    } catch (error) {
      console.error('删除帖子失败:', error);
    }
  };
  // 修改帖子
  const editPost = (postId) => {
  router.push(`/ForumCenter/editPost/${postId}`);
  };
  // 组件挂载时获取帖子列表
  onMounted(() => {
    fetchPosts();
  });
  </script>
  
  <style scoped>
  /* 页面的特定样式 */
  </style>