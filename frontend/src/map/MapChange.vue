<template>
  <div id="container1"></div>
</template>
  
  <script setup>
  import { onMounted, onUnmounted } from "vue";
  import { location } from '@/api/user'
  import AMapLoader from "@amap/amap-jsapi-loader";
  
  const props = defineProps({
      center: {
          type: Array
      },
      zoom: {
          type: Number
      },
      markerPosition: {
          type: Array
      } 
  })
  
  let marker = null;
  let map = null;
  
  onMounted(() => {
    console.log("传入的坐标" , props.markerPosition)
    console.log("传入的中心点" , props.center)
    window._AMapSecurityConfig = {
      securityJsCode: "fd49876bde2479a9c3935444d613ce0a",
    };
    AMapLoader.load({
      key: "c650eb1ae1fe174a0048104528d32fcb", // 申请好的Web端开发者Key，首次调用 load 时必填
      version: "2.0", // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
      plugins: ["AMap.Scale" , "AMap.Marker"], //需要使用的的插件列表，如比例尺'AMap.Scale'，支持添加多个如：['...','...']
    })
      .then((AMap) => {
        map = new AMap.Map("container1", {
          // 设置地图容器id
          viewMode: "3D", // 是否为3D地图模式
          zoom: props.zoom, // 初始化地图级别
          center: props.center, // 初始化地图中心点位置
        });
        if (props.markerPosition && props.markerPosition.length === 2) {
            marker = new AMap.Marker({
                position: [props.markerPosition[0], props.markerPosition[1]],
            })
            map.add(marker)
        }
        location.longitude = props.markerPosition[0]
        location.latitude = props.markerPosition[1]
        console.log("当前坐标" , location)
        map.on("click", (e) => {
            const {lng , lat} = e.lnglat; 
            console.log("点击的经纬度坐标" , lng, lat)
            location.longitude = lng
            location.latitude = lat
            marker.setPosition([lng, lat])
            console.log("当前坐标" , location)
        })
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
    #container1 {
      padding: 0px;
      margin: 0px;
      width: 100%;
      height: 800px;
    }
  </style>