<template>
	<view class="out">
		<image :src="list.imgUrl" mode="aspectFit"></image>
		<view class="box1">
			<view class="slide"></view>
			
			<view class="type">
				<view class="item" :class="typeIndex==index ? 'active' : ''" v-for="(item,index) in typeArr" :key="item.id" @click="clickType(index)" style="font-size: 20rpx;">{{item.title}}</view>
			</view>
			
			<view class="box2" v-if="typeIndex==0">
				<view class="content">主轴转速:<input class="input" v-model="list.rpm" />r/s</view>
				<view class="content">主轴流量:<input class="input" v-model="list.flow" /></view>
				<view class="content">滞止压力:<input class="input" v-model="list.press" />V</view>
				<view class="content">修正系数:<input class="input" v-model="list.correction" /></view>
				<view class="content">额定功率:<input class="input" v-model="list.feng_power" />kW</view>
				<view class="content">效率:<input class="input" v-model="list.feng_efficiency" /></view>
			</view>
			<view class="box2" v-else-if="typeIndex==1">
				<view class="content">转速:<input class="input" v-model="list.rotated_speed" />r/min</view>
				<view class="content">效率（%）:<input class="input" v-model="list.efficiency" /></view>
				<view class="content">型号:<input class="input" v-model="list.motor_type" /></view>
				<view class="content">额定功率:<input class="input" v-model="list.power" />kW</view>
				
			</view>
			<view class="box2" v-else>
				<view class="content">主轴转速:<input class="input" v-model="list.rpm" />r/s</view>
				<view class="content">主轴流量:<input class="input" v-model="list.flow" /></view>
				<view class="content">滞止压力:<input class="input" v-model="list.press" />V</view>
				<view class="content">修正系数:<input class="input" v-model="list.correction" /></view>
			</view>
			
			<view class="line"></view>
			<image class="import" src="/static/photo/导入.png" mode="aspectFit" @click="clickImport"></image>
			
			<view class="result" v-model="list.batch">
				<view>能效等级：</view>
				<view style="font-weight: bold;">{{list.grade}}</view>
			</view>
			<view class="result" v-model="list.batch">
				<view>是否淘汰：</view>
				<view style="font-weight: bold;">{{list.is_backward}}</view>
			</view>
			<view class="result" v-model="list.batch">
				<view>来源：</view>
				<view style="font-weight: bold;">{{list.batch}}</view>
			</view>
			
			<view class="flip">
				<button class="button" hover-class="button2">上一页</button>
				<button class="button" hover-class="button2">下一页</button>
			</view>
			
			<button class="return" hover-class="return2" @click="clickReturn">返回首页</button>
			
		</view>
	</view>
</template>

<script>
	export default {
		mounted() {
		    // 在 mounted 钩子中获取 OCR 结果参数并展示
		    var ocrResult = uni.getStorageSync('ocrResult');
			var imgUrl = uni.getStorageSync('imgUrl');
		    if (ocrResult && imgUrl) {
		        // 展示 OCR 结果中的参数
		        console.log('efficiency:', ocrResult.efficiency);
		        console.log('power:', ocrResult.power);
				console.log('rotated_speed:', ocrResult.rotated_speed);
				console.log('motor_type:',ocrResult.motor_type);
		        console.log('imgUrl:',imgUrl);
				this.list.efficiency = ocrResult.efficiency;
		        this.list.power = ocrResult.power;
		        this.list.rotated_speed = ocrResult.rotated_speed;
				this.list.motor_type=ocrResult.motor_type;
				this.list.imgUrl=imgUrl;
				this.sendData();
				// 成功获取并展示 OCR 结果后删除缓存数据
				uni.removeStorageSync('ocrResult');
				uni.removeStorageSync('imgUrl');
				console.log('缓存数据已删除');

		    } else {
		        console.error('未获取到 OCR 结果');
		    }
		},
		onShow() {
			uni.startPullDownRefresh();
		},
		data() {
			return {
				typeArr:[
					{id:1,title:"风机"},
					{id:2,title:"电机"},
					{id:3,title:"水泵"}
				],
				
				typeIndex:0,
				list:{
					efficiency:"",
					power:"",
					rotated_speed:"",
					motor_type:"",
					rpm:"",
					flow:"",
					press:"",
					correction:"",
					power:"",
					batch:"",
					grade:"",
					is_backward:"",
					imgUrl:"",
				}
			};
		},
		
		methods:{
			clickImport(){
				uni.switchTab({
					url:'/pages/personalCenter/personalCenter'
				})
			},
			clickType(e){
				this.typeIndex=e
			},
			clickReturn(){
				uni.switchTab({
					url:'/pages/home/home'
				})
			},
			async sendData() {
			    try {
			        const response = await fetch('http://127.0.0.1:5000/is_backward', {
			            method: 'POST',
			            headers: {
			                'Content-Type': 'application/json'
			            },
			            body: JSON.stringify(this.list)
			        });
			
			        if (!response.ok) {
			            throw new Error('Network response was not ok');
			        }
			
			        // 处理后端返回的数据
			        const responseData = await response.json();
			        console.log(responseData);
			
			        // 更新页面上的 is_backward 和 batch
			        this.list.is_backward = responseData.is_backward;
			        this.list.batch = responseData.batch;
			
			    } catch (error) {
			        console.error('Error:', error);
			    }
			}

		}
	}
</script>

<style lang="scss">
.out{
	position: relative;
	height: 100vh;
	.image{
		width: 750rpx;
		height: 50%;
	}
	.box1{
		width: 750rpx;
		height: 1000rpx;
		position: absolute;
		bottom: 0;
		border-top-left-radius: 15px;
		border-top-right-radius: 15px;
		background-color: #fff;
		box-shadow: 0px -10px 10px rgba(0,0,0,0.5);
		.slide{
			position: absolute;
			left: 50%;
			transform: translate(-50%, -50%);
			width: 80rpx;
			height: 10rpx;
			border-radius: 15px;
			background-color: #979797;
			margin-top: 25rpx;
		}
		.type{
			margin-top: 80rpx;
			padding-left: 10%;
			padding-right: 10%;
			display: flex;
			justify-content: space-around;
			align-items: center;
			.item{
				width: 70rpx;
				height: 70rpx;
				border-radius: 50%;
				background-color: #fff;
				display: flex;
				justify-content: center;
				align-items: center;
				&.active{
					background-color: rgba(255, 141, 26, 0.73);
					color: #fff;
					font-size: 22rpx !important;
				}
			}
			.circle{
				width: 70rpx;
				height: 70rpx;
				border-radius: 50%;
				background-color: rgba(255, 141, 26, 0.73);
				display: flex;
				justify-content: center;
				align-items: center;
				.text{
					width: 40rpx;
					height: 40rpx;
					font-size: 20rpx;
					line-height: 40rpx;
				}
			}
		}
		.box2{
			width: 680rpx;
			height: 300rpx;
			border-color: #E5E5E5;
			background-color: #fff;
			box-shadow: 0px 2px 5px rgba(0,0,0,0.4);
			border-radius: 30px;
			position: absolute;
			left: 50%;
			transform: translateX(-50%);
			margin-top: 40rpx;
			display: flex;
			flex-wrap: wrap; //允许换行
			justify-content: flex-start;
			padding-left: 60rpx;
			padding-top: 10%;
			.content{
				display: flex;
				width: 50%;
				text-align: left;
				font-size: 28rpx;
				font-weight: bold;
				text-align: left;
			}
			
			.content input{
				margin-left: 20rpx;
				margin-right: 20rpx;
				width: 80rpx;
				position: relative;
				padding-bottom: 5rpx;
				font-weight: 500 !important;
			}
			.content input::after{
				content: '';
				display: block;
				width: 100%;
				height: 1px;
				background-color: #cecece;
				position: absolute;
				bottom: 25%;
				left: 0;
			}
		}
		.line{
			margin-top: 60%;
			width: 750rpx;
			height: 10rpx;
			background-color: #E5E5E5;
			margin-bottom: 60rpx;
			position: relative;
		}
		.import{
			margin-top: 15%;
			width: 100rpx;
			height: 100rpx;
			display: flex;
			position: absolute;
			top: 50%; /* 将 .import 定位到 .line 的中间 */
			left: 50%;
			transform: translate(-50%, -50%); /* 调整位置 */
			z-index: 1;
		}
		.result{
			font-size: 30rpx;
			display: flex;
			margin-top: 30rpx;
			justify-content: center; /* 水平居中 */
		}
		.flip{
			margin-top: 20rpx;
			display: flex;
			justify-content: space-around;
			align-items: center;
			.button{
				justify-content: center; /* 水平居中 */
				width: 30%;
				height: 60rpx;
				background-color: rgba(255, 141, 26, 0.73);
				color: #fff;
				font-size: 30rpx;
				display: flex;
				align-items: center;
				margin-top: 20rpx;
			}
			.button2{
				justify-content: center; /* 水平居中 */
				width: 30%;
				height: 60rpx;
				background-color: rgba(255, 141, 26, 0.4);
				color: #fff;
				font-size: 30rpx;
				display: flex;
				align-items: center;
				margin-top: 20rpx;
			}
		}
		.return{
			justify-content: center; /* 水平居中 */
			width: 30%;
			height: 60rpx;
			background-color: rgba(255, 141, 26, 0.73);
			color: #fff;
			font-size: 30rpx;
			display: flex;
			align-items: center;
			margin-top: 30rpx;
		}
		.return2{
			justify-content: center; /* 水平居中 */
			width: 30%;
			height: 60rpx;
			background-color: rgba(255, 141, 26, 0.4);
			color: #fff;
			font-size: 30rpx;
			display: flex;
			align-items: center;
			margin-top: 30rpx;
		}
	}
}
</style>
