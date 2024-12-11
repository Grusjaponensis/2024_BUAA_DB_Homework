<template>
    <v-container>
      <!-- 顶部欢迎横栏 -->
      <v-toolbar color='#eadbe7' dark class="top-bar">
        <v-toolbar-title>
          Hello，{{ username }}，欢迎来到论坛中心，一起来积极互动吧！
        </v-toolbar-title>
      </v-toolbar>
        <!-- 标签管理卡片 -->
        <v-card v-if="showDialog" class="tag-management-card">
          <v-card-title class="headline">标签管理</v-card-title>
          <v-card-text>
            <ul>
              <li v-for="tag in tags" :key="tag.id">
                {{ tag.name }}
                <button @click="removeTag(tag)"><v-icon>mdi-close</v-icon></button>
              </li>
            </ul>
            <div class="input-group" >
              <input v-model="newTag" placeholder="添加新标签" />
              <button @click="addTag"><v-icon>mdi-plus</v-icon></button>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="showDialog = false" ><v-icon>mdi-close</v-icon>关闭</v-btn>
          </v-card-actions>
        </v-card>

      <v-container>
      <!-- 侧边栏（包含按钮） -->
      <v-row class="mb-4" no-gutters>
        <v-col cols="12" md="3" class="sidebar">
          <!-- 分析数据栏 -->
            <v-card elevation="4" class="mb-4">
              <v-card-text class="pa-4">
                <div class="d-flex flex-column align-start">
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">帖子总数： </span>
                    <span class="font-weight-bold ml-auto">352{{ totalPosts }}</span>
                  </div>
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">今日新增： </span>
                    <span class="font-weight-bold ml-auto">25{{ newToday }}</span>
                  </div>
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">总浏览量： </span>
                    <span class="font-weight-bold ml-auto">1215{{ totalViews }}</span>
                  </div>
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">站内热帖： </span>
                    <span class="font-weight-bold ml-auto">《寻找失踪小橘猫》</span>
                  </div>
                  <!-- 更多分析数据 -->
                </div>
              </v-card-text>
            </v-card>
          <v-card elevation="4">
            <v-card-text class="pa-4">
              <!-- 按钮组 -->
              <div class="d-flex flex-column align-center">
                <v-btn
                  fab
                  dark
                  rounded
                  color=#eadbe7
                  @click="createPost"
                  to="/ForumCenter/createPost"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <span class="caption">创建帖子</span>
                
                <v-btn
                  fab
                  dark
                  rounded
                  color=#aeb9e2
                  @click="myPosts"
                >
                  <v-icon>mdi-cat</v-icon>
                </v-btn>
                <span class="caption">我的帖子</span>
                
                <v-btn
                  fab
                  dark
                  rounded
                  color=#acc9e9
                  @click="myFavorites"
                >
                  <v-icon>mdi-heart</v-icon>
                </v-btn>
                <span class="caption">我的收藏</span>

                <v-btn
                  v-if="isAdmin"
                  fab
                  dark
                  rounded
                  color=#f2ddb3
                  @click="showDialog = !showDialog"
                >
                  <v-icon>mdi-tag</v-icon>
                </v-btn>
                <span class="caption" v-if="isAdmin">标签管理</span>
              </div>
            </v-card-text>
          </v-card>
          <v-img src="@/assets/cat-forum.png" />
        </v-col>

        <!-- 主内容区域（帖子列表） -->
        <v-col cols="12" md="9">
          <!-- 标签按钮组 -->
          <div class="d-flex justify-start mb-4 button-group">
            <v-btn
              v-for="tag in tags"
              :key="tag.id"
              :color="isSelected(tag.name) ? '#acc9e9' : '#f0f0f0'"
              fab
              dark
              depressed
              small
              class="v-tag-btn"
              @click="filterPostsByTag(tag.name)"
            >
              {{ tag.name }}
            </v-btn>
          </div>
        <!-- 主内容区域 -->
          <v-list>
            <v-list-item
              v-for="post in filteredPosts"
              :key="post.id"
              class="post-card my-4"
            >
            <v-card
              class="pa-4 post-card"
              color="#fff"
              elevation="4"
              hover
            >
              <v-row>
                <!-- 左侧列：标题和内容 -->
                <v-col cols="12" md="8">
                  <v-list-item-content @click="goToPostDetails(post.id)">
                    <v-list-item-title class="headline">{{ post.title }}</v-list-item-title>
                    <v-list-item-subtitle style="margin-top: 10px;margin-bottom: 10px;">{{ post.content }}</v-list-item-subtitle>
                    <v-list-item-subtitle class="grey--text">
                      post at {{ new Date(post.created_at).toLocaleString() }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      {{ post.likes_number }} likes
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-col>
                <v-col cols="12" md="4" class="d-flex align-center justify-end">
                  <div class="d-flex align-center">
                    <v-chip
                      v-for="tagName in post.tags"
                      :key="tagName"
                      :color="getTagColor(tagName)"
                      class="ma-1"
                      outlined
                      small
                    >
                      {{ tagName }}
                    </v-chip>
                  </div>
                </v-col>
              </v-row>
              <v-row >
                <v-col cols="12" md="8"></v-col>
                <v-col cols="12" md="4" class="d-flex align-center justify-end">
                  <v-list-item-action>
                    <v-btn icon @click="toggleFavorite(post)" style="margin-right: 12px;">
                      <v-icon>{{ post.like_status ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>
                    <v-btn icon @click="removePost(post)" v-if="isAdmin">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-col>
              </v-row>
            </v-card>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
      </v-container>
  </v-container>
</template>

<script setup>
import { getPosts, deletePost, likePost, unlikePost } from '@/api/post';
import { getTags, create, remove } from '@/api/tags';
import { getProfile } from '@/api/user';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { user } from '@/api/user';
import snackbar from '@/api/snackbar';

const router = useRouter();
const posts = ref([]); 
const isAdmin = ref(false); 
const showDialog = ref(false);
const tags = ref([]);
const newTag = ref('');
const selectedTags = ref(new Set());
const username = ref('');


const myPosts = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.warning('请先登录'); 
  } else {
    router.push('/ForumCenter/myPosts');
  }
}

const createPost = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.warning('请先登录'); 
  } else {
    router.push('/ForumCenter/createPost');
  }
}

const myFavorites = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.warning('请先登录'); 
  } else {
    router.push('/ForumCenter/myFavorites');
  }
}

const fetchTags = async () => {
  try {
    const response = await getTags();
    tags.value = response;
    console.log(tags.value);
  } catch (error) {
    console.error('获取标签列表失败:', error);
  }
};

const addTag = async () => {
  if (newTag.value.trim()) {
    try {
      await create(newTag.value);
      fetchTags(); 
      newTag.value = ''; 
    } catch (error) {
      console.error('添加标签失败:', error);
    }
  }
};

const removeTag = async (tag) => {
  try {
    await remove(tag.id);
    fetchTags(); 
  } catch (error) {
    console.error('删除标签失败:', error);
  }
};

const fetchProfile = async () => {
  try {
    const profile = await getProfile();
    username.value = profile.data.nickname;
    isAdmin.value = profile.data.is_superuser;
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
};
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
  fetchTags();
  fetchProfile();
  fetchPosts();
});

const tagColors = {
  分享: 'green',
  求助: 'red',
  讨论: 'blue',
  精华: 'purple',
}

function getTagColor(tagName) {
  return tagColors[tagName] || tagColors['讨论']; 
}

// 过滤帖子的方法
const filterPostsByTag = (tag) => {
  if (selectedTags.value.has(tag)) {
    selectedTags.value.delete(tag);
  } else {
    selectedTags.value.add(tag);
  }
};

const isSelected = (tagName) => {
  return selectedTags.value.has(tagName);
};

const filteredPosts = computed(() => {
  if (selectedTags.value.size === 0) {
    return posts.value;
  }
  return posts.value.filter((post) => {
    return post.tags.some((tag) => selectedTags.value.has(tag));
  });
});
</script>

<style scoped>
.tag-management-card {
  max-width: 600px;
  margin: auto;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}


input {
  margin-bottom: 10px;
  padding: 5px;
  width: calc(100% - 10px);
}

.input-group {
  display: flex;
  align-items: center;
}

.input-group input {
  flex-grow: 1;
  margin-right: 10px;
}

/* 美化帖子卡片 */
.post-card {
  border-radius: 10px; /* 圆角 */
  transition: transform 0.3s ease-in-out; /* 平滑变换 */
  background-color: #f0f0f0; /* 背景色 */
  padding: 10px; /* 内边距 */
  margin-bottom: 20px; /* 外边距 */
  cursor: pointer; /* 鼠标指针 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */

}

.post-card:hover {
  transform: translateY(-5px); /* 鼠标悬停时上移 */
}

/* 美化操作按钮 */
.v-btn {
  transition: background-color 0.3s ease-in-out; /* 背景色渐变 */
}

.v-btn:hover {
  background-color: #e0e0e0; /* 鼠标悬停时的背景色 */
}

/* 标签管理卡片美化 */
.tag-management-card {
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 阴影 */
  background-color: #e5edf2;
}

/* 增加输入框和按钮的美观性 */
.input-group button {
  border: none;
  background-color: #c7d9e9;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.input-group button:hover {
  background-color: #8ea5cc;
}

/* 底部按钮美化 */
.v-footer .v-btn {
  transition: box-shadow 0.3s ease-in-out;
}

.v-footer .v-btn:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
}

.sidebar {
  max-width: 240px; 
  margin-right: 30px;
}

.v-btn {
  border-radius: 25%; 
  width: 40px; 
  height: 40px; 
  margin-right: 6px;
}
.v-tag-btn {
  border-radius: 25%; 
  width: 40px; 
  height: 40px; 
  margin-right: 12px;
}
.button-group {
  display: flex;
  justify-content: space-between;
}

.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
</style>