<template>
  <h1 class = "title">北航猫咪管理系统</h1>
  <v-btn to="/login" v-if="!isLoggedIn">Login</v-btn>
</template>

<script setup>
  import { useUserStore } from '../stores/user';
  const userStore = useUserStore();
  const isLoggedIn = computed(() => userStore.isLoggedIn);
  //
</script>

<style scoped>
.title {
  text-align: center;
  margin-top: 50px;
  color: #ffffff;
}
</style>