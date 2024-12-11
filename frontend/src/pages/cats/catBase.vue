<template>
  <div class="cat-base">
  <v-container>
    <!-- 顶部欢迎横栏 -->
    <!-- <v-toolbar color='#d4eae0' dark class="top-bar">
        <v-toolbar-title>
          这里是猫猫基地，猫猫欢迎你！
        </v-toolbar-title>
      </v-toolbar> -->
    <v-row class="mt-5">
      <v-col cols="12" md="6" v-for="cat in cats" :key="cat.id" justify="center" align="center">
        <v-card class="d-flex flex-column text-center" rounded="lg" elevation="4" max-width="500px">
          <v-carousel hide-delimiters="true" show-arrows="hover" style = "max-width: 500px; height: 300px; margin: 0 auto;">
            <v-carousel-item 
              v-for="(image, index) in cat.image_urls"
              :key = index
              cover
              >
              <v-img
                max-width="100%"
                max-height="100%"
                :src = "`${addPrefix(image)}`"
                contain
              ></v-img>
            </v-carousel-item>
          </v-carousel>
          <div style="background-color:white; padding: 10px;">
          <v-card-title class="headline">{{ cat.name }}</v-card-title>
          <v-card-subtitle >年龄: {{ cat.age }}</v-card-subtitle>
          <v-card-subtitle >性别: {{ cat.is_male ? '男' : '女' }}</v-card-subtitle>
          <v-card-subtitle >描述: {{ cat.description }}</v-card-subtitle>
          <v-card-subtitle >健康状况: {{ cat.health_condition  == 1 ? "HEALTHY" : cat.health_condition == 2 ? "SICK" : cat.health_condition == 3 ? "VACCINATED" : "DEAD"}}</v-card-subtitle>
          <!-- <v-card-subtitle>收到投喂: {{ cat.cans }}</v-card-subtitle> -->
          
          <v-expand-transition>
            <div v-show="showStates[cat.id]?.showCatEdit" class="mt-4 mb-4">
              <v-text-field
                v-model="name"
                label="姓名"
                type="text"
                :rules="[v => !!v || '昵称不能为空']"
              ></v-text-field>
              <v-text-field
                v-model="description"
                label="描述"
                type="text"
                :rules="[v => !!v || '描述不能为空']"
              ></v-text-field>
              <v-btn color="#bbd5eb" @click="updateCatProfile(cat.id)" >确认更新</v-btn>
              <v-btn color="#f0f0f0" class="ml-2" @click="toggleSection(cat.id, 'showCatEdit', false)">取消</v-btn>
            </div>
          </v-expand-transition>
          <v-expand-transition>
            <div v-show="showStates[cat.id]?.showAvatarUpload" class="mt-4 mb-4">
              <v-file-input
              label="上传图片"
              accept="image/*"
              multiple
              @change="handleFiles"
              ></v-file-input>
              <v-row>
                <v-col 
                  v-for="(fileUrl, index) in fileUrls"
                  :key = "index"
                  cols = "4">
                  <v-img
                    :src="fileUrl"
                    alt="预览图"
                    aspect-ratio = "1"
                    max-height = "150"
                    class="mb-4"
                    ></v-img>
                </v-col>
              </v-row>
              <v-btn color="#bbd5eb" class = "mt-2" @click="updateCatAvatar(cat.id)">确认上传</v-btn>
              <v-btn color="#f0f0f0" class="ml-2 mt-2" @click="toggleSection(cat.id, 'showAvatarUpload', false)">取消</v-btn>
            </div>
          </v-expand-transition>

          <v-card-actions class="d-flex justify-center">
            <v-btn
              rounded="lg"
              variant="elevated"
              color = "#c2d7f3"
              @click="feedCat(cat)"
              v-if="user.login && !user.is_superuser"
            >
              <v-icon left class = "mr-1">mdi-paw</v-icon>投喂
            </v-btn>
            <v-btn
              rounded="lg"
              variant="elevated"
              color = "#fff8dc"
              @click= goToCatDetails(cat.id)
              v-if="user.login"
              >
            <v-icon left class = "mr-1">mdi-cat</v-icon> 详情
            </v-btn>
            <v-btn
                color="#e8d6ec"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(cat.id, 'showCatEdit', true)"
                v-if="user.login && user.is_superuser"
              >
              <v-icon left class="mr-1">mdi-pencil</v-icon> 修改信息
            </v-btn>
            <v-btn
                color="#d9ecfc"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(cat.id, 'showAvatarUpload', true)"
                v-if="user.login && user.is_superuser"
              >
              <v-icon left class="mr-1">mdi-image</v-icon> 更换图片
            </v-btn>
            <v-btn 
              rounded="lg"
              @click="showDeleteDialog = true ; removeCatId = cat.id" 
              v-if="isAdmin" 
              variant="elevated"
              color="#f8d6dd">
              <v-icon left class = "mr-1">mdi-delete</v-icon>删除猫咪
            </v-btn>
          </v-card-actions>
        </div>
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
          <v-btn color="red" @click = "removeCat(removeCatId)"> 确认</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
  <v-btn
      color="#bbd5eb"
      class="elevation-4"
      style="position: fixed; bottom: 24px; right: 24px;"
      size="large"
      @click = "showAddCatDialog = true"
      v-if = "user.login && user.is_superuser"
    >
    <v-icon>mdi-plus</v-icon>
    </v-btn>

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
            label="上传图片"
            accept="image/*"
            multiple
            @change="handleFiles"
          ></v-file-input>
          <v-row>
            <v-col 
              v-for="(fileUrl, index) in fileUrls"
              :key = "index"
              cols = "4">
              <v-img
                :src="fileUrl"
                alt="预览图"
                aspect-ratio = "1"
                max-height = "150"
                class="mb-4"
                ></v-img>
            </v-col>
          </v-row>
          <v-textarea
            v-model="cat_in.description"
            label="对猫咪的描述"
            counter="50"
            class="mt-3"
          ></v-textarea>
          <v-btn
            color="disabled? 'grey' : '#bbd5eb'"
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
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getProfile } from '@/api/user';
import { addPrefix } from '@/api/post';
import { getCats, createCat,deleteCat,updateCatByAdmin } from '@/api/cat';
import { user } from '@/api/user';
import snackbar from '@/api/snackbar';

const cats = ref([]);
const isAdmin = ref(false);
const router = useRouter();
const remainingCans = ref(6);
const showStates = ref({});
const name = ref('');
const description = ref('');
const showCatEdit = ref(false);
const fileUrls = ref([])

const handleFiles = (event) => {
  const files = event.target.files;
  console.error("上传的图片：" + files) 
  if (files) {
    cat_in.value.image = Array.from(files)
    fileUrls.value = []
    Array.from(files).forEach((file) => {
      fileUrls.value.push(URL.createObjectURL(file))
    })
  }
}

onMounted(async() => {
  fetchProfile();
  try {
    const response = await getCats();
    cats.value = response.cats;
    cats.value.forEach((cat) => {
      showStates.value[cat.id] = {
        showCatEdit: false,
        showAvatarUpload: false,
      };
    })
    console.log('获取猫咪列表成功', response.cats);
  } catch (error) {
    console.log('获取猫咪列表失败:', error);
  }
});

const toggleSection = (id, section, value) => {
  Object.keys(showStates.value).forEach((key) => {
    showStates.value[key][section] = key == id ? value : false;
    console.log("key : " + key);
    console.log("section : " + section);
    console.log("toggleSection : " +  showStates.value[key][section]);
  });

  if (section === "showCatEdit" && value) {
      // console.error(id)
      const cat = cats.value.find((u) => u.id === id)
      // console.error(cat)
      name.value = cat.name;
      description.value = cat.description;
  }
};

const updateCatAvatar = async (id) => {
  try {
    const formData = new FormData();
    if (cat_in.value.image && cat_in.value.image.length > 0) {
      cat_in.value.image.forEach((file) => {
        formData.append('new_images', file);
      })
    } else {
      snackbar.error('请上传图片！');
      return;
    }
    console.log('formData_Change_avatar' ,  formData)
    const response = await updateCatByAdmin(id, formData);
    console.log('头像上传成功', response);
    showCatEdit.value = false;
    cat_in.value = {
      name: '',
      age: null,
      is_male: null,
      health_condition: null,
      description: '',
      image: [],
    };
    fetchCats();
    toggleSection(id, "showAvatarUpload", false);
    snackbar.success('头像上传成功');
  } catch (error) {
    console.error('上传头像失败:', error);
    snackbar.error('上传头像失败');
  }
}

const updateCatProfile = async (id) => {
    try {
      if (!name.value || name.value.trim() === '') {
        snackbar.error('昵称或邮箱不能为空');
        return;
      }
      if (name.value.length > 128) {
        snackbar.error('姓名长度不能超过128个字符');
        return;
      }
      if (!description.value || description.value.trim() === '') {
        snackbar.error('描述不能为空');
        return;
      }
      if (description.value.length > 256) {
        snackbar.error('描述长度不能超过256个字符');
        return;
      }
      const catData = new FormData();
      catData.append('name', name.value);
      catData.append('description', description.value);
      console.error('catData', catData);
      const response = await updateCatByAdmin(id , catData);
      console.log('信息修改成功', response);
      showCatEdit.value = false;
      await fetchCats();
      snackbar.success('信息修改成功');
      toggleSection(id, "showCatEdit", false);
    } catch (error) {
      console.error('更新猫咪资料失败:', error);
      snackbar.error('更新猫咪资料失败');
    }
  };

const cat_in = ref({
  name: '',
  is_male: null,
  age: null,
  health_condition: null,
  description: '',
  image: [],
});

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
    && cat_in.value.image != []
  );
});

const submitForm = async () => {
  try {
    if (cat_in.value.name.length > 128) {
      snackbar.error('姓名长度不能超过128个字符');
      return;
    }
    if (cat_in.value.age > 30) {
      snackbar.error('年龄过大，请重新输入！');
      return;
    }
    if (cat_in.value.description.length > 256) {
      snackbar.error('描述长度不能超过256个字符');
      return;
    }
    const formData = new FormData();
    formData.append('name', cat_in.value.name);
    formData.append('is_male', cat_in.value.is_male === '公猫');
    formData.append('age', parseInt(cat_in.value.age, 10));
    formData.append('health_condition', 
      cat_in.value.health_condition === 'HEALTHY' ? 1
        : cat_in.value.health_condition === 'SICK' ? 2
        : cat_in.value.health_condition === 'VACCINATED' ? 3
        : 4);
    formData.append('description', cat_in.value.description);
    // formData.append('image', cat_in.value.image);
    if (cat_in.value.image && cat_in.value.image.length > 0) {
      cat_in.value.image.forEach((file) => {
        formData.append('image', file);
      })
    } else {
      snackbar.error('请上传图片！');
      return;
    }
    console.error('提交猫咪信息: ', formData)
    const response = await createCat(formData);
    console.error('返回信息: ', response);
    // 提交后重置表单
    cat_in.value = {
      name: '',
      age: null,
      is_male: null,
      health_condition: null,
      description: '',
      image: [],
    };
    fetchCats();
    showAddCatDialog.value = false;
    snackbar.success('提交成功！');
  } catch (error) {
    console.error('添加猫咪失败:', error);
    snackbar.error('添加猫咪失败，请检查猫咪是否已存在');
  }
};
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
    cats.value.forEach((cat) => {
      showStates.value[cat.id] = {
        showCatEdit: false,
        showAvatarUpload: false,
      };
    })
    console.log('获取猫咪列表成功', response.cats);
  } catch (error) {
    console.error('获取猫咪列表失败:', error);
  }
};

const removeCat = async (id) => {
  try {
    await deleteCat(id);
    snackbar.success('删除成功！');
    cats.value = cats.value.filter((c) => c.id !== id);
    fetchCats();
    showDeleteDialog.value = false;
  } catch (error) {
    snackbar.error('删除失败');
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
    snackbar.warning('已到达每日投喂上限');
  }
};

</script>

<style scoped>
.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
.cat-base {
  background-color: #f0f0f0;
  height: 100%;

}
</style>