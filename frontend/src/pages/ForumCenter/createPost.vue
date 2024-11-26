<template>
  <v-container>
    <v-card>
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

          <!-- 其他基本字段 -->
          <v-select
            v-model="post.label"
            :items="labels"
            label="标签"
            required
          ></v-select>

          <!-- 提交按钮 -->
          <v-btn
            color="primary"
            :disabled="!isFormValid"
            @click="submitPost"
          >
            发帖
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      post: {
        title: '',
        content: '',
         label: null,
      },
       labels: ['求助', '分享', '讨论'], // 标签类别
    };
  },
  computed: {
    isFormValid() {
      // 表单验证逻辑
      return this.post.title.trim() !== '' && this.post.content.trim() !== '';
    },
  },
  methods: {
    submitPost() {
      if (this.$refs.form.validate()) {
        // 提交逻辑
        console.log('提交', this.post);
        
        axios.post('/api/posts', {
          title: this.post.title,
          content: this.post.content,
          label: this.post.label,
        })
        .then(response => {
          // 处理响应
          console.log('帖子提交成功:', response.data);
          this.$router.push('/forum-center'); // 跳转回论坛中心
        })
        .catch(error => {
          // 处理错误
          console.error('发帖失败:', error);
        });
      }
    },
  },
};
</script>

<style scoped>
/* 针对createPost页面的特定样式 */
</style>