<template>
  <view>
	  <view class="user-info" style="border: 1px solid black; display: flex; align-items: center;">
	        <image class="user-avatar" src="/static/user.jpg"></image>
	        <view style="display: flex; flex-direction: column;">
	          <text class="user-name" style="font-size: 22px; margin-bottom: 10px;">李四</text>
	          <text class="user-role" style="font-size: 16px;">管理员</text>
	        </view>
	      </view>
   <view class="item" v-for="(item, index) in lisiData" :key="index">
     <image class="item-image" :src="`/static/photo/${index + 1}.jpg`"></image>
     <view class="item-details">
       <text class="record-place">记录地址:{{ item.record_place }}</text>
       <text class="type">机器类型:{{ item.type }}</text>
	   <text class="energy-consumption">机器能效：{{ item.energy_consumption }}</text>
       <text class="record-time">记录时间:{{ item.record_time }}</text>
     </view>
   </view>

    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      lisiData: [] // Initialize an empty array to store data from the backend
    };
  },
  mounted() {
    // Make a GET request to the backend API endpoint
    uni.request({
      url: 'http://127.0.0.1:5000/lisidata', // Replace 'your-backend-url' with the actual URL of your backend
      method: 'GET',
      success: (res) => {
        // Update the lisiData array with the data received from the backend
        this.lisiData = res.data;
      },
      fail: (err) => {
        console.error('Failed to fetch data:', err);
      }
    });
  }
}
</script>

<style scoped>
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
.energy-consumption,
.record-time {
  margin-bottom: 5px;
}

</style>
