<template>
	<view class="box">
		<view class="title">请输入公司名称</view>
		
		<view class="box">
			<view class="subTitle">公司名称</view>
			<input class="input" type="input" placeholder="请输入公司名称" v-model="company" />
			<button class="button" hover-class="button2" @click="onSubmit">确认</button>
		</view>
		
		<!-- 图片 -->
		<image src="/static/company1.png" mode="aspectFit" class="image1"></image>
		<image src="/static/company2.png" mode="aspectFit" class="image2"></image>
		<image src="/static/company3.png" mode="aspectFit" class="image3"></image>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				company:''
			};
		},
		methods:{
			onSubmit(){
				uni.setStorageSync('company', this.company);
				uni.switchTab({
					url:'/pages/home/home'
				})
			}
		}
	}
</script>

<style lang="scss">
page{
	background-image: linear-gradient(to bottom, rgba(255, 235, 59, 0.14), rgba(163, 255, 51, 0.23));
}
.box{
	overflow: hidden;
	.title{
		text-align: center;
		background-color: #fdfce2;
		font-size: 50rpx;
		font-weight: bold;
		padding-top: 100rpx;
		margin-top: 80rpx;
	}
	.box{
		margin-top: 60rpx;
		position: absolute;
		top: 40%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 650rpx;
		height: 600rpx;
		background-color: rgba(255,255,255,0.5);
		box-shadow: 0px 3px 8px rgba(0,0,0,0.5);
		border-radius: 15px;
		.subTitle{
			text-align: center;
			padding-top: 80rpx;
		}
		.input{
			position: absolute;
			left: 50%;
			transform: translate(-50%, -50%);
			width:550rpx;
			height: 100rpx;
			background-color: rgba(204,204,204,0.3);
			border-radius: 50px;
			margin-top: 120rpx;
			text-align: center !important;
		}
		.button{
			margin-top: 280rpx;
			width:400rpx;
			background-color: rgba(247,183,32,0.8);
			color: #000;
			font-weight: 500;
			font-size: 35rpx;
			border-radius: 50px;
		}
		.button2{
			margin-top: 280rpx;
			width:400rpx;
			background-color: rgba(247,183,32,0.4);
			color: rgba(0,0,0,0.4);
			font-weight: 500;
			font-size: 35rpx;
			border-radius: 50px;
		}
	}
	.image1{
		position: absolute;
		bottom: -40%;
		left: -20%;
		width: 75%;
		height: 75%;
		object-fit: cover;
		image-rendering: pixelated;
	}
	.image2{
		position: absolute;
		bottom: 0%;
		left: 30%;
		width: 40%;
		height: 40%;
		object-fit: cover;
		image-rendering: pixelated;
	}
	.image3{
		position: absolute;
		bottom: -35%;
		right: -10%;
		width: 65%;
		height: 65%;
		object-fit: cover;
		image-rendering: pixelated;
	}
}
</style>
