<template>
	<view>
		<view class="search">
			<image src="../../static/search.png" mode="aspectFit" class="search-img"></image>
			<input class="search-input" type="input" placeholder="搜索" v-model="searchContent" />
		</view>
		
		<view class="box">
			<view class="nameCompany">公司名称</view>
			<view class="modify" @click="modify">修改公司名称</view>
			<image src="../../static/home-company.png" mode="aspectFit" class="homeCompany"></image>
		</view>
		
		<view class="selectAll">
			<!-- 扫描 -->
			<view class="select">
				<view class="block" style="background-color: #DEEEFF;">
					<image src="/static/scan-select.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">扫描</text>
			</view>
			<!-- 照片 -->
			<view class="select">
				<view class="block" style="background-color: #FFECE8;">
					<image src="/static/photo.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">照片</text>
			</view>
			<!-- 文件 -->
			<view class="select">
				<view class="block" style="background-color: #FFF5D7;">
					<image src="/static/file.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">文件</text>
			</view>
			<!-- 历史列表 -->
			<view class="select">
				<view class="block" style="background-color: #E7F6EC;">
					<image src="/static/history.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">历史列表</text>
			</view>
		</view>
		
		<!-- 最近 -->
		<view class="recent">
			最近
		</view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				searchContent: ""
			};
		},
		methods:{
			modify(){
				uni.navigateTo({
					url:'/pages/company/company'
				})
			}
		}
	}
</script>

<style lang="scss">
.search{
	display: flex;
	height: 30rpx;
	margin-top: 30rpx;
	text-align: center;
	.search-img{
		width: 30rpx;
		height: 30rpx;
		position: absolute;
		left: 5%;
		top: 1%;
	}
	.search-input{
		position: absolute;
		left: 55%;
		transform: translate(-50%, -50%);
		width:600rpx;
		height: 30rpx;
		background-color: #F7F8FC;
		border-radius: 50px;
		text-align: center !important;
	}
}
.box{
	width: 700rpx;
	height: 250rpx;
	background-color: #FF8D1A;
	box-shadow: 0px 10px 10px rgba(0,0,0,0.4);
	border-radius: 30px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
	margin-top: 50rpx;
	overflow: hidden;
	.nameCompany{
		color: #fff;
		font-weight: bold;
		position: absolute;
		top: 20%;
		left: 15%;
		font-size: 45rpx;
	}
	.modify{
		color: #fff;
		position: absolute;
		top: 60%;
		left: 15%;
		font-size: 30rpx;
		
	}
	.homeCompany{
		width: 500rpx;
		height: 400rpx;
		position: absolute;
		right: -25%;
		top: -40%;
	}
}
.selectAll{
	display: flex;
	align-content: center;
	justify-content: space-around;
	margin-top: 360rpx;
	.select{
		display: flex;
		flex-direction: column;
		align-items: center;
		.block{
			display: flex;
			justify-content: center;
			align-items: center;
			width: 120rpx;
			height: 120rpx;
			border-radius: 15px;
			.scanSelect{
				width: 55rpx;
				height: 55rpx;
			}
		}
		.text{
			margin-top: 5rpx;
			font-size: 25rpx;
			font-weight: bold;
		}
	}
}
.recent{
	font-size: 30rpx;
	font-weight: bold;
	margin-top: 60rpx;
	margin-left: 40rpx;
}
</style>
