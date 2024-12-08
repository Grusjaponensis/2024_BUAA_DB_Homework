<template>
  <v-container fluid class="home-container">
    <v-row justify="center" class="mb-8">
      <v-col cols="12" md="6" class="text-center">
        <!-- <img src="kitten-logo.png" alt="Kitten Logo" class="kitten-logo" /> -->
        <h1 class="display-2 font-weight-bold mb-4">猫猫欢迎你！</h1>
        <p class="headline font-weight-regular">北航所有的猫猫，都在这里！</p>

        <v-btn class="login_btn" size="x-large" to="/login">登录</v-btn>
        <v-btn class="signup_btn" size="x-large" to="/signup">注册</v-btn>
      </v-col>
    </v-row>

    <v-col class="mx-auto" justify="center">
      <v-row cols="12" md="6" class="mb-6">
        <v-card class="elevation-10">
          <v-card-title class="headline">公告栏</v-card-title>
          <v-card-text>
            <p>这里是最新的平台公告和更新信息。请定期查看以获取最新动态。</p>
          </v-card-text>
        </v-card>
      </v-row>
      <v-row cols="12" md="6" class="mb-6">
        <v-card class="elevation-10">
          <v-card-title class="headline">小贴士</v-card-title>
          <v-card-text>
            <p>了解如何与猫咪互动，发现新功能，以及如何充分利用我们的平台。</p>
          </v-card-text>
        </v-card>
      </v-row>
    </v-col>
  </v-container>
</template>

<script setup>
  //
</script>

<style scoped>
.title {
  text-align: center;
  margin-top: 50px;
  color: #ffffff;
}

.home-container {
  background-image: url('your-background-image.jpg'); /* Set background image */
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent black overlay for better text visibility */
}

.kitten-logo {
  width: 150px; /* Logo size */
  height: auto;
  margin-bottom: 24px;
}

h1.display-2 {
  color: #00bbff; /* Golden color for the title */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6); /* Strong shadow for readability */
}

p.headline {
  color: #ffffff; /* White color for subtitle */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6); /* Strong shadow for readability */
}

.v-card {
  background-color: rgba(255, 255, 255, 0.85); /* Slightly more opaque background for readability */
  border-radius: 8px; /* Rounded corners for the cards */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
  margin-top: 24px; /* Spacing between cards */
}

.v-card-title.headline {
  color: #3b3b3b; /* Darker color for the card title for contrast */
}

.v-card-text {
  color: #4a4a4a; /* Slightly softer text color */
}

.primary-btn {
  background-color: #ffcc00; /* Button color */
  color: #3b3b3b; /* Text color for the button */
  font-weight: bold;
  border-radius: 8px; /* Rounded button */
  padding: 10px 24px;
  text-transform: uppercase;
}

.primary-btn:hover {
  background-color: #e6b800; /* Darker shade on hover */
  transition: background-color 0.3s ease-in-out;
}

.login_btn {
  margin-top: 25px;
};

.signup_btn {
  margin-top: 25px;
  margin-left: 10px;

}
</style>
