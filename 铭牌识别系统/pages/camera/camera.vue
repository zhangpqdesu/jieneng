<template>
  <view>
    <!-- 选择图片按钮 -->
	<view class="upload">
		<image class="image" src="/static/photo/上传图片.png" mode="aspectFit" @click="chooseImage"></image>
		<text style="color: #707070;margin-top: 10rpx;">点击图标拍照/选择图片</text>
	</view>

    <!-- 展示选择的图片 -->
    <image :src="imgUrl" mode="aspectFit" v-if="imgUrl" style="width: 300px; height: 300px;"></image>

  </view>
</template>

<script>
import config from '../../config.js';
export default {
  data() {
    return {
      imgUrl: '',
      ocrResult: null
    }
  },
  methods: {
    // 选择图片
    chooseImage: function() {
      var that = this;
      uni.chooseImage({
        count: 9,
        sizeType: ['original', 'compressed'],
        sourceType: ['album', 'camera'],
        success: function (res) {
          // 选择图片成功后，显示选择的图片
          that.imgUrl = res.tempFilePaths[0];
          that.ocrResult = null; // 清空之前的 OCR 结果
    
          // 将选择的图片上传到后端
          uni.uploadFile({
            url: `${config.SERVER_URL}/ocr`,
            filePath: res.tempFilePaths[0],
            name: 'image',
            success: function (uploadRes) {
              console.log('上传成功，后端返回数据:', uploadRes.data);
              try {
                var response = JSON.parse(uploadRes.data);
                console.log('解析后的响应数据:', response);
                that.ocrResult = response;
                uni.setStorageSync('ocrResult',response);
                // 存储图片路径到本地存储
                uni.setStorageSync('imgUrl', res.tempFilePaths[0]);
                
                // 重定向到结果页面
                uni.reLaunch({
                  url: '/pages/result/result'
                });
              } catch (error) {
                console.error('解析响应数据出错:', error);
              }
            },
            fail: function (error) {
              console.error('上传失败:', error);
            }
          });
        },
        fail: function (error) {
          console.error('选择图片失败:', error);
        }
      });
    }
  }
}
</script>

<style lang="scss">
.upload{
	margin-top: 20%;
	display: flex;
	flex-direction: column;
	align-items: center;
	.image{
		height: 100rpx;
	}
}
</style>
