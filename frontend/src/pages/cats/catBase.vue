<template>
  <v-container>
    <v-container>
      <v-chip-group absolute top left v-if="user.login">
        <v-chip>
          剩余罐罐: {{ remainingCans }}
        </v-chip>
      </v-chip-group>
      <v-row>
        <v-col cols="12" md="4" v-for="cat in cats" :key="cat.id">
          <!-- <v-card @click="goToCatDetails(cat.id)" class="d-flex flex-column"> -->
          <v-card lass="d-flex flex-column">
            <v-img
              src="https://placekitten.com/200/300"
              height="200px"
              class="mx-auto"
            ></v-img>
            <v-card-title class="headline">{{ cat.name }}</v-card-title>
            <v-card-subtitle>年龄: {{ cat.age }}</v-card-subtitle>
            <v-card-subtitle>品种: {{ cat.breed }}</v-card-subtitle>
            <v-card-subtitle>性格: {{ cat.temperament }}</v-card-subtitle>
            <v-card-subtitle>收到投喂: {{ cat.cans }}</v-card-subtitle>
            <v-card-text>
              <v-btn
                text
                color="primary"
                class="feed-button"
                @click="feedCat(cat)"
              >
                <v-icon left>mdi-paw</v-icon>
                投喂
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-footer padless v-if="user.login">
      <v-row justify="end" no-gutters>
        <v-btn
          fab
          dark
          fixed
          bottom
          right
          color="primary"
          to="/cats/addCat"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </v-footer>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { user } from '@/api/user';
import snackbar from '@/api/snackbar';

const cats = ref([]);
const isAdmin = ref(true);
const router = useRouter();
const remainingCans = ref(6);

// 模拟数据
const catsData = {
  data: [
    {
      id: 1,
      name: 'Kitty',
      age: 3,
      breed: 'Persian',
      temperament: 'Playful',
      cans: 5,
    },
    {
      id: 2,
      name: 'Fluffy',
      age: 2,
      breed: 'Maine Coon',
      temperament: 'Docile',
      cans: 7,
    },
    {
      id: 3,
      name: 'Whiskers',
      age: 1,
      breed: 'Bengal',
      temperament: 'Independent',
      cans: 4,
    },
  ],
};

cats.value = catsData.data;
// const fetchCats = async () => {
//   try {
//     const response = await getCats();
//     cats.value = response.data;
//   } catch (error) {
//     console.error('获取猫咪列表失败:', error);
//   }
// };
// const goToCatDetails = (id) => {
//   router.push(`/cats/${id}`);
// };

const feedCat = (cat) => {
  if (!user.login) {
    snackbar.warning('请先登录！')
    return;
  }
  if (remainingCans.value > 0) {
    remainingCans.value--;
    cat.cans++;
  } else {
    alert('已达每日投喂上限！');
  }
};

onMounted(() => {

});
</script>

<style scoped>
/* 针对 catBase 页面的特定样式 */
.feed-button {
  margin: 4px;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  text-transform: none;
  font-weight: 500;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.feed-button:hover {
  background-color: rgba(0, 0, 0, 0.04);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.24);
}

</style>
