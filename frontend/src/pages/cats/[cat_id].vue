<template>
  <div class="cat-details">
    <v-container>
    
    <v-row align="center">
      <!-- 插画 -->
      <v-col cols="12" md="4" class="pa-0" align="center">
        <v-img
          src="@/assets/cat-detail.png"
          class="illustration"
          contain
          max-width="100%"
          max-height="100%"
        ></v-img>
      </v-col>

      <!-- 内容 -->
      <v-col cols="12" md="8" >
        <v-btn color="#bdd4eb" text @click="$router.push('/cats/catBase')" class="mb-3"><v-icon left>mdi-arrow-left</v-icon> 返回 </v-btn>
        
        
        <v-card v-if="cat" class="mx-auto">
          <v-card-title class="headline">{{ cat.name }}</v-card-title>
          <v-card-subtitle>年龄: {{ cat.age }}</v-card-subtitle>
          <v-card-subtitle>性别: {{ cat.is_male ? '男' : '女' }}</v-card-subtitle>
          <v-card-subtitle>健康状况: {{ cat.health_condition == 1 ? "HEALTHY" : cat.health_condition == 2 ? "SICK" : cat.health_condition == 3 ? "VACCINATED" : "DEAD"}}</v-card-subtitle>
          <v-card-subtitle>最近一次出没地点: {{ cat.latest_longitude }}, {{ cat.latest_latitude }}</v-card-subtitle>
          <v-card-text>
            描述： {{ cat.description }}
          </v-card-text>
          <!-- 图片 -->
          <v-card-text v-if="cat.image_urls && cat.image_urls.length > 0">
            <v-img
              v-for="(image, index) in cat.image_urls"
              :key="index"
              :src = "`${addPrefix(image)}`"
              class="mb-3"
              max-width="100%"
              max-height="300px"
            ></v-img>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>


  <v-divider class="my-4"></v-divider>
</v-container>
</div>
</template>

  <script setup>
  import { ref, onMounted } from 'vue';
  import { getCat } from '@/api/cat';
  import { useRoute } from 'vue-router';
  import { addPrefix } from '@/api/post';
  
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
    max-height: 100%;
    object-fit: cover; /* 保持图片的比例 */
  }
  .illustration {
  border-radius: 8px; /* 插画圆角 */
}
.cat-details {
  padding: 20px;
  background-color: #f0f0f0;
  height: 100%;
  width: 100%;
}
  </style>