<template>
  <v-snackbar v-model="snackbar" color="success" timeout="3000">
    {{ snackbarText }}
  </v-snackbar>
  <v-container>
    <!-- 主内容 -->
    <v-main>
      <h1>欢迎来到首页</h1>
      <!-- 其他内容 -->
    </v-main>
  </v-container>
</template>
  
<script setup>
  import {ref , onMounted} from 'vue'
  import { useRouter } from 'vue-router'

  const snackbar = ref(false)
  const snackbarText = ref('')
  const router = useRouter()

  onMounted(() => {
    if (router.query.loggedIn) {
      snackbarText.value = '登录成功'
      snackbar.value = true
    }
  }) 
</script>