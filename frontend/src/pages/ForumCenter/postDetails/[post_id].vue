<template>
  <v-container>
    <v-btn color="#bdd4eb" text @click="$router.go(-1)" class="mb-3">
      <v-icon left>mdi-arrow-left</v-icon> 
      返回 
    </v-btn>
    <v-row>
      <!-- 插画 -->
      <v-col cols="3" class="pa-0">
        <v-img
          src="@/assets/detail.png" 
          class="illustration"
        ></v-img>
      </v-col>

      <!-- 帖子内容 -->
      <v-col cols="9">
        <v-card
          v-if="post"
        >
        <v-card-title class="headline" style="font-size: 24px;">{{ post.title }}</v-card-title>
        <div class="d-flex align-center ml-1">
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
        <v-md-preview :text="post.content"></v-md-preview>
        <!-- 展示图片 -->
        <v-card-text v-if="post.images && post.images.length > 0" style="margin: auto;">
          <v-img
            v-for="(image, index) in post.images"
            :key="index"
            :src="`${addPrefix(image)}`"
            class="mb-3"
            max-width="100%"
            max-height="300px"
          ></v-img>
        </v-card-text>
        <v-card-subtitle class="text-right mr-2">发布时间: {{ new Date(post.created_at).toLocaleString() }}</v-card-subtitle>
        <v-card-actions class="justify-end">
          <v-btn
            :prepend-icon="post.like_status ? 'mdi-heart' : 'mdi-heart-outline'"
            :text="post.like_status ? '取消喜欢' : '喜欢'"
            width="100px"
            color="pink"
            @click="toggleFavorite"
          ></v-btn>
          <v-btn icon="mdi-pencil" ></v-btn>
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
import { useRouter } from 'vue-router';
const router = useRouter()
const route = useRoute()

const post = ref(null);
const { post_id } = route.params;

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

const tagColors = {
  分享: 'green',
  求助: 'red',
  讨论: 'blue',
  精华: 'purple',
}

function getTagColor(tagName) {
  return tagColors[tagName] || tagColors['讨论']; 
}
onMounted(() => {
  fetchPost();
});
</script>

<style scoped>
/* 针对postDetails页面的特定样式 */
.v-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover; /* 保持图片的比例 */
}

.illustration {
  border-top-left-radius: 8px; /* 插画圆角 */
  border-bottom-left-radius: 8px; /* 插画圆角 */
}
</style>