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
                <v-list-item-title>{{ post.title }}</v-list-item-title>
                <v-list-item-subtitle>{{ post.content }}</v-list-item-subtitle>
                <v-list-item-subtitle class="grey--text">
                  发布于 {{ new Date(post.createdAt).toLocaleString() }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon @click="toggleFavorite(post)">
                  <v-icon>{{ post.isFavorited ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
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
        </v-footer>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { getPosts, deletePost } from '@/api/post';
import { ref, onMounted, inject } from 'vue';


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
  router.push({ name: 'PostDetails', params: { postId } });
};


// 组件挂载时获取帖子列表
onMounted(() => {
  fetchPosts();
});
</script>

<style scoped>
/* 针对forumCenter页面的特定样式 */
</style>