<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="4">
        <v-card class="mx-auto my-4" max-width="600" rounded="lg" elevation="4">
          <v-card-title class="headline">添加猫咪</v-card-title>
          <v-card-text>
            <v-form ref="form" @submit.prevent="submitForm">
              <v-text-field
                v-model="cat_in.name"
                label="猫咪姓名"
                required
                outlined
              ></v-text-field>
              <v-select
                v-model="cat_in.is_male"
                :items="['male', 'female']"
                label="猫咪性别"
                required
                outlined
                dense
              ></v-select>
              <v-text-field
                v-model="cat_in.age"
                type="number"
                label="猫咪年龄"
                required
                :rules="[rules.age]"
                outlined
                dense
              ></v-text-field>
              <v-select
                v-model="cat_in.health_condition"
                :items="['HEALTHY', 'SICK', 'VACCINATED', 'DEAD']"
                label="猫咪健康状况"
                required
                outlined
                dense
              ></v-select>
              <div class="mt-8">
                <v-file-input
                  v-model="avatarFile"
                  label="上传图片"
                  accept="image/*"
                  @click="AvatarUpload"
                  outlined
                  dense
                ></v-file-input>
              </div>
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
              <v-btn
                color="green"
                to="/cats/catBase"
                rounded
                class="mt-2"
                block
              >
                返回
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { createCat } from '@/api/cat';
import snackbar from '@/api/snackbar';

const cat_in = ref({
  name: '',
  is_male: null,
  age: null,
  health_condition: null,
  description: '',
});

const avatarFile = ref(null);

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
        is_male: cat_in.value.is_male === 'male',
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
</script>

<style scoped>
.v-card {
  transition: transform 0.3s ease;
}

.v-card:hover {
  transform: translateY(-4px);
}

.v-btn {
  margin: 4px;
  text-transform: none;
}
</style>
