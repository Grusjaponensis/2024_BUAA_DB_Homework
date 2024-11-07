<template>
    <h1>cat {{ cat_id }}</h1>
</template>
<script setup>
import { useRoute } from 'vue-router';

const route = useRoute()

const { cat_id } = route.params

</script>