<template>
  <v-container>
    <v-card>
      <v-card-title class="headline">{{ post.title }}</v-card-title>
      <v-card-subtitle>发布时间: {{ post.created_at }}</v-card-subtitle>
      <v-card-subtitle>标签: {{ post.tags.join(', ') }}</v-card-subtitle>
      <v-card-text style="margin: auto;">{{ post.content }}</v-card-text>
      <v-card-actions>
        <v-btn icon @click="toggleFavorite">
          <v-icon>{{ post.like_status ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-divider class="my-4"></v-divider>

    <!-- <v-card>
      <v-card-title>评论</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item v-for="comment in post.comments" :key="comment.id">
            <v-list-item-content>
              <v-list-item-title>{{ comment.content }}</v-list-item-title>
              <v-list-item-subtitle>{{ comment.user.name }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card> -->

    <!-- <v-card>
      <v-card-text>
        <v-textarea
          v-model="newComment"
          label="添加评论"
          @keyup.enter="addComment"
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="addComment">发表评论</v-btn>
      </v-card-actions>
    </v-card> -->
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getPost, likePost, unlikePost } from '@/api/post';

const route = useRoute();
const post = ref({});

const fetchPost = async () => {
  try {
    const response = await getPost(route.params.postId);
    post.value = response.data;
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

// const addComment = async () => {
//   if (newComment.value.trim()) {
//     try {
//       const response = await addComment(post.value.id, { content: newComment.value });
//       post.value.comments.push(response.data);
//       newComment.value = '';
//     } catch (error) {
//       console.error('添加评论失败:', error);
//     }
//   }
// };

onMounted(() => {
  fetchPost();
});
</script>

<style scoped>
/* 针对postDetails页面的特定样式 */
</style>