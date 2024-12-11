<template>
  <!-- 主内容区域 -->
  <v-container>
    <v-row class="mb-4" no-gutters>
    <v-col cols="12" md="3" class="sidebar">
          <!-- 分析数据栏 -->
            <v-card elevation="4" class="mb-4">
              <v-card-text class="pa-4">
                <div class="d-flex flex-column align-start">
                  <span class="body-2 mb-2">Hi！ 继续积极互动吧！</span>
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">发帖总数： </span>
                    <span class="font-weight-bold ml-auto">{{ posts.length }}</span>
                  </div>

                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">总获赞数： </span>
                    <span class="font-weight-bold ml-auto">{{ posts.reduce((acc, post) => acc + post.likes_number, 0) }}</span>
                  </div>

                  <!-- 更多分析数据 -->
                </div>
              </v-card-text>
            </v-card>
          <v-img src="@/assets/mypost.png" />
        </v-col>

    <v-col cols="12" md="9">
    <div class="d-flex justify-start mb-4 button-group">
      <v-btn :to="'/ForumCenter/forumCenter'" class="v-tag-btn">
        <v-icon>mdi-arrow-left</v-icon>
        返回
      </v-btn>
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
          <v-col cols="12" md="8">
            <v-list-item-content>
              <v-list-item-title class="text-h6 mb-2">{{ post.title }}</v-list-item-title>
              <!-- <v-list-item-subtitle style="margin-top: 10px;margin-bottom: 10px;">{{ post.content }}</v-list-item-subtitle> -->
              <v-list-item-subtitle class="grey--text mb-1">
                发布于 {{ new Date(post.created_at).toLocaleString() }}
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
        <v-row>
          <v-col cols="12" md="8"></v-col>
          <v-col cols="12" md="4" class="d-flex align-center justify-end">
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
          </v-col>
        </v-row>
        </v-card>
      </v-list-item>
    </v-list>
    <v-toolbar color='#f0f0f0' dark class="top-bar" v-if="posts.length === 0">
        <v-toolbar-title>
          你还没有发布任何帖子，快来发布你的第一篇帖子吧！
        </v-toolbar-title>
        <v-btn @click="$router.push('/ForumCenter/createPost')">去发布 </v-btn>
    </v-toolbar>
  </v-col>
</v-row>
  </v-container>
</template>
  
  <script setup>
  import { getMyPosts, likePost, unlikePost, deletePost } from '@/api/post';
  import { useRouter } from 'vue-router';
  import snackbar from '@/api/snackbar';
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
      snackbar.success('删除成功');
    } catch (error) {
      console.error('删除帖子失败:', error);
      snackbar.error('删除失败');
    }
  };
  // 修改帖子
  const editPost = (postId) => {
  router.push(`/ForumCenter/editPost/${postId}`);
  };
  // 组件挂载时获取帖子列表
  onMounted(() => {
    fetchPosts();
    fetchTags();
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
import { getTags } from '@/api/tags';
const tags = ref([]);
const selectedTags = ref(new Set());
const fetchTags = async () => {
  try {
    const response = await getTags();
    tags.value = response;
    console.log(tags.value);
  } catch (error) {
    console.error('获取标签列表失败:', error);
  }
};
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
  /* 页面的特定样式 */
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

/* 美化操作按钮 */
.v-btn {
  transition: background-color 0.3s ease-in-out; /* 背景色渐变 */
}
/*
.post-card:hover {
  transform: translateY(-5px);
} */
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

.v-btn {
  border-radius: 25%; 
  width: 40px; 
  height: 40px; 
  margin-right: 6px;
}
.sidebar {
  margin-top: 25px;
  max-width: 240px; 
  margin-right: 30px;
}
.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
  </style>