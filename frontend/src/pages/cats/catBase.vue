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
        <v-card class="d-flex flex-column">
        <!-- <v-card lass="d-flex flex-column"> -->
          <v-img
            src="https://placekitten.com/200/300"
            height="200px"
            class="mx-auto"
          ></v-img>
          <v-card-title class="headline" @click="goToCatDetails(cat.id)">{{ cat.name }}</v-card-title>
          <v-card-subtitle @click="goToCatDetails(cat.id)">年龄: {{ cat.age }}</v-card-subtitle>
          <v-card-subtitle @click="goToCatDetails(cat.id)">性别: {{ cat.is_male ? '男' : '女' }}</v-card-subtitle>
          <v-card-subtitle @click="goToCatDetails(cat.id)">描述: {{ cat.description }}</v-card-subtitle>
          <v-card-subtitle @click="goToCatDetails(cat.id)">健康状况: {{ cat.health_condition  == 1 ? "HEALTHY" : cat.health_condition == 2 ? "SICK" : cat.health_condition == 3 ? "VACCINATED" : "DEAD"}}</v-card-subtitle>
          <!-- <v-card-subtitle>收到投喂: {{ cat.cans }}</v-card-subtitle> -->
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
            <v-btn icon @click="removeCat(cat)" v-if="isAdmin">
                <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-footer padless v-if="isAdmin && user.login">
    <v-row justify="end" no-gutters >
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
import { getProfile } from '@/api/user';
import { getCats,deleteCat } from '@/api/cat';
import { user } from '@/api/user';
import snackbar from '@/api/snackbar';

const cats = ref([]);
const isAdmin = ref(false);
const router = useRouter();
const remainingCans = ref(6);

const fetchProfile = async () => {
  try {
    const response = await getProfile();
    isAdmin.value = response.data.is_superuser;
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
};
const fetchCats = async () => {
  try {
    const response = await getCats();
    cats.value = response.cats;
  } catch (error) {
    console.error('获取猫咪列表失败:', error);
  }
};
const removeCat = async (cat) => {
  try {
    const response = await deleteCat(cat.id);
    snackbar.success('删除成功！');
    cats.value = cats.value.filter((c) => c.id !== cat.id);
    fetchCats();
  } catch (error) {
    console.error('删除失败:', error);
  }
};
const goToCatDetails = (id) => {
  router.push(`/cats/${id}`);
};

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
  fetchProfile();
  fetchCats();
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
