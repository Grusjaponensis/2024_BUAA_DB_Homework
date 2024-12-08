<template>
  <v-snackbar v-model="snackbar" color="success" timeout="3000">
    {{ snackbarText }}
  </v-snackbar>
  <v-container fluid class="home-container">
    <v-row justify="center" class="mb-8">
      <v-col cols="12" md="6" class="text-center">
        <!-- <img src="kitten-logo.png" alt="Kitten Logo" class="kitten-logo" /> -->
        <h1 class="display-2 font-weight-bold mb-4">猫猫欢迎你！</h1>
        <p class="headline font-weight-regular">北航所有的猫猫，都在这里！</p>
      </v-col>
    </v-row>

    <v-col class="mx-auto" justify="center">
      <v-row cols="12" md="6" class="mb-6">
        <v-card class="elevation-10">
          <v-card-title class="headline">公告栏</v-card-title>
          <v-card-text>
            <p>这里是最新的平台公告和更新信息。请定期查看以获取最新动态。</p>
          </v-card-text>
        </v-card>
      </v-row>
      <v-row cols="12" md="6" class="mb-6">
        <v-card class="elevation-10">
          <v-card-title class="headline">小贴士</v-card-title>
          <v-card-text>
            <p>了解如何与猫咪互动，发现新功能，以及如何充分利用我们的平台。</p>
          </v-card-text>
        </v-card>
      </v-row>
    </v-col>
  </v-container>
</template>
  
<script setup>
  import {ref , onMounted} from 'vue'
  import { useRouter } from 'vue-router'

  const snackbar = ref(false)
  const snackbarText = ref('')
  const router = useRouter()

  onMounted(() => {
    // if (router.query.loggedIn) {
    //   snackbarText.value = '登录成功'
    //   snackbar.value = true
    // }
  }) 
</script>

<style scoped>
.title {
  text-align: center;
  margin-top: 50px;
  color: #ffffff;
}
.home-container {
  background-image: url('your-background-image.jpg'); /* 设置背景图片 */
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.kitten-logo {
  width: 150px; /* 调整猫咪logo的大小 */
  height: auto;
  margin-bottom: 24px;
}

h1.display-2 {
  color: #ffffff; /* 标题颜色 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* 标题阴影 */
}

p.headline {
  color: #ffffff; /* 副标题颜色 */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* 副标题阴影 */
}

.v-card {
  background-color: rgba(255, 255, 255, 0.8); /* 卡片背景透明度 */
  border-radius: 8px; /* 卡片圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 卡片阴影 */
  margin-top: 24px; /* 卡片顶部间距 */
}

.v-card-title.headline {
  color: #000000; /* 卡片标题颜色 */
}

.v-card-text {
  color: #000000; /* 卡片文本颜色 */
}
</style>