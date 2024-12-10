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
        color="primary"
        @click="showAddCatDialog = true"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-row>
  </v-footer>
  </v-container>

  <v-dialog 
    v-model="showAddCatDialog" 
    max-width="70vw"
    width="650px"
  >
    <v-toolbar title="加入猫咪大军">
      <v-btn icon="mdi-close" @click="showAddCatDialog = false"></v-btn>
    </v-toolbar>
    <v-card>
      <v-card-text>
        <v-form ref="form" @submit.prevent="submitForm">
          <v-text-field
            v-model="cat_in.name"
            label="猫咪姓名"
            required
          ></v-text-field>
          <v-select
            v-model="cat_in.is_male"
            :items="['公猫', '母猫']"
            label="猫咪性别"
          ></v-select>
          <v-text-field
            v-model="cat_in.age"
            type="number"
            label="猫咪年龄"
            required
            :rules="[rules.age]"
          ></v-text-field>
          <v-select
            v-model="cat_in.health_condition"
            :items="['HEALTHY', 'SICK', 'VACCINATED', 'DEAD']"
            label="猫咪健康状况"
          ></v-select>
          <v-file-input
            v-model="avatarFile"
            label="上传图片"
            accept="image/*"
            @click="AvatarUpload"
          ></v-file-input>
          <v-textarea
            v-model="cat_in.description"
            label="对猫咪的描述"
            counter="50"
            required
            outlined
            dense
          ></v-textarea>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!formIsValid"
            rounded
            class="mt-4"
            block
          >
            加入猫咪大军
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getProfile } from '@/api/user';
import { getCats,deleteCat, createCat } from '@/api/cat';
import { user } from '@/api/user';
import snackbar from '@/api/snackbar';

const cats = ref([]);
const isAdmin = ref(false);
const router = useRouter();
const remainingCans = ref(6);

const cat_in = ref({
  name: '',
  is_male: null,
  age: null,
  health_condition: null,
  description: '',
});

const avatarFile = ref(null);
const showAddCatDialog = ref(false);

const rules = {
  age: value => {
    return value > 0 ? true : '年龄必须为正整数';
  }
};

const formIsValid = computed(() => {
  return (
    cat_in.value.name !== '' &&
    cat_in.value.age !== null &&
    cat_in.value.is_male !== null &&
    cat_in.value.health_condition !== null &&
    cat_in.value.description !== ''
  );
});

const submitForm = async () => {
  try {
    const data = {
      cat_in: {
        name: cat_in.value.name,
        is_male: cat_in.value.is_male === '公猫',
        age: parseInt(cat_in.value.age, 10),
        health_condition: 
          cat_in.value.health_condition === 'HEALTHY'
            ? 1
            : cat_in.value.health_condition === 'SICK'
            ? 2
            : cat_in.value.health_condition === 'VACCINATED'
            ? 3
            : 4,
        description: cat_in.value.description,
      },
    };
    const response = await createCat(data);
    console.log('提交猫咪信息：', response);
    // 提交后重置表单
    cat_in.value = {
      name: '',
      age: null,
      is_male: null,
      health_condition: null,
      description: '',
    };
    snackbar.success('提交成功！');
  } catch (error) {
    console.error('添加猫咪失败:', error);
    snackbar.error('提交失败，请检查输入是否正确');
  }
};

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
