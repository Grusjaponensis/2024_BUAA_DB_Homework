<template>
<h1>login</h1>
<p>{{  username }}</p>
<p>{{  password }}</p>
<v-text-field v-model="username" label="username"></v-text-field>
<v-text-field v-model="password" label="password"></v-text-field>

<v-btn @click="submitLogin">Login</v-btn>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
const username = ref('')
const password = ref('')

const submitLogin = async () => {
    const server = axios.create({
        withCredentials: true
    })
    try {
        const res = await server.post('/api/v1/login/access-token', {
            username: username.value,
            password: password.value,
        }, { headers: { 'Content-Type': 'multipart/form-data' } })
        console.log(res);
        // set cookie access_token
        const access_token = res.data.access_token
        document.cookie = `access_token=${access_token};path=/`
    } catch (error) {
        console.error("NIMASILE" , error)
    }
}

</script>