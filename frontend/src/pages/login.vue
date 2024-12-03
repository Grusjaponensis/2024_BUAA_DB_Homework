<template>

    <h1>login</h1>

    <v-text-field 
        v-model="username" 
        label="username">
    </v-text-field>

    <v-text-field 
        v-model="password" 
        label="password"
        type="password">
    </v-text-field>

    <v-btn @click="submitLogin">
        submitLogin
    </v-btn>

    <v-btn to="/signup">Sign up</v-btn>

    <v-btn to="/">Backhome</v-btn> 

    <v-btn @click="test">test</v-btn>

</template>

<script setup>
import { getPosts } from '@/api/post';
import server from '@/api/server';
import { login } from '@/api/user';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('')
const password = ref('')
const router = useRouter()

const submitLogin = async () => {
    await login(username.value, password.value);
}

const test = () => {
    // const res = server.get('/posts/');
    const res = server.get('/posts/my');
    console.log(res);
}

</script>