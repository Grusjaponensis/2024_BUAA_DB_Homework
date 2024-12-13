<template>
  <div class="cat-base">
  <v-container>
    <!-- 顶部欢迎横栏 -->
    <v-toolbar color='#d4eae0' dark class="top-bar">
      <v-toolbar-title>
        这里是猫猫基地，猫猫欢迎你！
      </v-toolbar-title>
    </v-toolbar>
    
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
    <!-- 左侧说明框 -->
    <div style="flex: 1; min-width: 200px; max-width: 300px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
      <h3 style="margin-bottom: 20px;">&nbsp;&nbsp;&nbsp;&nbsp;过去一年，我们收到了很多爱心人士的捐赠，感谢大家对猫猫的帮助！</h3>
      <h4>最近三笔捐款</h4>
      <ul style="list-style: none; padding: 0;">
        <li v-for="(donation, index) in recentDonations" :key="index" style="margin-bottom: 10px;">
          <div><strong>捐赠者:</strong>{{donation.is_anonymous? '匿名捐赠' : usernames[donation.user_id] }}</div>
          <div><strong>金额:</strong> ¥{{ donation.amount }}</div>
          <div><strong>时间:</strong> {{ donation.donated_at }}</div>
          <div v-if="donation.message"><strong>留言:</strong> {{ donation.message }}</div>
        </li>
      </ul>
    </div>
    <!-- 图表 -->
    <!-- <div style="flex: 2; min-width: 400px; max-width: 800px;">
      <canvas id="donationChart" style="width: 100%; height: 400px;"></canvas>
    </div> -->
    <!-- 时间选择器 -->
    <div class="donation-chart-container">
    <!-- 时间范围选择 -->
    <div class="date-selector">
      <div class="input-group">
        <label for="startMonth">起始月份：</label>
        <input type="month" id="startMonth" v-model="startMonth" class="month-input" />
      </div>
      <div class="input-group">
        <label for="endMonth">结束月份：</label>
        <input type="month" id="endMonth" v-model="endMonth" class="month-input" />
      </div>
      <div class="button-group">
        <v-btn @click="loadDonationChart" color="#d9ecfc" class="action-btn">查询</v-btn>
        <v-btn @click="exportToPDF" color="secondary" class="action-btn">导出为 PDF</v-btn>
      </div>
    </div>
    <!-- 图表展示 -->
    <div class="chart-wrapper">
      <canvas id="donationChart"></canvas>
    </div>
  </div>
  </div>
    <v-row class="mt-5">
      <v-col cols="12" md="6" v-for="cat in cats" :key="cat.id" justify="center">
        <v-card class="d-flex flex-column text-center pa-4" rounded="lg" elevation="4" max-width="550px">
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
          <div style=" padding: 10px;">
          <v-card-title class="headline">{{ cat.name }}</v-card-title>
          <v-card-subtitle >年龄: {{ cat.age }}</v-card-subtitle>
          <v-card-subtitle >性别: {{ cat.is_male ? '男' : '女' }}</v-card-subtitle>
          <v-card-subtitle >描述: {{ cat.description }}</v-card-subtitle>
          <v-card-subtitle >健康状况: {{ cat.health_condition  == 1 ? "HEALTHY" : cat.health_condition == 2 ? "SICK" : cat.health_condition == 3 ? "VACCINATED" : "DEAD"}}</v-card-subtitle>
          <!-- <v-card-subtitle>收到投喂: {{ cat.cans }}</v-card-subtitle> -->
          <v-expand-transition>
            <div v-show="showStates[cat.id]?.showCatEdit" class="mt-4 mb-4">
              <v-select
                v-model="health_condition"
                :items="['HEALTHY', 'SICK', 'VACCINATED', 'DEAD']"
                label="猫咪健康状况"
              ></v-select>
              <v-text-field
                v-model="description"
                label="描述"
                type="text"
                :rules="[v => !!v || '描述不能为空']"
              ></v-text-field>
              <v-btn color="#bbd5eb" @click="updateCatProfile(cat)" >确认更新</v-btn>
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
                v-if="user.login && (user.is_superuser || user.is_volunteer)"
              >
              <v-icon left class="mr-1">mdi-pencil</v-icon> 修改信息
            </v-btn>
            <v-btn
                color="#d9ecfc"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(cat.id, 'showAvatarUpload', true)"
                v-if="user.login && (user.is_superuser || user.is_volunteer)"
              >
              <v-icon left class="mr-1">mdi-image</v-icon> 更换图片
            </v-btn>
            <v-btn
              color="indigo-lighten-2"
              rounded="lg"
              variant="elevated"
              @click="showPositionEdit = true; positionEditCat = cat"
              v-if="user.login && (user.is_superuser || user.is_volunteer)"
            >
            <v-icon left class="mr-1">mdi-map-marker-outline</v-icon> 更新位置
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
      style="position: fixed; bottom: 80px; right: 24px;"
      size="large"
      @click = "showAddCatDialog = true"
      v-if = "user.login && (user.is_superuser || user.is_volunteer)"
    >
    <v-icon>mdi-plus</v-icon>
    </v-btn>

    <v-btn
      color="#bbd5eb"
      class="elevation-4"
      style="position: fixed; bottom: 24px; right: 24px;"
      size="large"
      @click = "showDonateDialog = true"
      v-if = "user.login"
    >
    <v-icon>mdi-handshake</v-icon>
    </v-btn>
    <v-dialog 
    v-model="showDonateDialog" 
    max-width="70vw"
    width="650px"
  >
    <v-toolbar title="捐赠">
      <v-btn icon="mdi-close" @click="showDonateDialog = false"></v-btn>
    </v-toolbar>
    <v-card>
      <v-card-text>
        <v-form ref="form" @submit.prevent="submitDonation">
          <v-select
            v-model="donation.amount"
            :items="[50, 100, 200, 500, 1000]"
            label="选择捐赠金额 (元)"
            required
          ></v-select>
          <v-checkbox
            v-model="donation.isAnonymous"
            label="匿名捐赠"
          ></v-checkbox>
          <v-textarea
            v-model="donation.message"
            label="留言 (可选)"
            counter="100"
            class="mt-3"
          ></v-textarea>
          <v-btn
            color="primary"
            type="submit"
            :disabled="!donationFormIsValid"
            rounded
            class="mt-4"
            block
          >
            提交捐赠
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

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
          <div class="mt-4 text-h6 font-weight-regular">
          选择猫咪位置
          </div>
          <MapView 
          style="height: 500px;"
          ></MapView>
          <v-text-field>
            当前位置:{{ location.latitude }} , {{ location.longitude }} 
          </v-text-field>
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
  <v-dialog v-model="showPositionEdit" max-width="500px">
    <v-toolbar title="更新猫咪位置">
      <v-btn icon="mdi-close" @click="showPositionEdit = false"></v-btn>
    </v-toolbar>
    <v-card>
      <MapChange
      :center="[positionEditCat.latest_longitude, positionEditCat.latest_latitude]"
      :zoom = 16.5
      :markerPosition="[positionEditCat.latest_longitude, positionEditCat.latest_latitude]"
      >
      </MapChange>
      <v-text-field>
        当前位置： {{ location.longitude }} , {{ location.latitude }}
      </v-text-field>
      <v-btn
        color="blue-lighten-2"
        @click="updateCatPosition(positionEditCat, location.longitude , location.latitude)"
        rounded="lg"
        class="ma-4"
      >
        确定
      </v-btn>
    </v-card>
  </v-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getProfile } from '@/api/user';
import { addPrefix } from '@/api/post';
import { getCats, createCat,deleteCat,updateCatByAdmin, updateCatLocation } from '@/api/cat';
import { createDonation } from '@/api/donate';
import { user } from '@/api/user';
import { location } from '@/api/user';
import snackbar from '@/api/snackbar';
import MapView from '@/map/MapView.vue';
import MapChange from '@/map/MapChange.vue';

const cats = ref([]);
const isAdmin = ref(false);
const router = useRouter();
const remainingCans = ref(6);
const showStates = ref({});
const description = ref('');
const showCatEdit = ref(false);
const fileUrls = ref([])
const health_condition = ref('')
const showPositionEdit = ref(false);
const positionEditCat = null;

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
  loadDonationChart();
  loadRecentDonations();
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

const updateCatPosition = async (cat, longitude, latitude) => {
  try {
    const response = await updateCatLocation(cat.id, longitude, latitude);
    console.log('更新猫咪位置成功', response);
    showPositionEdit.value = false;
    snackbar.success('更新猫咪位置成功');
  } catch (error) {
    console.error('更新猫咪位置失败:', error);
    snackbar.error('更新猫咪位置失败');
  }
}

const toggleSection = (id, section, value) => {
  Object.keys(showStates.value).forEach((key) => {
    showStates.value[key][section] = key == id ? value : false;
    // console.log("key : " + key);
    // console.log("section : " + section);
    // console.log("toggleSection : " +  showStates.value[key][section]);
  });

  if (section === "showCatEdit" && value) {
      // console.error(id)
      const cat = cats.value.find((u) => u.id === id)
      // console.error(cat)
      description.value = cat.description;
      health_condition.value = cat.health_condition === 1 ? 'HEALTHY'
        : cat.health_condition === 2 ? 'SICK'
        : cat.health_condition === 3 ? 'VACCINATED'
        : 'DEAD';
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

const updateCatProfile = async (cat) => {
    try {
      if (!description.value || description.value.trim() === '') {
        snackbar.error('描述不能为空');
        return;
      }
      if (description.value.length > 256) {
        snackbar.error('描述长度不能超过256个字符');
        return;
      }
      const catData = new FormData();
      catData.append('description', description.value);
      catData.append('health_condition', 
      health_condition === 'HEALTHY' ? 1
        : health_condition === 'SICK' ? 2
        : health_condition === 'VACCINATED' ? 3
        : 4);
      console.error('catData', catData);
      const response = await updateCatByAdmin(cat.id , catData);
      console.log('信息修改成功', response);
      showCatEdit.value = false;
      await fetchCats();
      snackbar.success('信息修改成功');
      toggleSection(cat.id, "showCatEdit", false);
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
  image: []
});

const showAddCatDialog = ref(false);
const showDonateDialog = ref(false);
const donation = ref({
  amount: null,
  isAnonymous: false,
  message: '',
});
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
const donationFormIsValid = computed(() => {
  return donation.value.amount !== null;
});
const submitForm = async () => {
  try {
    console.error('位置信息 ' + location.longitude + ' ' + location.latitude)
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
    if (location.longitude === 0 || location.latitude === 0) {
      snackbar.error('请在地图上选择猫咪位置！');
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
    formData.append('longitude', location.longitude);
    formData.append('latitude', location.latitude);
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
      image: []
    };
    fetchCats();
    showAddCatDialog.value = false;
    snackbar.success('提交成功！');
  } catch (error) {
    console.error('添加猫咪失败:', error);
    snackbar.error('添加猫咪失败，请检查猫咪是否已存在');
  }
};

const submitDonation = async () => {
  try {
    if (!donation.value.amount) {
      snackbar.error('请选择捐赠金额！');
      return;
    }

    if (donation.value.message && donation.value.message.length > 100) {
      snackbar.error('留言长度不能超过100个字符');
      return;
    }
    
    const data = {
      amount: donation.value.amount,
      is_anonymous: donation.value.isAnonymous ? true : false,
      message: donation.value.message || '',
    }

    console.error('提交捐赠信息: ', data);
    const response = await createDonation(data); 
    console.error('返回信息: ', response);

    // 重置表单
    donation.value.amount = null;
    donation.value.isAnonymous = false;
    donation.value.message = '';

    showDonateDialog.value = false;
    snackbar.success('捐赠成功！感谢您的支持！');
    loadRecentDonations();
    loadDonationChart();
  } catch (error) {
    console.error('提交捐赠失败:', error);
    snackbar.error('提交失败，请稍后再试');
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

import { getPublicProfile } from '@/api/user';
import { fetchDonationTotal,fetchDonations } from '@/api/donate';
// 最近三笔捐款
const recentDonations = ref([]);
const usernames = ref({});
// 获取最近三笔捐款
const loadRecentDonations = async () => {
  try {
    const donations = await fetchDonations(); 
    recentDonations.value = donations.data.slice(0, 3); 
    console.log('获取最近捐款成功:', recentDonations.value);
    for (const donation of recentDonations.value) {
    console.log('加载用户名', donation);
      const id = donation.user_id;
      try {
        const response = await getPublicProfile(id);
        console.log(`获取用户 ${id} 名称成功:`, response.nickname);
        usernames.value[id] = response.nickname;
      } catch (error) {
        console.error(`获取用户 ${id} 名称失败:`, error);
        usernames.value[id] = '匿名用户';
      }
    }
  } catch (error) {
    console.error('获取最近捐款失败:', error);
  }
};



const fetchMonthlyDonations = async (startMonth, endMonth) => {
  const start = new Date(startMonth);
  const end = new Date(endMonth);
  const monthlyData = [];

  while (start <= end) {
    const startOfMonth = new Date(start.getFullYear(), start.getMonth(), 1);
    const endOfMonth = new Date(start.getFullYear(), start.getMonth() + 1, 0);

    const startDate = startOfMonth.toISOString().split('T')[0];
    const endDate = endOfMonth.toISOString().split('T')[0];

    try {
      const total = await fetchDonationTotal({ start_date: startDate, end_date: endDate }).then(res => res.data.total_amount);
      console.log(`获取${startDate}至${endDate}的捐赠成功:`, total);
      monthlyData.push({
        month: `${startOfMonth.getFullYear()}-${String(startOfMonth.getMonth() + 1).padStart(2, '0')}`,
        total,
      });
    } catch (error) {
      console.error(`获取${startDate}至${endDate}的捐赠失败:`, error);
      monthlyData.push({
        month: `${startOfMonth.getFullYear()}-${String(startOfMonth.getMonth() + 1).padStart(2, '0')}`,
        total: 0,
      });
    }

    start.setMonth(start.getMonth() + 1);
  }

  return monthlyData;
};

import { Chart } from 'chart.js/auto';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

const startMonth = ref(new Date(new Date().setFullYear(new Date().getFullYear() - 1)).toISOString().substring(0, 7));
const endMonth = ref(new Date().toISOString().substring(0, 7));
let chartInstance = null;

const createDonationChart = (ctx, data) => {
  const labels = data.map(item => item.month);
  const totals = data.map(item => item.total);

  return new Chart(ctx, {
    type: 'bar', // 或 'line'
    data: {
      labels,
      datasets: [
        {
          label: '每月捐赠总额 (元)',
          data: totals,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

const loadDonationChart = async () => {
  if (new Date(startMonth.value) > new Date(endMonth.value)) {
    alert('起始月份不能晚于结束月份！');
    return;
  }

  const ctx = document.getElementById('donationChart').getContext('2d');
  const data = await fetchMonthlyDonations(startMonth.value, endMonth.value);

  if (chartInstance) {
    chartInstance.destroy(); // 销毁旧图表
    chartInstance = null;
  }
  chartInstance = createDonationChart(ctx, data);
};
const exportToPDF = async () => {
  const canvas = document.getElementById('donationChart');
  const canvasImage = await html2canvas(canvas);

  const imgData = canvasImage.toDataURL('image/png');
  const pdf = new jsPDF('landscape');
  pdf.addImage(imgData, 'PNG', 10, 10, 280, 150);
  pdf.save(`donation-statistics-${startMonth.value}-to-${endMonth.value}.pdf`);
};

</script>

<style scoped>
.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
.cat-base {
  height: 100%;
}
.donation-chart-container {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 时间选择区域样式 */
.date-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
  justify-content: flex-start;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.month-input {
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  max-width: 200px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 4px;
}

/* 图表区域样式 */
.chart-wrapper {
  margin-top: 20px;
  background-color: #effaf5;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>