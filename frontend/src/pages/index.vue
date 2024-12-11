<template>
  <v-container fluid class="home-container">
    <v-container class="content">
    <v-col>
    <!-- 标题 -->
    <v-row justify="center" class="mb-5">
      <v-col cols="12" md="8" class="text-center">
        <h1 class="display-2 font-weight-bold mb-4">猫猫欢迎你！</h1>
        <p class="headline font-weight-regular">北航所有的猫猫，都在这里！</p>
      </v-col>
    </v-row>

    <!-- 图片和公告栏区域 -->
    <v-row justify="center" class="mb-5" align="center">
      <!-- 图片区域 -->
      <v-col cols="8" md="6" class="pa-0">
        <v-img src="@/assets/kitten.png" class="kitten-logo" />
      </v-col>

      <!-- 公告栏区域 -->
      <v-col cols="8" md="6">
        <v-row>
          <!-- 第一个公告栏 -->
          <v-col cols="12" class="pa-2">
            <v-card class="elevation-10 pa-4 announcement-card">
              <v-card-title class="headline">公告栏</v-card-title>
              <v-card-text>
                <p>这里是最新的平台公告和更新信息。请定期查看以获取最新动态。</p>
              </v-card-text>
            </v-card>
          </v-col>
          <!-- 第二个公告栏 -->
          <v-col cols="12" class="pa-2">
            <v-card class="elevation-10 pa-4 announcement-card">
              <v-card-title class="headline">小贴士</v-card-title>
              <v-card-text>
                <p>了解如何与猫咪互动，发现新功能，以及如何充分利用我们的平台。</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    </v-col>
  </v-container>
  </v-container>
</template>

<script setup>

</script>

<style scoped>
.content {
  max-width: 80%; /* 设置容器宽度为屏幕宽度的一半 */
  margin: auto; /* 水平居中 */
  padding: 24px; /* 根据需要设置内边距 */
  height: 100%; /* 设置容器高度为100% */
}
.title {
  text-align: center;
  margin-top: 50px;
  color: #ffffff;
}

.announcement-card {
  height: 500px; /* 调整公告栏的高度 */
}

.kitten-logo {
  height: 500px; /* 调整图片的高度 */
  object-fit: cover; /* 保持图片的宽高比 */
}
.home-container {
  background-color: #d4eae0;
  background: linear-gradient(135deg, #d4eae0, #c7d9e9);
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;

}


h1.display-2 {
  font-size: 60px;
  color: #3b3b3b; /* Golden color for the title */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* Strong shadow for readability */
}

p.headline {
  font-size: 30px;
  color: #3b3b3b; /* White color for subtitle */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* Strong shadow for readability */
}

.v-card {
  background-color: rgba(255, 255, 255, 0.85); /* Slightly more opaque background for readability */
  border-radius: 8px; /* Rounded corners for the cards */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
  margin-top: 12px; /* Spacing between cards */
  height: auto; /* Adjust the height as needed */
}

.v-card-title.headline {
  color: #3b3b3b; /* Darker color for the card title for contrast */
}

.v-card-text {
  color: #4a4a4a; /* Slightly softer text color */
}

</style>
