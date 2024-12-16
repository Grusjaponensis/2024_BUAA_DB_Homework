<template>
  <div class="cat-details">
    <v-container>
    
    <v-row text-align="center">
      <!-- 插画 -->
      <v-btn 
        color="#bdd4eb" 
        @click="$router.push('/cats/catBase')" 
        prepend-icon="mdi-arrow-left"
        text="返回"
        class="mb-3"
        style="position: fixed; bottom: 24px; left: 36px;;"
      >
      </v-btn>
      <v-col cols="12" md="4" class="pa-0">
        <v-img
          src="@/assets/cat-detail.png"
          class="illustration"
          contain
          max-width="100%"
          max-height="100%"
        ></v-img>
      </v-col>

      <!-- 内容 -->
      <v-col cols="12" md="8" v-if="loaded">
        <v-card class="pa-3 rounded-lg elevation-4">
        <v-row>
          <v-card-text v-if="cat.image_urls && cat.image_urls.length > 0">
            <v-carousel hide-delimiters="true" show-arrows="hover" style = "max-width: 500px; height: 300px; margin: 0 auto;">
              <v-carousel-item 
                v-for="(image, index) in cat.image_urls"
                :key = index
                :src = "`${addPrefix(image)}`"
                rounded="lg"
                cover
              ></v-carousel-item>
            </v-carousel>
          </v-card-text>
          <v-col>
            <v-card-title class="text-h5 font-weight-bold">{{ cat.name }}</v-card-title>
            <v-card-text>
              <v-col>
                <v-row cols="12" class="mb-2">
                  <div class="field">
                    <v-icon class="mr-2" color="deep-purple-darken-1">mdi-calendar-check</v-icon>
                    <span class="text-body-1">年龄: {{ cat.age }}</span>
                  </div>
                </v-row>
                <v-row cols="12" class="mb-2">
                  <div class="field">
                    <v-icon class="mr-2" color="red-darken-1">mdi-gender-male-female</v-icon>
                    <span class="text-body-1">性别: {{ cat.is_male ? '男' : '女' }}</span>
                  </div>
                </v-row>
                <v-row cols="12" class="mb-2">
                  <div class="field">
                    <v-icon class="mr-2"  color="pink-darken-1">mdi-heart-pulse</v-icon>
                    <span class="text-body-1">健康状况: 
                      {{ cat.health_condition == 1 ? "健康" 
                      : cat.health_condition == 2 ? "生病" 
                      : cat.health_condition == 3 ? "残疾" 
                      : "去喵星"}}</span>
                  </div>
                </v-row>
                <v-row>
                  <div class="field">
                    <v-icon class="mr-2"  color="purple-darken-1">mdi-pencil</v-icon>
                    <span class="text-body-1">描述: {{ cat.description }}</span>
                  </div>
                </v-row>
              </v-col>
            </v-card-text>
          </v-col>
        </v-row>
        <v-divider class="my-4"></v-divider>
        <v-card-subtitle class="text-h6 font-weight-bold">最近一次出没地点:</v-card-subtitle>
        <v-container class="pa-6">
          <MapContainer 
          :center="[cat.latest_longitude, cat.latest_latitude]"
          :zoom="16.5"
          :markerPosition="[cat.latest_longitude, cat.latest_latitude]"
          :markerTitle="cat.name"
          style = "width: 100%; height: 500px;"
          ></MapContainer>
        </v-container>
        <v-text-field>
          经纬度信息: {{ cat.latest_longitude }}, {{ cat.latest_latitude }}
        </v-text-field>
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
  import MapContainer from '@/map/MapContainer.vue';
  
  const route = useRoute();
  const cat = ref(null);
  const loaded = ref(false);
    
  const fetchCat = async () => {
    try {
      const response = await getCat(route.params.cat_id);
      console.log(response);
      cat.value = response;
      loaded.value = true;
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

.cat-info p{
  margin: 0
}
</style>