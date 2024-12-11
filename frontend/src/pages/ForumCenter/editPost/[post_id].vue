<template>
    <v-container>
      <v-btn color="#bdd4eb" text @click="$router.push('/ForumCenter/myPosts')"><v-icon left>mdi-arrow-left</v-icon> 返回 </v-btn>
      <v-card class="elevation-12 mt-5">
        <v-card-title class="headline">编辑帖子</v-card-title>
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <v-text-field
              v-model="post.title"
              label="标题"
              counter="100"
              required
            ></v-text-field>

            <!-- <v-textarea
              v-model="post.content"
              label="内容"
              counter="1000"
              required
            ></v-textarea> -->

            <v-md-editor
              v-model="post.content" 
              height="400px"
              left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | code | link table"
            />

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
                <div v-if="post.keep_images && post.keep_images.length > 0"  style="margin: auto; ">
                  <v-img
                  v-for="(image, index) in post.keep_images"
                  :key="index"
                  :src="`${addPrefix(image)}`"
                  class="mb-3"
                  max-width="100%"
                  max-height="300px"
                  ></v-img>
                  <v-btn
                  v-for="(image, index) in post.keep_images"
                  :key="index"
                  color="error"
                  text
                  @click="removeImage(image)"
                  >
                  删除图片
                  </v-btn>
              </div>
              </v-row>
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
                更新帖子
                </v-btn>
              </v-row>
            </v-col>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { getPost, updatePost, addPrefix } from '@/api/post';
  import { getTags } from '@/api/tags';
  import { useRouter } from 'vue-router';
  import { useRoute } from 'vue-router';
  import snackbar from '@/api/snackbar';

  const route = useRoute()
  const router = useRouter();
  const post = ref({
    title: '',
    content: '',
    tags: [],
    keep_images: [],
    upload_images: [],
  });
  const isFormValid = computed(() => post.value.title.trim() !== '' && post.value.content.trim() !== '');
  const allTags = ref([]);
  const showTags = ref(false);
  // 获取帖子详情
  const fetchPost = async () => {
    try {
      const response = await getPost(route.params.post_id);
      post.value.title = response.title;
      post.value.content = response.content;
      post.value.tags = response.tags;
      post.value.keep_images = response.images;
      post.value.upload_images = [];
      post.value.id = response.id;
      console.log('帖子详情获取成功', response.data);
    } catch (error) {
      console.error('获取帖子详情失败:', error);
    }
  };
  
  // 处理文件上传
  const handleFileUpload = (event) => {
    const files = event.target.files;
    if (files) {
      post.value.upload_images = Array.from(files);
    }
  };
  
  // 提交帖子
  const submitPost = async () => {
    if (isFormValid.value) {
        try {
          const formData = new FormData();
          formData.append('title', post.value.title);
          formData.append('content', post.value.content);
          formData.append('tags', post.value.tags);
          if (post.value.keep_images.length > 0) {
            post.value.images.forEach((image, index) => {
              formData.append(`keep_images`, image);
            });
          }
          if (post.value.upload_images.length > 0) {
            post.value.upload_images.forEach((image, index) => {
              formData.append(`upload_images`, image);
            });
          }
          console.log('formData', formData.get('content'));
          const response = await updatePost(post.value.id, formData);
          console.log('帖子更新成功', response);
          snackbar.success('帖子更新成功');
          router.push('/ForumCenter/myPosts');
        } catch (error) {
          console.error('更新帖子失败:', error);
          snackbar.error('更新帖子失败');
        }
    }
    };
  // 删除图片
  const removeImage = (image) => {
    const index = post.value.keep_images.indexOf(image);
    if (index !== -1) {
      post.value.keep_images.splice(index, 1);
    }
  };
  // 获取标签
  const fetchTags = async () => {
    const data = await getTags();
    allTags.value = data;
  };
  
  // 组件挂载时获取帖子详情和标签
  onMounted(async () => {
    fetchPost();
    fetchTags();
  });
  </script>
  
  <style scoped>
  /* 针对editPost页面的特定样式 */
  </style>