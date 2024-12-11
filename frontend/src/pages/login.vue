<template>
    <div class="login-container">
        <v-card class="login-card" elevation="8">
            <v-card-title class="title">
                登录
            </v-card-title>
            <v-card-title>
                <v-form>
                    <v-text-field
                        v-model="email"
                        label="邮箱"
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
            <v-card-actions class="actions" justify="center">
                <v-btn color="primary" size="large" block @click="submitLogin">
                    登录
                </v-btn>
            </v-card-actions>
            <v-card-actions class="actions" justify="center">
                <v-btn color="secondary" size="large" block to="/signup">
                    注册
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>

    <!-- <v-btn @click="test">test</v-btn> -->

</template>

<script setup>
import server from '@/api/server';
import { login } from '@/api/user';
import { ref } from 'vue';
import { useRouter } from 'vue-router'
import { user } from '../api/user';
import snackbar from '../api/snackbar';

const router = useRouter();
const email = ref('')
const password = ref('')
const submitLogin = async () => {
    if (email.value.trim() === '') {
        snackbar.error('邮箱不能为空')
        return
    }
    if (password.value.trim() === '') {
        snackbar.error('密码不能为空')
        return
    }
    try {
        await login(email.value, password.value)
        console.log("登录成功 " + user.login)
        router.push('/')
    } catch (error) {
        console.error('登录失败', error);
    }
}

const test = () => {
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
    background: linear-gradient(135deg, #d4eae0, #dcd5f2);
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
    color: #629a90;
    margin-bottom: 8px;
    }

    .actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    }
</style>