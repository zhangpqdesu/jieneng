<template>
  <view class="contact-us">
    <view class="contact-info">
      <image src="/static/logo.png" class="logo" />
      <view class="info">
        <text>公司名称：UniApp Corp</text><br>
        <text>地址：123 Main St, City, Country</text><br>
        <text>电话：123-456-7890</text><br>
        <text>邮箱：info@uniapp.com</text>
      </view>
    </view>
    <view class="map">
      <!-- 在此处添加地图组件，显示公司位置 -->
    </view>
  </view>
</template>

<style>
  .contact-us {
    padding: 20px;
  }
  .contact-info {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }
  .logo {
    width: 80px;
    height: 80px;
    margin-right: 20px;
  }
  .info {
    flex: 1;
  }
  .map {
    height: 300px;
    /* 设置地图高度 */
  }
</style>

<script>
  export default {
    name: 'ContactUs',
    data() {
      return {};
    },
    methods: {},
    onLoad() {
      // 在此处添加逻辑以初始化地图
    }
  };
</script>
