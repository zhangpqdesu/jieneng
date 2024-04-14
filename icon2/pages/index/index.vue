<template>
	<view class="out">
		<view class="title">你好，欢迎登录</view>
		<view class="subTitle" @click="onClick">未创建账号？立即注册>></view>
		
		<view class="select">
			<view class="item" :class="selectIndex==index ? 'active' : ''" v-for="(item,index) in selectArr" :key="item.id" @click="clickSeclect(index)">{{item.select}}</view>
		</view>
		
		<view class="box">
			<view class="return">
				<view v-if="state" class="text">姓名</view>
			  	<image src="/static/xicon.png" mode="aspectFit" class="image" @click="prompt"></image>
			</view>
			
			<view v-if="state" class="border">
				<input class="block" type="input" placeholder="请输入姓名" v-model="message.username">
			</view>
			
			
			<view v-if="state" class="text2">密码</view>
			
			<view v-if="state" class="border">
				<input class="block" type="password" placeholder="请输入密码" v-model="message.password">
			</view>
		
			
			<button class="button" hover-class="button2" @click="onSubmit">立即登录</button>
			
			<view class="agree">
			    <u-checkbox-group>
					<u-checkbox @change="clickChecked" v-model="checked" shape="circle" active-color="#FFC300" size="40rpx" />
						已经阅读并同意<span class="highlight">用户协议、隐私政策</span>
					</u-checkbox>
			    </u-checkbox-group>
			</view>
			
		</view>
		
		<!-- 图片 -->
		<image src="/static/no1.png" mode="aspectFit" class="image1"></image>
		<image src="/static/no2.png" mode="aspectFit" class="image2"></image>
		
	</view>
	
</template>

<script>
	import config from '../../config.js';
	export default {
		data() {
			return {
				selectArr:[
					{id:1,select:"账号登录"},
					
				],
				selectIndex:0,
				message:{
					username:"",
					password:"",
					phone:"",
					verification:""
				},
				checked: false,
				state: true,
			}
		},
		onLoad() {

		},
		methods: {
			onClick(){
				uni.navigateTo({
					url:'/pages/register/register'
				})
			},
			clickSeclect(e){
				console.log(e)
				this.selectIndex=e
				this.state=!this.state
			},
			clickChecked(){
				this.checked=!this.checked;
			},
			onSubmit(){
				if(!this.checked){
					uni.showToast({
						title: '请同意用户协议',
						icon: 'none',
						duration: 2000
					});
					return;
				};
				console.log(this.message)
				uni.request({
					url: `${config.SERVER_URL}/login`,
					method: 'POST',
					data:{
						name: this.message.username,
						password: this.message.password
					},
					success:(res)=>{
						console.log('连接成功',res);
						// 如果登录成功，再进行页面跳转
						if (res.data.message === '登录成功') {
							console.log(res.data.message)
							uni.showToast({
								title: res.data.message,
								icon: 'success',
								duration: 5000,
								success: () => {
									uni.setStorageSync('name',this.message.username);
									uni.switchTab({
										url: '/pages/home/home'
									});
								}
							});
						}
						else{
							uni.showToast({
								title: res.data.error,
								icon: 'error',
								duration: 2000
							});
						}
					},
					fail:(err)=>{
						console.error('错误', err);
					}
				});
			},
			selected(){
				console.log(this.checkedValue)
				this.checkedValue=!this.checkedValue
			},
			prompt(){
				uni.showModal({
					title: '提示',
					content: '你确定要放弃登录吗？',
					success: function (res) {
						if (res.confirm) {
							console.log('用户点击确定');
							uni.navigateTo({
								url: '/pages/register/register'
							});
						} else if (res.cancel) {
							console.log('用户点击取消');
						}
					}
				});
			}
		}
	}
</script>

<style lang="scss">
page{
	background-image: linear-gradient(to bottom, rgba(255, 235, 59, 0.14), rgba(163, 255, 51, 0.23));
}
.out{
	position: relative;
	width: 100%;
	height: 100vh;
	overflow: hidden;
	background-color: rgba(255,255,255,0.2);
	.title{
		text-align: center;
		background-color: #fdfce2;
		font-size: 50rpx;
		font-weight: bold;
		padding-top: 50rpx;
	}
	.subTitle{
		text-align: center;
		background-color: #fdfce2;
		font-size: 25rpx;
		color: rgba(128,128,128,0.6);
		padding: 10rpx;
	}
	.select{
		background-color: #fdfce2;
		display: flex;
		justify-content: space-around;
		align-items: center;
		padding-top: 100rpx;
		font-weight: 600;
		.item{
			color: #ccc;
			&.active{
				color: #000;
			}
		}
	}
	.box{
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 650rpx;
		height: 800rpx;
		background-color: rgba(255,255,255,0.8);
		box-shadow: 0px 3px 8px rgba(0,0,0,0.5);
		border-radius: 15px;
		.text{
			margin-left: 70rpx;
			margin-top: 80rpx;
			margin-bottom: 80rpx;
			font-size: 35rpx;
			margin-right: 420rpx;
		}
		.text2{
			margin-left: 70rpx;
			margin-top: 100rpx;
			margin-bottom: 80rpx;
			font-size: 35rpx;
		}
		.return{
			display: flex;
			align-items: center; /* 垂直居中对齐 */
			.image{
				width: 30rpx;
				height: 30rpx;
			}
		}
		.border{
			position: absolute;
			left: 50%;
			transform: translate(-50%, -50%);
			width:550rpx;
			height: 100rpx;
			background-color: rgba(204,204,204,0.3);
			border-radius: 50px;
			display: flex;
			.block{
				align-items: center;
				margin: 10px;
			}
			.verification{
				position: absolute;
				font-size: 28rpx;
				right: 5%;
				margin-top: 30rpx;
			}
		}
		.button{
			margin-top: 100px;
			width:550rpx;
			background-color: rgba(247,183,32,0.8);
			color: #000;
			font-weight: 500;
			font-size: 35rpx;
			border-radius: 50px;
		}
		.button2{
			margin-top: 100px;
			width:550rpx;
			background-color: rgba(247,183,32,0.4);
			color: rgba(0,0,0,0.4);
			font-weight: 500;
			font-size: 35rpx;
			border-radius: 50px;
		}
		.agree{
			align-items: center;
			margin-top: 25rpx;
			margin-left: 70rpx;
			font-size: 28rpx;
			color: #808080;
			.highlight{
				color: #FFC300;
				text-decoration: underline;
			}
		}
	}
	.image1{
	    position: absolute;
	    bottom: -2%;
	    left: 5%;
	    width: 28%;
	    height: 28%;
		object-fit: cover;
		image-rendering: pixelated;
	}
	.image2{
		position: absolute;
		bottom: -50%;
		left: 50%;
		width: 80%;
		height: 80%;
		object-fit: cover;
		image-rendering: pixelated;
	}
}
</style>
