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
        @keyup.enter="searchPosts"
      ></v-text-field>
      
    </v-app-bar>

    <!-- 主内容区域 -->
    <v-main>
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
              <v-btn icon @click="deletePost(post)" v-if="isModerator">
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
            to="/create-post"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-row>
      </v-footer>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
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
      posts: [], // 存储帖子列表
      currentUser: {}, // 当前用户信息
      isModerator: false, // 是否是管理员
    };
  },
  methods: {
    clearSearch() {
      // 清空搜索框逻辑
    },
    searchPosts() {
      // 搜索帖子逻辑
    },
    fetchPosts() {
      // 获取帖子列表
      // axios.get('/api/v1/posts')
      //   .then(response => {
      //     this.posts = response.data;
      //   })
      //   .catch(error => {
      //     console.error('获取帖子列表失败:', error);
      //   });
    },
    toggleFavorite(post) {
      // 收藏或取消收藏帖子
      axios.post(`/api/v1/posts/${post.id}/favorite`, { postId: post.id })
        .then(response => {
          // 更新帖子的收藏状态
          post.isFavorited = response.data.isFavorited;
        })
        .catch(error => {
          console.error('收藏帖子失败:', error);
        });
    },
    deletePost(post) {
      // 删除帖子
      axios.delete(`/api/v1/posts/${post.id}`)
        .then(response => {
          this.posts = this.posts.filter(p => p.id !== post.id);
        })
        .catch(error => {
          console.error('删除帖子失败:', error);
        });
    },
    goToPostDetails(postId) {
      // 跳转到帖子详情页面
      this.$router.push({ name: 'PostDetails', params: { postId } });
    },
  },
  created() {
    this.fetchPosts(); // 获取帖子列表
  },
};
</script>

<style scoped>
/* 针对forumCenter页面的特定样式 */
</style>