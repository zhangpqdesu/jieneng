<template>
	<view>
		<view class="search">
			<image src="../../static/search.png" mode="aspectFit" class="search-img"></image>
			<input class="search-input" type="input" placeholder="搜索" v-model="searchContent" />
		</view>
		
		<view class="box">
			<view class="nameCompany">{{company}}</view>
			<view class="modify" @click="modify">修改公司名称</view>
			<image src="../../static/home-company.png" mode="aspectFit" class="homeCompany"></image>
		</view>
		
		<view class="selectAll">
			<!-- 扫描 -->
			<view class="select" @click="clickScan">
				<view class="block" style="background-color: #DEEEFF;">
					<image src="/static/scan-select.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">扫描</text>
			</view>
			<!-- 照片 -->
			<view class="select" @click="clickPhoto">
				<view class="block" style="background-color: #FFECE8;">
					<image src="/static/photo.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">照片</text>
			</view>
			<!-- 文件 -->
			<view class="select" @click="clickFile">
				<view class="block" style="background-color: #FFF5D7;">
					<image src="/static/file.png" mode="aspectFit" class="scanSelect"></image>
				</view>
				<text class="text">文件</text>
			</view>
			<!-- 历史列表 -->
			<view class="select" @click="clickHistory">
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
				searchContent: "",
				imageList: [],  // 用于存储已选择的图片信息
				company:''
			};
		},
		onShow() {
		    // 从本地存储中获取参数
		    this.company = uni.getStorageSync('company') || '';
		    // 清空本地存储，确保下一次可以重新设置
		    uni.removeStorageSync('company');
		},
		methods:{
			modify(){
				uni.navigateTo({
					url:'/pages/company/company'
				})
			},
			clickScan(){
				uni.switchTab({
					url:'/pages/camera/camera'
				})
			},
			clickPhoto() {
			    uni.chooseImage({
			        count: 9,  // 最多选择9张图片
			        sizeType: ['compressed'],
			        sourceType: ['album', 'camera'],
			        success: (res) => {
						console.log('选择成功')
						// 将选择的图片信息添加到imageList中
						this.imageList = this.imageList.concat(res.tempFilePaths.map(path => ({
							url: path,
							file: { path },  // 创建一个包含 path 的对象
						})));
						// 上传图片
						this.imageList.forEach((image, index) => {
							uni.uploadFile({
								url: 'http://127.0.0.1:5000/upload',  // 后端接口地址
								filePath: image.file.path,  // 使用 path 属性
								name: 'file',
								formData: {
						            // 可以添加其他参数
								},
								success: (res) => {
						            // 上传成功后的处理
						            console.log(`第${index + 1}张图片上传成功`, res);
						            // 这里可以根据后端返回的数据进行相应的处理
									uni.navigateTo({
										url:'/pages/result/result'
									})
								},
								fail: (err) => {
						            console.error(`第${index + 1}张图片上传失败`, err);
								},
							});
						});
			        },
			        fail: (err) => {
			           console.error('选择图片失败', err);
			        },
			    });
			},
			clickFile(){
				uni.navigateTo({
					url:'/pages/handleFile/handleFile'
				})
			},
			clickHistory(){
				uni.navigateTo({
					url:'/pages/checkHistoryRecords/checkHistoryRecords'
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
