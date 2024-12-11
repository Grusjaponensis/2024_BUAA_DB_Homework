<template>
  <v-container>
    <v-btn color="#bdd4eb" text @click="$router.push('/ForumCenter/forumCenter')"><v-icon left>mdi-arrow-left</v-icon> 返回 </v-btn>
    <v-card class="elevation-12 mt-5">
      <v-card-title class="headline">创建帖子</v-card-title>
      <v-card-text>
        <v-form ref="form" lazy-validation>
          <v-text-field
            v-model="post.title"
            label="标题"
            counter="100"
            required
          ></v-text-field>

          <v-textarea
            v-model="post.content"
            label="内容"
            counter="1000"
            required
          ></v-textarea>
          
        <v-col>
          <v-row >
            <v-col cols="12">
              <v-btn text @click="showTags = !showTags">添加标签</v-btn>
            </v-col>
            <v-col cols="12" v-if="showTags">
              <v-select
                v-model="post.tags"
                :items="allTags.map(tag => tag.name)"
                multiple
                chips
                label="Tags"
              ></v-select>
            </v-col>
          </v-row>
          <!-- 上传文件按钮 -->
          <v-row class="mt-5">
            <input type="file" multiple @change="handleFileUpload" />
          </v-row>

          <!-- 发帖按钮靠右 -->
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
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { createPost } from '@/api/post';
import { getTags } from '@/api/tags';
import { useRouter } from 'vue-router';
import snackbar from '@/api/snackbar';

const router = useRouter();
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
      snackbar.success('帖子提交成功');
      router.push('/ForumCenter/forumCenter'); 
    } catch (error) {
      console.error('发帖失败:', error);
      snackbar.error('发帖失败');
    }
  }
};

const allTags = ref([]);
const showTags = ref(false);

const fetchTags = async () => {
  const data = await getTags();
  allTags.value = data;
  console.log('所有标签', allTags.value);
};

watchEffect(() => {
  if (showTags.value) {
    fetchTags();
  }
});
</script>

<style scoped>
/* 针对createPost页面的特定样式 */
</style>
