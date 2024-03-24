<template>
  <view>
    <view class="out">
      <image class="default" src="/static/photo/default.png" mode="aspectFit"></image>
      <view class="personalDetail">
        <view class="name">{{ name }}</view>
        <view class="name2">{{ name2 }}</view>
      </view>  
    </view>
    <br><br><br><br>
    
    <!-- 显示从后端获取的数据 -->
    <view v-if="listData.length > 0">
		<view class="export-button">
	      <button class="btn" @click="exportData">导出数据</button>
	    </view>
      <view v-for="(item, index) in listData" :key="index" class="item">
        <image class="item-image" :src="item.url"></image>
        <view class="item-details">
		  <text class="record-place">记录url: {{ item.url }}</text>
          <text class="record-place">记录地址: {{ item.record_place }}</text>
          <text class="type">机器类型: {{ item.type }}</text>
          <text class="energy-consumption">机器能效：{{ item.energy_consumption }}</text>
          <text class="is_backward">是否为淘汰设备：{{item.is_backward}}</text>
		  <text class="record-time">记录时间: {{ item.record_time }}</text>
          <text class="extraInfo">备注：{{item.extra_info}}</text>
		</view>
      </view>
    </view>
    <view v-else>
      <text>没有数据</text>
    </view>
  </view>
</template>


<script>
  import config from '../../config.js';
  export default {
    data() {
      return {
        listData: [], // Initialize an empty array to store data from the backend
        name: '',
        name2: '普通用户'
      };
    },
    onShow() {
      this.name = uni.getStorageSync('name') || '未登录';
    },
	methods: {
	      exportData() {
	        const username = uni.getStorageSync('name') || '未登录';
	
	        // Fetch data from backend
	        uni.request({
	          url: `${config.SERVER_URL}/listdata?username=${username}`,
	          method: 'GET',
	          success: (res) => {
	            // Convert data to JSON
	            const jsonData = JSON.stringify(res.data.data);
	
	            // Create a Blob with the JSON data
	            const blob = new Blob([jsonData], { type: 'application/json' });
	
	            // Create a temporary URL for the Blob
	            const url = window.URL.createObjectURL(blob);
	
	            // Create a link element
	            const link = document.createElement('a');
	            link.href = url;
	            link.setAttribute('download', 'data.json');
	
	            // Simulate click to trigger download
	            document.body.appendChild(link);
	            link.click();
	
	            // Cleanup
	            document.body.removeChild(link);
	            window.URL.revokeObjectURL(url);
	          },
	          fail: (err) => {
	            console.error('Failed to fetch data:', err);
	          }
	        });
	      }
	    },
    mounted() {
  // 获取当前用户的用户名
  const username = uni.getStorageSync('name') || '未登录';

  // 发起带有用户名参数的GET请求
  uni.request({
    url: `${config.SERVER_URL}/listdata?username=${username}`, // 将用户名作为查询参数添加到URL中
    method: 'GET',
    success: (res) => {
      // 更新 listData 数组为从后端接收到的数据
      this.listData = res.data.data; // 注意这里修改为 res.data.data
      console.log(this.listData); // 打印接收到的数据，确保数据已经正确获取
    },
    fail: (err) => {
      console.error('Failed to fetch data:', err);
    }
  });
}
  }
</script>

<style lang="scss">
.out{
	position: relative;
	.default{
		position: absolute;
		left: 50rpx;
		top: 60rpx;
		height: 120rpx;
		width: 120rpx;
	}
	.personalDetail{
		position: absolute;
		left: 220rpx;
		top: 60rpx;
		.name{
			font-size: 35rpx;
		}
		.name2{
			margin-top: 30rpx;
			font-size: 25rpx;
		}
	}
}
.line{
	position: absolute;
	top: 200rpx;
	width: 750rpx;
	height: 10rpx;
	background-color: #E5E5E5;
}
.user-info {
  display: flex;
  align-items: center;
  margin-top: 20rpx;
}

.user-avatar {
  width: 150rpx;
  height: 150rpx;
  border-radius: 50%;
}

.user-name {
  font-size: 32rpx;
  color: #333;
  margin-left: 20rpx;
}

.file-info {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}

.btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.item-image {
  width: 100px;
  height: 100px;
  margin-right: 10px;
}

.item-details {
  display: flex;
  flex-direction: column;
}

.record-place,
.type,
.is_backward,
.energy-consumption,
.extraInfo,
.record-time {
  margin-bottom: 5px;
}

</style>
