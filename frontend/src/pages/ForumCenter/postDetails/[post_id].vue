<template>
  <v-container fluid>
    <v-row class="mx-8">
      <!-- 插画 -->
      <v-col cols="3" class="pt-2 sticky-col">
        <v-btn 
          color="#bdd4eb"
          prepend-icon="mdi-arrow-left"
          text="返回"
          @click="$router.go(-1)"
          class="my-2"
          style="position: fixed; bottom: 24px; left: 24px;"
        ></v-btn>

        <v-img
          src="@/assets/detail.png" 
          class="illustration"
        ></v-img>
      </v-col>
      <!-- 帖子内容 -->
      <v-col cols="9">
        <v-card
          v-if="post"
          min-height="400px"
        >
        <v-card-title class="text-h4">{{ post.title }}</v-card-title>
        <v-card-subtitle class="ml-1 pb-2" style="font-style: italic; font-size: medium;">
          {{ user_profile.nickname + " " + user_profile.email }}
        </v-card-subtitle>
        <div class="d-flex align-center ml-3 mb-2">
          <v-chip
            v-for="tagName in post.tags"
            :key="tagName"
            :color="getTagColor(tagName)"
            prepend-icon="mdi-tag"
            class="ma-1"
          >
            {{ tagName }}
          </v-chip>
        </div>
        <v-divider class="mx-4" thickness="3"></v-divider>
        <v-md-preview :text="post.content"></v-md-preview>
        <!-- 展示图片 -->
        <div class="my-4 mx-10">
          <v-carousel 
            v-if="post.images && post.images.length > 0"
            show-arrows="hover"
            cycle
          >
            <v-carousel-item
              v-for="(image, index) in post.images"
              :key="index"
              :src="`${addPrefix(image)}`"
            ></v-carousel-item>
          </v-carousel>
        </div>
        <v-card-subtitle class="text-right mr-2">发布时间: {{ new Date(post.created_at).toLocaleString() }}</v-card-subtitle>
        <v-card-actions class="justify-end">
          <v-btn
            :prepend-icon="post.like_status ? 'mdi-heart' : 'mdi-heart-outline'"
            :text="post.like_status ? '取消喜欢' : '喜欢'"
            width="100px"
            color="pink"
            @click="toggleFavorite"
          ></v-btn>
          <v-btn 
            v-if="user.user_id === post.user_id || user.is_superuser" 
            prepend-icon="mdi-pencil" 
            text="编辑帖子"
            :to="`/ForumCenter/editPost/${post.id}`"
          >
          </v-btn>
        </v-card-actions>
      </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getPost, likePost, unlikePost, addPrefix } from '@/api/post';
import { useRoute } from 'vue-router';
import { user, getPublicProfile } from '@/api/user';
const route = useRoute()

const post = ref(null);
const user_profile = ref({nickname: '111', email: '111'});

const fetchPost = async () => {
  try {
    const response = await getPost(route.params.post_id);
    console.log(response);
    post.value = response;
  } catch (error) {
    console.error('获取帖子详情失败:', error);
  }
};

const toggleFavorite = async () => {
  if (post.value.like_status) {
    await unlikePost(post.value.id);
  } else {
    await likePost(post.value.id);
  }
  post.value.like_status = !post.value.like_status;
};

const getUserProfile = async () => {
  try {
    const response = await getPublicProfile(post.value.user_id);
    user_profile.value = response;
    console.log('11', response);
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
}

const tagColors = {
  分享: 'green',
  求助: 'red',
  讨论: 'blue',
  精华: 'purple',
}

function getTagColor(tagName) {
  return tagColors[tagName] || tagColors['讨论']; 
}

onMounted(async () => {
  await fetchPost();
  await getUserProfile();
});
</script>

<style scoped>
.v-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.illustration {
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.sticky-col {
  position: sticky;
  top: 0;
  align-self: flex-start;
  z-index: 1;
}

.sticky-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>