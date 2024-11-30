<template>
    <v-container>
      <v-card>
        <v-card-title>{{ post.title }}</v-card-title>
        <v-card-subtitle>发布人: {{ post.user.name }}</v-card-subtitle>
        <v-card-subtitle>标签: {{ post.label }}</v-card-subtitle>
        <v-card-text>{{ post.content }}</v-card-text>
        <v-card-actions>
          <v-btn icon @click="toggleFavorite">
            <v-icon>{{ post.isFavorited ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
  
      <v-divider class="my-4"></v-divider>
  
      <v-card>
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
      </v-card>
  
      <v-card>
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
      </v-card>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        post: {
          title: '',
          user: {},
          label: '',
          content: '',
          isFavorited: false,
          comments: [],
        },
        newComment: '',
      };
    },
    methods: {
      toggleFavorite() {
        // 切换收藏状态
        axios.post(`/api/v1/posts/${this.$route.params.postId}/favorite`)
          .then(response => {
            this.post.isFavorited = response.data.isFavorited;
          })
          .catch(error => {
            console.error('切换收藏状态失败:', error);
          });
      },
      addComment() {
        // 添加评论
        axios.post(`/api/v1/posts/${this.$route.params.postId}/comments`, {
          content: this.newComment,
        })
          .then(response => {
            this.post.comments.push(response.data);
            this.newComment = '';
          })
          .catch(error => {
            console.error('添加评论失败:', error);
          });
      },
      fetchPost() {
        // 获取帖子详情
        axios.get(`/api/v1/posts/${this.$route.params.postId}`)
          .then(response => {
            this.post = response.data;
          })
          .catch(error => {
            console.error('获取帖子详情失败:', error);
          });
      },
    },
    created() {
      this.fetchPost(); // 创建时获取帖子详情
    },
  };
  </script>
  
  <style scoped>
  /* 针对postDetails页面的特定样式 */
  </style>