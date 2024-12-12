<template>
  <div id="container"></div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import AMapLoader from "@amap/amap-jsapi-loader";

const props = defineProps({
    center: {
        type: Array, default: () => [116.347209, 39.981645]
    },
    zoom: {
        type: Number , default: 16.3
    },
    markerPosition: {
        type: Array, default: () => [116.347209, 39.981645]
    } 
    , markerTitle: {
        type: String, default: "Marker"
    }
})

let marker = null;
let map = null;

onMounted(() => {
  window._AMapSecurityConfig = {
    securityJsCode: "fd49876bde2479a9c3935444d613ce0a",
  };
  AMapLoader.load({
    key: "c650eb1ae1fe174a0048104528d32fcb", // 申请好的Web端开发者Key，首次调用 load 时必填
    version: "2.0", // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
    plugins: ["AMap.Scale" , "AMap.Marker"], //需要使用的的插件列表，如比例尺'AMap.Scale'，支持添加多个如：['...','...']
  })
    .then((AMap) => {
      map = new AMap.Map("container", {
        // 设置地图容器id
        viewMode: "3D", // 是否为3D地图模式
        zoom: props.zoom, // 初始化地图级别
        center: props.center, // 初始化地图中心点位置
      });
      marker = new AMap.Marker({
        position: props.markerPosition,
        title: props.markerTitle,
      })
      map.add(marker)
      map.addControl(new AMap.Scale())
    })
    .catch((e) => {
      console.log("加载地图失败", e);
    });
});

onUnmounted(() => {
  map?.destroy();
});
</script>

<style scoped>
  #container {
    padding: 0px;
    margin: 0px;
    width: 100%;
    height: 800px;
  }
</style>