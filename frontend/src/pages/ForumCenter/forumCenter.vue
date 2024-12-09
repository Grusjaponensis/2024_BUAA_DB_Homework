<template>
    <v-container>
      <v-container>
       <!-- 管理员进行标签管理 -->
      <v-row v-if="isAdmin">
        <v-col>
          <v-btn color="primary" @click="showDialog = !showDialog" class="mb-4">
            标签管理
          </v-btn>
        </v-col>
      </v-row>

      <!-- 标签管理卡片 -->
      <v-card v-if="showDialog" class="tag-management-card">
        <v-card-title class="headline">标签管理</v-card-title>
        <v-card-text>
          <ul>
            <li v-for="tag in tags" :key="tag.id">
              {{ tag.name }}
              <button @click="removeTag(tag)"><v-icon>mdi-delete</v-icon></button>
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
        <!-- 主内容区域 -->
          <v-list>
            <v-list-item
              v-for="post in posts"
              :key="post.id"
              class="my-2"
            >
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
              <v-list-item-action>
                <v-btn icon @click="toggleFavorite(post)">
                  <v-icon>{{ post.like_status ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                </v-btn>
                <v-btn icon @click="removePost(post)" v-if="isAdmin">
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
  </v-container>
</template>

<script setup>
import { getPosts, deletePost, likePost, unlikePost } from '@/api/post';
import { getTags, create, remove } from '@/api/tags';
import { getProfile } from '@/api/user';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const posts = ref([]); 
const isAdmin = ref(false); 
const showDialog = ref(false);
const tags = ref([]);
const newTag = ref('');

const fetchTags = async () => {
  try {
    const response = await getTags();
    tags.value = response;
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
</style>