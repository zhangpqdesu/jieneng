<template>
	<view class="out">
		<view class="title">欢迎使用</view>
		<view class="subTitle" @click="onClick">已有账号？立即登录>></view>
	
		<view class="box">
			<u-form :model="form" ref="uForm">
				<u-form-item label="姓名" label-position="top" border-bottom="true"><u-input v-model="form.name" placeholder="请输入姓名" /></u-form-item>
				<u-form-item label="手机号" label-position="top" border-bottom="true"><u-input v-model="form.phone" placeholder="请输入手机号" /></u-form-item>
				<u-form-item label="工作单位" label-position="top" border-bottom="true"><u-input v-model="form.workplace" placeholder="请输入工作单位" /></u-form-item>
				<u-form-item label="身份权限" label-position="top" border-bottom="true">
					<picker mode="selector" :range="options" value="selectValue" @change="pickerChange" class="u-input" style="padding-left: 20rpx; padding-top: 10rpx;">
						<view class="option">
							{{options[selectValue]}}
							<text class="triangle">&#x25BC;</text>
						</view>
					</picker>
				</u-form-item>
				<u-form-item label="账号密码" label-position="top" border-bottom="true"><u-input v-model="form.password" placeholder="请输入密码" /></u-form-item>
			</u-form>
			
			<button class="button" hover-class="button2" @click="onSubmit">立即注册</button>
			
			<view class="agree">
			    <u-checkbox-group>
					<u-checkbox @change="clickChecked" v-model="checked" shape="circle" active-color="#FFC300" size="28rpx" />
						已经阅读并同意<span class="highlight">用户协议、隐私政策</span>
					</u-checkbox>
			    </u-checkbox-group>
			</view>
			
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				form: {
					name:"",
					phone:"",
					workplace:"",
					password:""
				},
				options:["普通用户","管理员"],
				selectValue:0,
				checked: false
			};
		},
		methods: {
			onClick(){
				uni.navigateTo({
					url:'/pages/index/index'
				})
			},
			clickChecked(){
				this.checked=!this.checked;
			},
			onSubmit(){
				console.log("check",this.checked);
				// 检查是否同意用户协议
				if(!this.checked){
					uni.showToast({
						title: '请同意用户协议',
						icon: 'none',
						duration: 2000
					});
					return;
				};
				console.log("注册请求数据", this.form);
				// 构造请求函数
				const requestData = {
					name: this.form.name,
					phone: this.form.phone,
					workplace: this.form.workplace,
					identity: this.options[this.selectValue],
					password: this.form.password,
				};
				
				// 发送POST请求
				uni.request({
					url:'http://127.0.0.1:5000/register',
					method: 'POST',
					withCredentials: true,
					data: requestData,
					success: (res) =>{
						console.log(res.data);
						uni.showToast({
							title: '注册成功',
							icon: 'success'
						});
						uni.navigateTo({
							url: '/pages/index/index'
						});
					},
					fail:(err)=>{
						console.error(err);
						uni.showToast({
							title:'注册失败',
							icon:'error'
						})
					}
				});
			},
			pickerChange(e){
				this.selectValue=e.detail.value
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
	flex: auto;
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
	.box{
		margin-top: 120rpx;
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 650rpx;
		height: 1250rpx;
		background-color: rgba(255,255,255,0.5);
		box-shadow: 0px 3px 8px rgba(0,0,0,0.5);
		border-radius: 15px;
		.u-form-item {
			white-space: nowrap; /* 防止文本换行 */
			margin-top: 30rpx;
			margin-left: 40rpx;
			margin-right: 30rpx;
			font-weight: 600;
		}
		.u-input{
			margin-top: 10rpx;
			font-weight: 500;
			border: none !important;
		}
		.option{
			display: flex;
			.triangle {
				margin-left: 400rpx; /* 调整与文本之间的距离 */
			}	
		}
		.button{
			margin-top: 50rpx;
			width:550rpx;
			background-color: rgba(247,183,32,0.8);
			color: #000;
			font-weight: 500;
			font-size: 35rpx;
			border-radius: 50px;
		}
		.button2{
			margin-top: 50rpx;
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
}
</style>
