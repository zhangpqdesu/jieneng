<template>
  <view>
    <!-- 选择图片按钮 -->
    <button @click="chooseImage">选择图片</button>

    <!-- 展示选择的图片 -->
    <image :src="imgUrl" mode="aspectFit" v-if="imgUrl" style="width: 300px; height: 300px;"></image>

   
    
  </view>
</template>

<script>
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
            url: 'http://127.0.0.1:5000/ocr', // 请替换为你的后端接口地址
            filePath: res.tempFilePaths[0],
            name: 'image',
            success: function (uploadRes) {
              console.log('上传成功，后端返回数据:', uploadRes.data);
              try {
                var ocrResult = JSON.parse(uploadRes.data);
                console.log('解析后的 OCR 结果:', ocrResult);
                that.ocrResult = ocrResult;
				// 在发送请求并获取到参数后
				uni.setStorageSync('ocrResult', ocrResult);
				
				uni.reLaunch({
			  url: '/pages/result/result'
				});
              } catch (error) {
                console.error('解析 OCR 结果出错:', error);
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
