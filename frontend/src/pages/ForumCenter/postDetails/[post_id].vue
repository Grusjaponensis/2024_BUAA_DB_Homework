<template>
  <v-container>
    
      <v-row align="center">
        <!-- 插画 -->
        <v-col cols="12" md="4" class="pa-0" align="center">
          <v-img
            src="@/assets/detail.png" 
            class="illustration"
            contain
            max-width="100%"
            max-height="100%"
          ></v-img>
        </v-col>

        <!-- 帖子内容 -->
        <v-col cols="12" md="4" >
          <v-btn color="#bdd4eb" text @click="$router.push('/ForumCenter/forumCenter')" class="mb-3"><v-icon left>mdi-arrow-left</v-icon> 返回 </v-btn>
          
          
          <v-card
            v-if="post"
            class="post-card"
            color="#f0f0f0"
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
          <v-card-subtitle class="text-right">发布时间: {{ post.created_at }}</v-card-subtitle>
          <v-card-actions class="row justify-end">
            <v-btn icon @click="toggleFavorite">
              <v-icon>{{ post.like_status ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
        </v-col>
      </v-row>


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

.post-card {
  display: flex;
  flex-direction: column;
  width: 400px;
}

.illustration {
  border-top-left-radius: 8px; /* 插画圆角 */
  border-bottom-left-radius: 8px; /* 插画圆角 */
}
.v-tag-btn {
  border-radius: 25%; 
  width: 40px; 
  height: 40px; 
  margin-right: 12px;
}
</style>