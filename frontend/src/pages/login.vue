<template>
    <v-snackbar v-model="snackbar" color="snackbarColor" timeout="3000">
        {{ snackbarText }}
    </v-snackbar>

    <div class="login-container">
        <v-card class="login-card" elevation="8">
            <v-card-title class="title">
                登录
            </v-card-title>
            <v-card-title>
                <v-form>
                    <v-text-field
                        v-model="username"
                        label="用户名"
                        outlined
                        dense
                        prepend-inner-icon="mdi-account">
                    </v-text-field>

                    <v-text-field
                        v-model="password"
                        label="密码"
                        type="password"
                        outlined
                        dense
                        prepend-inner-icon="mdi-lock">
                    </v-text-field>
                </v-form>
            </v-card-title>
            <v-card-actions class="actions">
                <v-btn color="primary" size="large" block @click="submitLogin">
                    登录
                </v-btn>
                <v-btn color="secondary" size="large" block to="/signup">
                    注册
                </v-btn>
                <v-btn color="error" size="large" block to="/">
                    返回首页
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>

    <!-- <v-btn @click="test">test</v-btn> -->

</template>

<script setup>
import { getPosts } from '@/api/post';
import server from '@/api/server';
import { login } from '@/api/user';
import {useUserStore} from '@/stores/user';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('')
const password = ref('')
const router = useRouter()
const snackbar = ref(false)
const snackbarText = ref('')
const userStore = useUserStore()
const snackbarColor = ref('success')

const submitLogin = async () => {
    try {
        await login(username.value, password.value);
        snackbar.value = true;
        snackbarText.value = '登录成功';
        snackbarColor.value = 'success';
        userStore.login(username.value)
        router.push({ path: '/home', query: { loggedIn: true } });
    } catch (error) {
        console.error('登录失败', error);
        snackbarColor.value = 'error';
        snackbarText.value = '登录失败，请检查用户名或密码';
        snackbar.value = true;
    }
}

// onMounted(() => {
//     if (router.query.Signup) {
//       snackbarText.value = '登录成功'
//       snackbar.value = true
//     }
//   }) 

const test = () => {
    // const res = server.get('/posts/');
    const res = server.get('/posts/my');
    console.log(res);
}

</script>

<style scoped>
    .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #7874eb, #c1ace5);
    padding: 16px;
    }

    .login-card {
    width: 100%;
    max-width: 500px;
    border-radius: 16px;
    overflow: hidden;
    }

    .title {
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: #dfd5d5;
    margin-bottom: 8px;
    }

    .actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
    }
</style>