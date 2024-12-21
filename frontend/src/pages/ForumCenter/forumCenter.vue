<template>
  <v-container>
    <!-- 顶部欢迎横栏 -->
    <v-toolbar color="primary" class="block rounded-lg" style="opacity: 0.8;">
      <v-toolbar-title>
        Hello，{{ username }}，欢迎来到论坛中心，一起来积极互动吧！
      </v-toolbar-title>
    </v-toolbar>
    <v-dialog v-model="showDialog">
      <!-- 标签管理卡片 -->
      <v-card 
        class="tag-management-card py-3 pl-6" 
        width="30vw" 
        title="标签管理"
        :color="$vuetify.theme.name === 'dark' ? 'accent' : '#e5edf2'"
      >
        <v-card-text>
          <ul>
            <li v-for="tag in tags" :key="tag.id">
              {{ tag.name }}
              <v-btn @click="removeTag(tag)" variant="text"><v-icon>mdi-close</v-icon></v-btn>
            </li>
          </ul>
          <div class="d-flex justify-space-between align-center" >
            <input v-model="newTag" placeholder="添加新标签" />
            <v-btn @click="addTag" variant="text" class="ml-2"><v-icon>mdi-plus</v-icon></v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn 
            @click="showDialog = false"
            prepend-icon="mdi-close"
            text="关闭"
            class="mr-4"
            >
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-container>
      <!-- 侧边栏（包含按钮） -->
      <v-row class="mb-4">
        <v-col cols="3">
          <!-- 按钮组 -->
          <div class="d-flex flex-column">
            <v-btn
              block
              :color="$vuetify.theme.name === 'dark' ? 'blue-darken-2' : 'blue-lighten-1'"
              @click="checkLogin(), showCreatePostDialog = !showCreatePostDialog"
              class="my-1"
              variant="outlined"
            >
              <v-icon class="mr-1">mdi-pencil</v-icon>
              创建帖子
            </v-btn>
            
            <v-btn
              block
              :color="$vuetify.theme.name === 'dark' ? 'deep-orange-darken-3' : 'orange-lighten-1'"
              @click="myPosts"
              class="my-1"
              variant="outlined"
            >
              <v-icon class="mr-1">mdi-cat</v-icon>
              我的帖子
            </v-btn>
            
            <v-btn
              block
              :color="$vuetify.theme.name === 'dark' ? 'red-darken-4' : 'red-lighten-1'"
              @click="myFavorites"
              class="my-1"
              variant="outlined"
            >
              <v-icon class="mr-1">mdi-heart</v-icon>
              我的喜欢
            </v-btn>

            <v-btn
              v-if="isAdmin"
              block
              :color="$vuetify.theme.name === 'dark' ? 'green-darken-2' : 'green-lighten-1'"
              @click="showDialog = !showDialog"
              class="my-1"
              variant="outlined"
            >
              <v-icon class="mr-1">mdi-tag</v-icon>
              标签管理
            </v-btn>
          </div>
          <!-- 分析数据栏 -->
          <!-- <v-card variant="outlined" class="mt-5">
            <v-card-text>
              <div class="d-flex flex-column align-start">
                <div class="d-flex align-start mt-2">
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
              </div>
            </v-card-text>
          </v-card> -->
          <v-img src="@/assets/cat-forum.png" class="mt-5"/>
        </v-col>

        <!-- 主内容区域（帖子列表） -->
        <v-col cols="9">
          <!-- 标签按钮组 -->
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
          <!-- 主内容区域 -->
          <v-card
            v-for="post in filteredPosts"
            :key="post.id"
            class="pa-1 mb-4 rounded-lg"
            elevation="2"
            @click="checkLogin()"
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
        </v-col>
      </v-row>
    </v-container>
    
    <!-- 创建帖子 -->
    <v-dialog v-model="showCreatePostDialog" max-width="80vw">
      <v-toolbar title="创建帖子">
        <v-btn icon="mdi-close" @click="showCreatePostDialog = false"></v-btn>
      </v-toolbar>
      <v-card class="elevation-12">
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <v-text-field
              v-model="post.title"
              label="标题"
              counter="100"
              required
            ></v-text-field>

            <v-md-editor
              v-model="post.content" 
              height="400px"
              left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | code | link table"
              right-toolbar="preview sync-scroll"
            ></v-md-editor>

            <v-col>
              <v-row>
                <v-col cols="6">
                  <v-select
                    v-model="post.tags"
                    :items="tags.map(tag => tag.name)"
                    multiple
                    label="标签"
                    class="mt-2"
                  ></v-select>
                </v-col>
                <v-col cols="6">
                  <v-file-input
                    label="上传图片"
                    accept="image/*"
                    class="mt-2"
                    multiple
                    @change="handleFileUpload"
                  ></v-file-input>
                </v-col>
              </v-row>

              <v-row class="mt-5 justify-end">
                <v-btn
                  color="primary"
                  :disabled="!isFormValid"
                  @click="submitPost"
                >
                  发帖
                </v-btn>
              </v-row>
            </v-col>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { getPosts, deletePost, likePost, unlikePost, getPostUnauthorized } from '@/api/post';
import { getTags, create, remove } from '@/api/tags';
import { getProfile, user } from '@/api/user';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { createPost } from '@/api/post';
import snackbar from '@/api/snackbar';

const router = useRouter();
const posts = ref([]); 
const isAdmin = ref(false); 
const showDialog = ref(false);
const tags = ref([]);
const newTag = ref('');
const selectedTags = ref(new Set());
const username = ref('');
const showCreatePostDialog = ref(false);


const myPosts = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.error('请先登录!'); 
  } else {
    router.push('/ForumCenter/myPosts');
  }
}

const checkLogin = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.error('请先登录!'); 
  }
}

const myFavorites = () => {
  if (!user.login) {
    router.push('/login')
    snackbar.error('请先登录!'); 
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
    const response = await getPostUnauthorized();
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
/////////////////////
const post = ref({
  title: '',
  content: '',
  tags: [],
  images: [], // 存储上传的图片文件
});
const isFormValid = computed(() => post.value.title.trim() !== '' && post.value.content.trim() !== '');

const handleFileUpload = (event) => {
  const files = event.target.files;
  if (files) {
    post.value.images = Array.from(files);
  }
};

const submitPost = async () => {
  if (isFormValid.value && post.value) { 
    try {
      const formData = new FormData();
      console.log(post.value);
      formData.append('title', post.value.title);
      formData.append('content', post.value.content);
      formData.append('tags', post.value.tags);
      if (post.value.images.length > 0) {
        post.value.images.forEach((image, index) => {
          formData.append(`upload_images`, image);
        });
      }

      const response = await createPost(formData);
      console.log('帖子提交成功', response.data.id);
      snackbar.success('发布成功！');
      await fetchPosts();
      showCreatePostDialog.value = false;
    } catch (error) {
      console.error('发帖失败:', error);
      snackbar.error('发帖失败');
    }
  }
};

const allTags = ref([]);
const showTags = ref(false);

watchEffect(() => {
  if (showTags.value) {
    fetchTags();
  }
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
  padding: 5px;
  width: calc(100% - 10px);
}

.input-group input {
  flex-grow: 1;
  margin-right: 10px;
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

.button-group {
  display: flex;
  justify-content: space-between;
}
</style>