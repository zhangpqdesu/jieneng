<template>
	<view>
		<view class="out">
			<image class="default" src="/static/photo/default.png" mode="aspectFit"></image>
			<view class="personalDetail">
				<view class="name">{{name}}</view>
				<view class="name2">{{name2}}</view>
			</view>  
		</view>
		
		<view class="line"></view>
	  
	  
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
      lisiData: [] ,// Initialize an empty array to store data from the backend
	  name:'',
	  name2:'普通用户'
    };
  },
  onShow(){
  	this.name = uni.getStorageSync('name') || '未登录';
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
.energy-consumption,
.record-time {
  margin-bottom: 5px;
}

</style>
