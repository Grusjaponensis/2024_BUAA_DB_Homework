<template>
    <div class="login-container">
        <v-card class="login-card" elevation="8">
            <v-card-title class="title">
                注册
            </v-card-title>
            <v-card-text>
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

                    <v-text-field
                        v-model="passwordConfirm"
                        label="确认密码"
                        type="password"
                        outlined
                        dense
                        prepend-inner-icon="mdi-lock-alert"
                    >
                    </v-text-field>

                    <v-text-field
                        v-model="nickname"
                        label="昵称"
                        outlined
                        dense
                        prepend-inner-icon="mdi-account-edit">
                    </v-text-field>
                </v-form>
            </v-card-text>
            <v-card-actions class="actions">
                <v-btn color="secondary" size="large" block @click="submitSignup">
                    注册
                </v-btn>
                <v-btn color="primary" size="large" block to="/login">
                    返回登录
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { signup } from '../api/user';
import { useRouter } from 'vue-router';
import snackbar from '../api/snackbar'

const email = ref('')
const password = ref('')
const nickname = ref('')
const passwordConfirm = ref('')
const router = useRouter()

const submitSignup = async () => {
    if (email.value.trim() === '') {
        snackbar.error('邮箱不能为空')
        return
    }
    if (email.value.indexOf('@') === -1 || email.value.indexOf('.') === -1) {
        snackbar.error('邮箱格式不正确')
        return
    }
    if (password.value.trim() === '') {
        snackbar.error('密码不能为空')
        return
    }
    if (password.value.length < 8) {
        snackbar.error('密码长度必须大于等于8')
        return
    }
    if (password.value !== passwordConfirm.value) {
        snackbar.error('两次密码输入不一致')
        return
    }
    try {
        await signup(email.value, password.value , nickname.value);
        router.push('/login');
    } catch (error) {
        console.error('注册失败', error);
    }
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