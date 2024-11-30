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

<router-link to="/signup">
    <v-btn>Sign up</v-btn>
</router-link>

<router-link to="/">
    <v-btn>Backhome</v-btn> 
</router-link>

</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('')
const password = ref('')
const router = useRouter()

const submitLogin = async () => {
  //  try {
        const server = axios.create({
            withCredentials: true
        })

        const formData = new FormData()
        formData.append('username',username.value)
        formData.append('password',password.value)
        console.log('formData', formData);
        const res = await server.post(
            '/api/v1/login/access-token', 
            {username: username.value, password: password.value}, 
            { headers: { 'Content-Type': 'multipart/form-data' } }
        )

        console.log('res.data', res.data)
        
 /*       if (res.data.access_token) {
            localStorage.setItem('access_token', res.data.access_token)
            router.push('/homepage')
        } else {
            alert('Login failed: No access token received')
        }
    } catch (error) {
        console.error('Login failed : ', error)
        alert('Login failed: ' + (error.response?.data?.detail || error.message))
    }
        */
}

</script>