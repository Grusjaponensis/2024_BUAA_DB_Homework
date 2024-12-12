<template>
  <!-- 主内容区域 -->
  <v-container>
    <v-row class="mb-4" no-gutters>
      <v-col cols="3" class="sidebar">
        <v-btn 
          color="#bdd4eb"
          prepend-icon="mdi-arrow-left"
          text="返回"
          to="/ForumCenter/forumCenter"
          class="mb-3"
        ></v-btn>
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
            </div>
          </v-card-text>
        </v-card>
        <v-img src="@/assets/mypost.png"/>
      </v-col>

      <v-col cols="9">
        <div class="d-flex justify-start mb-4 button-group">
          <v-btn
            v-for="tag in tags"
            :key="tag.id"
            :color="isSelected(tag.name) ? getTagColor(tag.name) : 'accent'"
            class="mx-1"
            prepend-icon="mdi-tag-outline"
            @click="filterPostsByTag(tag.name)"
          >
            {{ tag.name }}
          </v-btn>
        </div>

        <v-card
          v-for="post in filteredPosts"
          :key="post.id"
          class="pa-1 mb-4 rounded-lg"
          elevation="2"
          :to="`/ForumCenter/postDetails/${post.id}`"
        >
          <template #append>
            <v-chip
              v-for="tagName in post.tags"
              :key="tagName"
              :color="getTagColor(tagName)"
              prepend-icon="mdi-tag"
              class="ma-1"
            >
              {{ tagName }}
            </v-chip>
          </template>
          <template #title>{{ post.title }}</template>
          <v-card-text class="text-caption">
              发布于 {{ new Date(post.created_at).toLocaleString() }}
          </v-card-text>
          <v-chip
            :text="`${post.likes_number} likes`"
            prepend-icon="mdi-heart"
            color="red"
            class="my-2 ml-3"
          ></v-chip>
        </v-card>
        <v-toolbar color='#f0f0f0' dark class="top-bar" v-if="posts.length === 0">
          <v-toolbar-title>
            你还没有发布任何帖子，快来发布你的第一篇帖子吧！
          </v-toolbar-title>
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
  .button-group {
    display: flex;
    justify-content: space-between;
  }

  .sidebar {
    max-width: 240px; 
    margin-right: 30px;
  }
  .top-bar {
    border-radius: 8px;
    margin-bottom: 10px;
    padding: 1px 1px;
  }
</style>