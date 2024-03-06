<template>
  <view>
    <div>
      <button @click="chooseFile">选择文件</button>
      <ul>
        <li v-for="(file, index) in selectedFiles" :key="index">{{ file.name }}</li>
      </ul>
      <button @click="uploadFiles">上传文件</button>
    
    </div>
  </view>
</template>

<script>
	import config from '../../config.js';
export default {
  data() {
    return {
      selectedFiles: [] // 用于存储已选择的文件
    };
  },
  methods: {
    chooseFile() {
      uni.chooseFile({
        count: 5, // 设置为允许选择多个文件
        extension: ['.xls', '.xlsx'],
        success: res => {
          this.selectedFiles = res.tempFiles;
        }
      });
    },
    async uploadFiles() {
      // 遍历已选择的文件数组，逐个上传文件
      this.selectedFiles.forEach(file => {
        uni.uploadFile({
          url: `${config.SERVER_URL}/upload`,
          filePath: file.path,
          name: 'file',
          formData: {
            // 可以在这里添加其他需要上传的参数
          },
          success: async uploadRes => {
            console.log('文件上传成功', uploadRes);
            // 直接使用服务器返回的文件链接
            const fileLink = uploadRes.data;
            // 创建一个下载链接
            const downloadLink = document.createElement('a');
            downloadLink.href = fileLink;
			
            downloadLink.download = 'processed_file.xlsx';
            // 模拟点击下载链接
            downloadLink.click();
          },
          fail: err => {
            console.error('文件上传失败', err);
            // 这里处理文件上传失败后的逻辑
          }
        });
      });
    },



    
  }
};
</script>

<style lang="scss">

</style>
