<template>
  <view class="out">
		<image class="circle1" src="/static/photo/circle1.png" mode="aspectFit"></image>
		<image class="circle2" src="/static/photo/circle2.png" mode="aspectFit"></image>
		
		<image class="default" src="/static/photo/default.png" mode="aspectFit"></image>
		<view class="personalDetail">
			<view class="name">{{name}}</view>
			<view class="block">
				<image class="V" src="/static/photo/VIP.png" mode="aspectFit"></image>
				<view class="name2">{{name2}}</view>
			</view>
		</view>
		
		<view class="black">
			<button class="button" style="font-size: 24rpx; color: white;">申请管理员/普通用户</button>
		</view>
		
		<view class="box">
			<text class="text">特色服务</text>
			
			<view class="Icon">
				<view class="iconText">
					<image class="icon" src="/static/photo/常见问题.png" mode="aspectFit"></image>
					<text class="Text">常见问题</text>
				</view>
				<view class="iconText">
					<image class="icon" src="/static/photo/意见建议.png" mode="aspectFit"></image>
					<text class="Text">意见建议</text>
				</view>
				<view class="iconText" @click="goToContactUs">
					<image class="icon" src="/static/photo/contactUs.png" mode="aspectFit"></image>
					<text class="Text">联系我们</text>
				</view>
				<view class="iconText" @click="returnIndex">
					<image class="icon" src="/static/photo/退出登录.png" mode="aspectFit"></image>
					<text class="Text">退出登录</text>
				</view>
			</view>
			
			
		</view>
		
  </view>
</template>

<script>
export default {
	data() {
		return {
			name:'',
			name2: '普通用户'
		};
	},
	onShow(){
		this.name = uni.getStorageSync('name') || '未登录';
	},
	methods: {
		goToContactUs() {
			uni.navigateTo({
			url: '/pages/conTactUs/conTactUs' // 假设联系我们页面的路径为 '/pages/contactUs/contactUs'
			});
		},
		returnIndex(){
			uni.navigateTo({
				url:'/pages/index/index'
			})
		}
	}
}
</script>

<style lang="scss">
page{
	background-image: linear-gradient(to bottom, rgba(255, 141, 26, 0.55), rgba(255, 255, 255, 0));
}
.out{
	position: relative;
	.circle1{
		position: absolute;
		left: -400rpx;
		top: 100rpx;
		height: 800rpx;
		width: 800rpx;
	}
	.circle2{
		position: absolute;
		right: -450rpx;
		top: -400rpx;
		height: 1000rpx;
		width: 1000rpx;
	}
	.default{
		position: absolute;
		left: 50rpx;
		top: 250rpx;
		height: 150rpx;
		width: 150rpx;
	}
	.personalDetail{
		position: absolute;
		left: 240rpx;
		top: 280rpx;
		.name{
			font-size: 35rpx;
		}
		.block{
			margin-top: 25rpx;
			width: 200rpx;
			height: 45rpx;
			border-radius: 45rpx;
			background: rgba(255,255,255,0.5);
			display: flex;
			align-items: center;
			.V{
				margin-left: 15rpx;
				width: 32rpx;
				height: 32rpx;
			}
			.name2{
				margin-left: 20rpx;
				font-size: 25rpx;
				color: #F2A922;
			}
		}
	}
	.black{
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		top: 480rpx;
		height: 120rpx;
		width: 600rpx;
		background: linear-gradient(to bottom right, rgba(79,82,99,1), rgba(21,22,33,0.9));
		border-radius: 10px;
		.button{
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%,-50%);
			width: 300rpx;
			height: 40rpx;
			border-radius: 40rpx;
			display: flex;
			justify-content: center;
			align-items: center;
			background: linear-gradient(to bottom right, rgba(239,204,152,1), rgba(222,174,104,0.9));
		}
	}
	.box{
		position: absolute;
		top: 700rpx;
		left: 50%;
		transform: translateX(-50%);
		width: 650rpx;
		height: 600rpx;
		background-color: rgba(255,255,255,0.8);
		box-shadow: 0px 8.5px 25.5px #a2acc2;
		border-radius: 15px;
		.text{
			position: absolute;
			top: 5%;
			left: 5%;
		}
		.Icon{
			margin-top: 150rpx;
			display: flex;
			flex-wrap: wrap;
			justify-content: space-around;
			.iconText{
				display: flex;
			    flex-direction: column; /* 设置元素纵向排列 */
			    align-items: center; /* 可选：居中对齐 */
				width: calc(33.33% - 10px); /* 计算每个元素的宽度，减去间距 */
				margin-bottom: 40px; /* 间距 */
				box-sizing: border-box; /* 让边框和内边距不会撑大元素 */
				.icon{
					width: 60rpx;
					height: 60rpx;
				}
				.Text{
					color: #464a57;
					margin-top: 15rpx;
					font-size: 30rpx;
				}
			}
		}
	}
}
</style>
