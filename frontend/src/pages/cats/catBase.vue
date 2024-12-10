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
        <v-card class="d-flex flex-column text-center">
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
              rounded="lg"
              class="mr-2"
              variant="elevated"
              color = "blue-darken-3"
              @click="feedCat(cat)"
            >
              <v-icon left class = "mr - 1">mdi-paw</v-icon>投喂
            </v-btn>
            <v-btn 
              rounded="lg"
              @click="showDeleteDialog = true ; removeCatId = cat.id" 
              v-if="isAdmin" 
              class="ml-2" 
              variant="elevated"
              color="red darken-1">
              <v-icon left class = "mr-1">mdi-delete</v-icon>删除
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="showDeleteDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">
            确认删除
          </v-card-title>
          <v-card-text>
            确认要删除该猫咪吗？此操作不可恢复。
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click = "showDeleteDialog = false"> 取消</v-btn>
            <v-btn color="red" @click = "deleteCat(removeCatId)"> 确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-container>
  <v-footer padless v-if="isAdmin && user.login">
    <v-row justify="end" no-gutters >
      <v-btn
        fab
        dark
        fixed
        bottom
        right = "24px"
        color="indigo-darken-1"
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
const showDeleteDialog = ref(false);
const removeCatId = ref(null);

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