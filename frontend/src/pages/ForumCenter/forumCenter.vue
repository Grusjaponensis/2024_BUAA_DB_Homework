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
              @click="goToPostDetails(post.id)"
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
                <v-btn icon @click="removePost(post)" v-if="isModerator">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-container>
        <!-- 发帖 -->
        <v-footer padless>
          <v-row justify="end" no-gutters>
            <v-btn
              fab
              dark
              fixed
              bottom
              right
              color="primary"
              to="/ForumCenter/createPost"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-row>

          <!-- 我的帖子按钮 -->
          <v-btn
            fab
            dark
            fixed
            bottom
            right
            color="secondary"
            class="mx-4"  
            to="/ForumCenter/myPosts"
          >
            <v-icon>mdi-cat</v-icon>
          </v-btn>

          <!-- 我的点赞按钮 -->
          <v-btn
            fab
            dark
            fixed
            bottom
            right
            color="light-blue"
            to="/ForumCenter/myFavorites"
          >
            <v-icon>mdi-heart</v-icon>
          </v-btn>
        </v-footer>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { getPosts, deletePost, likePost, unlikePost } from '@/api/post';
import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();


const drawer = ref(null);
const posts = ref([]); 
const isModerator = ref(false); 

const items = inject('items');
// 获取帖子列表
const fetchPosts = async () => {
  try {
    const response = await getPosts();
    posts.value = response.posts;
  } catch (error) {
    console.error('获取帖子列表失败:', error);
  }
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

// 跳转到帖子详情页面的方法
const goToPostDetails = (postId) => {
  router.push(`/ForumCenter/postDetails/${postId}`);
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
/* 针对forumCenter页面的特定样式 */
</style>