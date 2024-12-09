<template>
    <v-container>
      <v-card v-if="cat">
        <v-card-title class="headline">{{ cat.name }}</v-card-title>
        <v-card-subtitle>年龄: {{ cat.age }}</v-card-subtitle>
        <v-card-subtitle>性别: {{ cat.is_male ? '男' : '女' }}</v-card-subtitle>
        <v-card-subtitle>健康状况: {{ cat.health_condition }}/4</v-card-subtitle>
        <v-card-subtitle>最近一次出没地点: {{ cat.latest_longitude }}, {{ cat.latest_latitude }}</v-card-subtitle>
        <v-card-text>
          描述： {{ cat.description }}
        </v-card-text>
        <!-- 图片 -->
        <v-card-text v-if="cat.images && cat.images.length > 0">
          <v-img
            v-for="(image, index) in cat.images"
            :key="index"
            :src="image"
            class="mb-3"
            max-width="100%"
            max-height="300px"
          ></v-img>
        </v-card-text>
      </v-card>

    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { getCat } from '@/api/cat';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  
  const cat = ref(null);
  
  const { cat_id } = route.params;
  
  const fetchCat = async () => {
    try {
      const response = await getCat(route.params.cat_id);
      console.log(response);
      cat.value = response;
    } catch (error) {
      console.error('获取猫咪详情失败:', error);
    }
  };
  
  onMounted(() => {
    fetchCat();
  });
  </script>
  
  <style scoped>
  /* 针对catDetails页面的特定样式 */
  .v-img {
    max-width: 100%;
    max-height: 300px;
    object-fit: cover; /* 保持图片的比例 */
  }
  </style>