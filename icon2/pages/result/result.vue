<template>
	<view class="out">
		<image :src="list.imgUrl" mode="aspectFit"></image>
		<view class="box1">
			<view class="slide"></view>

			<view class="type">
				<view class="item" :class="typeIndex==index ? 'active' : ''" v-for="(item,index) in typeArr"
					:key="item.id" @click="clickType(index)" style="font-size: 20rpx;">{{item.title}}</view>
			</view>

			<view class="box2" v-if="typeIndex==0">
				<view class="content">机号:<input class="input" v-model="list.machine_number" /></view>
				<view class="content">轮毂比:<input class="input" v-model="list.r" /></view>
				<view class="content">型号:<input class="input" v-model="list.type" /></view>
				<view class="content">滞止密度:<input class="input" v-model="list.p1" />m³/s</view>
				<view class="content">圆周速度:<input class="input" v-model="list.u" />m/s</view>
				<view class="content">转速:<input class="input" v-model="list.rotated_speed" />r/min</view>
				<view class="content">容积流量:<input class="input" v-model="list.flowRate" />m³/h</view>
				<view class="content">滞止压力:<input class="input" v-model="list.pressure" />pa</view>
				<view class="content">功率:<input class="input" v-model="list.power" />kW</view>
				<view class="content">效率:<input class="input" v-model="list.efficiency" />%</view>
			</view>
			<view class="box2" v-else-if="typeIndex==1">
				<view class="content">转速:<input class="input" v-model="list.rotated_speed" />r/min</view>
				<view class="content">效率（%）:<input class="input" v-model="list.efficiency" /></view>
				<view class="content">型号:<input class="input" v-model="list.model" /></view>
				<view class="content">额定功率:<input class="input" v-model="list.power" />kW</view>
				<view class="content">出厂时间：<input class="input" v-model="list.run_time" /></view>
				<!-- <view class="content">
				    类型:
				    <select class="content" v-model="list.motor_type_classification">
				      <option value="三相异步电动机">三相异步电动机</option>
				      <option value="电容起动异步电动机">电容起动异步电动机</option>
				      <option value="电容运转异步电动机">电容运转异步电动机</option>
				      <option value="双值电容异步电动机">双值电容异步电动机</option>
				      <option value="空调器风扇用异步电动机">空调器风扇用异步电动机</option>
				      <option value="异步起动三相永磁同步电动机">异步起动三相永磁同步电动机</option>
				      <option value="空调器风扇用无刷直流电动机">空调器风扇用无刷直流电动机</option>
				      <option value="电梯用永磁同步电动机">电梯用永磁同步电动机</option>
				      <option value="变频驱动永磁同步电动机">变频驱动永磁同步电动机</option>
				    </select>
				  </view> -->
			</view>
			<view class="box2" v-else>
				<view class="content">主轴转速:<input class="input" v-model="list.rotated_speed" />r/min</view>
				<view class="content">主轴流量:<input class="input" v-model="list.flowRate">m³/h</view>
				<view class="content">扬程:<input class="input" v-model="list.head" />m</view>
				<view class="content">型号:<input class="input" v-model="list.model" /></view>
				<view class="content">功率:<input class="input" v-model="list.power" />kw</view>
				<view class="content">级数:<input class="input" v-model="list.p1" /></view>
				<view class="content">密度:<input class="input" v-model="list.stage" />kg/m³</view>
				<view class="content">效率:<input class="input" v-model="list.efficiency" />%</view>

			</view>

			<view class="line"></view>

			<image class="import" src="/static/photo/load.png" mode="aspectFit" @click="clickImport"></image>

			<view class="result" v-model="energy_consumption">
				<view>能效等级：</view>
				<view style="font-weight: bold;">{{energy_consumption}}</view>
			</view>
			<view class="result" v-model="list.is_backward">
				<view>是否淘汰：</view>
				<view style="font-weight: bold;">{{list.is_backward}}</view>
			</view>
			<view class="result" v-model="list.batch">
				<view>来源：</view>
				<view style="font-weight: bold;">{{list.batch}}</view>
			</view>
			<view style="font-weight: bold;">备注:<input class="input" v-model="list.extraInfo" /></view>

			<div style="color: grey; font-size: smaller;">请在上方输入您的备注信息</div>
			<!-- <view class="flip">
				<button class="button" hover-class="button2">上一页</button>
				<button class="button" hover-class="button2">下一页</button>
			</view> -->
			<button class="return" @click="save_records">存储数据</button>

			<button class="return" hover-class="return2" @click="clickReturn">返回首页</button>

		</view>
	</view>
</template>

<script>
	import config from '../../config.js';
	export default {
		mounted() {
			// 在 mounted 钩子中获取 OCR 结果参数并展示
			// 从本地存储中获取 ocr 结果
			var ocrResult = uni.getStorageSync('ocrResult');
			console.log('OCR 结果:', ocrResult);

			// 从本地存储中获取图片 URL
			var imgUrl = uni.getStorageSync('imgUrl');
			console.log('图片 URL:', imgUrl);

			// 从本地存储中获取公司名称
			var company = uni.getStorageSync('company');
			console.log('公司名称:', company);

			// 从本地存储中获取用户名
			var username = uni.getStorageSync('name');
			console.log('用户名:', username);

			if (ocrResult && imgUrl) {
				// 根据 typeIndex 判断设备类型并展示参数
				if (ocrResult.typeIndex === 1) {
					// 电机逻辑
					this.list.efficiency = ocrResult.efficiency;
					this.list.power = ocrResult.power;
					this.list.rotated_speed = ocrResult.rotated_speed;
					this.list.model = ocrResult.model;
					this.list.imgUrl = imgUrl;
					this.typeIndex = ocrResult.typeIndex;
					this.list.record_place = company;
					this.list.username = username;
					this.sendData();
					// 成功获取并展示 OCR 结果后删除缓存数据
					uni.removeStorageSync('ocrResult');
					uni.removeStorageSync('imgUrl');
					this.computeMotorEnergyConsumption();
					console.log('缓存数据已删除');
				} else if (ocrResult.typeIndex === 2) {
					// 水泵逻辑
					this.list.rotated_speed = ocrResult.rotated_speed; // 转速
					this.list.flowRate = ocrResult.flowRate; // 流量
					this.list.head = ocrResult.head; // 扬程
					this.list.model = ocrResult.model; // 型号
					this.list.power = ocrResult.power; // 功率
					this.list.stage = ocrResult.stage; // 级数
					this.list.p1 = ocrResult.p1; // 密度
					this.list.efficiency = ocrResult.efficiency; // 效率
					this.list.imgUrl = imgUrl;
					this.typeIndex = ocrResult.typeIndex;
					this.list.record_place = company;
					this.list.username = username;
					this.sendData();
					// 成功获取并展示 OCR 结果后删除缓存数据
					uni.removeStorageSync('ocrResult');
					uni.removeStorageSync('imgUrl');

					console.log('缓存数据已删除');
				} else if (ocrResult.typeIndex === 0) {
					// 风机逻辑
					this.list.machine_number = ocrResult.machine_number; // 机号
					this.list.r = ocrResult.r; // 轮毂比
					this.list.type = ocrResult.type; // 型号
					this.list.p1 = ocrResult.p1; // 密度
					this.list.u = ocrResult.u; // 速度
					this.list.rotated_speed = ocrResult.rotated_speed; // 转速
					this.list.flowRate = ocrResult.flowRate; // 流量
					this.list.pressure = ocrResult.pressure; // 压力
					this.list.power = ocrResult.power; // 功率
					this.list.efficiency = ocrResult.efficiency; // 效率
					this.list.imgUrl = imgUrl;
					this.typeIndex = ocrResult.typeIndex;
					this.list.record_place = company;
					this.list.username = username;
					this.sendData();

					// 成功获取并展示 OCR 结果后删除缓存数据
					uni.removeStorageSync('ocrResult');
					uni.removeStorageSync('imgUrl');

					console.log('缓存数据已删除');
				} else {
					console.error('未获取到 OCR 结果');
				}
			}
		},
		
		onShow() {
			uni.startPullDownRefresh();
		},
		data() {
			return {
				typeArr: [

					{
						id: 0,
						title: "风机"
					},
					{
						id: 1,
						title: "电机"
					},
					{
						id: 2,
						title: "水泵"
					}
				],

				typeIndex: 0,
				energy_consumption: "",
				list: {
					efficiency: "",
					power: "",
					rotated_speed: 0,
					rpm: "",
					flowRate: "",
					pressure: "",
					correction: "",
					power: "",
					batch: "",
					is_backward: "",
					imgUrl: "",
					run_time: "",
					motor_type_classification: "",
					extraInfo: "",
					record_place: "",
					record_time: "",
					name: "",
					head: "",
					model: "",
					machine_number: "",
					r: "",
					type: "",
					p1: "",
					u: "",
					stage:""
				}
			};
		},

		methods: {
			clickImport() {
				this.sendData();
				
					if(this.typeIndex===1)
					{
						this.computeMotorEnergyConsumption();
					}
					if(this.typeIndex===0)
					{
						this.computeVentilationEnergyConsumption();
					}
					if(this.typeIndex===2)
					{
						this.computePumpConsumption();
					}
				
				uni.showToast({
					title: '数据已提交',
					duration: 2000
				});
			},
			clickType(e) {
				this.typeIndex = e
			},
			clickReturn() {
				uni.switchTab({
					url: '/pages/home/home'
				})
			},
			async computeMotorEnergyConsumption() {
			    uni.request({
			        url: config.SERVER_URL + '/query_motor_files',
			        data: {
			            power: this.list.power,
			            efficiency: this.list.efficiency,
			            rotated_speed: this.list.rotated_speed
			        },
			        method: 'GET',
			        success: (res) => {
			            console.log(res.data);
			            // 处理后端返回的数据
			            const responseData = res.data;
			            console.log(responseData);
			            
			            // 更新页面上的能效
			            this.energy_consumption = responseData.energy_consumption;
			        }
			    });
			},
			// 风机
			async computeVentilationEnergyConsumption() {
			    uni.request({
			        url: config.SERVER_URL + '/ventilation_fan',
			        data: {
						machine_number:this.list.machine_number,
						r:this.list.r,
						type:this.list.type,
						p1:this.list.p1,
						u:this.list.u,
						rotated_speed:this.list.rotated_speed,
						flowRate:this.list.flowRate,
						pressure:this.list.pressure,
						power:this.list.power,
						efficiency:this.list.efficiency,
			        },
			        method: 'GET',
			        success: (res) => {
			            console.log(res.data);
			            // 处理后端返回的数据
			            const responseData = res.data;
			            console.log(responseData);
			            
			            // 更新页面上的能效
			            this.energy_consumption = responseData.energy_consumption;
			        }
			    });
			},
			// 水泵
			async computePumpConsumption() {
			    uni.request({
			        url: config.SERVER_URL + '/water_pump',
			        data: {
						rotated_speed:this.list.rotated_speed, // 转速
						flowRate:this.list.flowRate, // 流量
						head:this.list.head, // 扬程
						model:this.list.model, // 型号
						power:this.list.power,// 功率
						stage:this.list.stage, // 级数
						p1:this.list.p1, // 级数
						efficiency:this.list.efficiency, // 效率
			        },
			        method: 'GET',
			        success: (res) => {
			            console.log(res.data);
			            // 处理后端返回的数据
			            const responseData = res.data;
			            console.log(responseData);
			            
			            // 更新页面上的能效
			            this.energy_consumption = responseData.energy_consumption;
			        }
			    });
			},
			async sendData() {
				 uni.request({
				     url: config.SERVER_URL + '/is_backward', //仅为示例，并非真实接口地址。
				    data: JSON.stringify(this.list),
						method: 'POST',
				    header: {
				        'Content-Type': 'application/json' //自定义请求头信息
				    },
				    success: (res) => {
				        console.log(res.data);
				        // 处理后端返回的数据
				        const responseData = res.data;
				        console.log(responseData);
				        
				        // 更新页面上的 is_backward 和 batch
				        this.list.is_backward = responseData.is_backward;
				        this.list.batch = responseData.batch;;
				    }
				}); 
				
			/* 	$.ajax({        
				   url: "http://162.14.67.149:5000/is_backward",
				      context: document.body,
				            cache : false, 
				          data: {        
				        username :  $('#username').val(),
				          password :  $('#password').val(),
				            },      
				     success: function ( data ) {
				               // do something   
							   console.log(data);
				       } 
				   }); */
				/* try {
					const response = await fetch(`${config.SERVER_URL}/is_backward`, {
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
				} */
			},
			async save_records() {
			    try {
			        // 构建需要发送给后端的对象
			        const requestData = {
			            username: this.list.username,  // 替换为真实的用户名或者从页面获取
			            imgUrl: this.list.imgUrl,
			            type: this.typeArr[this.typeIndex].title, // 获取当前选中的类型
			            energy_consumption:this.energy_consumption,
						record_place:this.list.record_place,
						//时间自动指定为发送请求的时间
						
			            is_backward: this.list.is_backward,
			            extraInfo: this.list.extraInfo
			            // 添加其他参数
			        };
			
			       /* const response = await fetch(`${config.SERVER_URL}/save_photo_data`, {
			            method: 'POST',
			            headers: {
			                'Content-Type': 'application/json'
			            },
			            body: JSON.stringify(requestData)
			        });
			        
			        if (!response.ok) {
			            throw new Error('Network response was not ok');
			        }
			
			        // 处理后端返回的数据
			        const responseData = await response.json();
			        console.log(responseData); */
					
					uni.request({
						url: config.SERVER_URL + '/save_photo_data',
					    // url: 'http://162.14.67.149:5000/save_photo_data', //仅为示例，并非真实接口地址。
					    data: JSON.stringify(requestData),
						method: 'POST',
					    header: {
					        'Content-Type': 'application/json' //自定义请求头信息
					    },
					    success: (res) => {
					        console.log(res.data);
					        // 处理后端返回的数据
					        const responseData = res.data;
					        console.log(responseData);
							uni.showToast({
								title: '数据已存储',
								duration: 2000
							});
							
					    }
					}); 
			
			
			        // 更新页面或者执行其他操作
			
			    } catch (error) {
			        console.error('Error:', error);
			    }
			}
		}
	}
</script>


<style lang="scss">
	.out {
		position: relative;
		height: 100vh;

		.image {
			width: 750rpx;
			height: 50%;
		}

		.box1 {
			width: 750rpx;
			height: 1000rpx;
			position: absolute;
			bottom: 0;
			border-top-left-radius: 15px;
			border-top-right-radius: 15px;
			background-color: #fff;
			box-shadow: 0px -10px 10px rgba(0, 0, 0, 0.5);

			.slide {
				position: absolute;
				left: 50%;
				transform: translate(-50%, -50%);
				width: 80rpx;
				height: 10rpx;
				border-radius: 15px;
				background-color: #979797;
				margin-top: 25rpx;
			}

			.type {
				margin-top: 80rpx;
				padding-left: 10%;
				padding-right: 10%;
				display: flex;
				justify-content: space-around;
				align-items: center;

				.item {
					width: 70rpx;
					height: 70rpx;
					border-radius: 50%;
					background-color: #fff;
					display: flex;
					justify-content: center;
					align-items: center;

					&.active {
						background-color: rgba(255, 141, 26, 0.73);
						color: #fff;
						font-size: 22rpx !important;
					}
				}

				.circle {
					width: 70rpx;
					height: 70rpx;
					border-radius: 50%;
					background-color: rgba(255, 141, 26, 0.73);
					display: flex;
					justify-content: center;
					align-items: center;

					.text {
						width: 40rpx;
						height: 40rpx;
						font-size: 20rpx;
						line-height: 40rpx;
					}
				}
			}

			.box2 {
							width: 680rpx;
							height: 300rpx;
							border-color: #E5E5E5;
							background-color: #fff;
							box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.4);
							border-radius: 30px;
							position: absolute;
							left: 50%;
							transform: translateX(-50%);
							margin-top: 40rpx;
							display: flex;
							flex-wrap: wrap; //允许换行
							justify-content: flex-start;
							padding-left: 60rpx;
							padding-top: 8%;
			
							.content {
								margin-top: -10px;
								display: flex;
								width: 50%;
								text-align: left;
								font-size: 25rpx;
								font-weight: bold;
								text-align: left;
								flex-wrap: wrap; /* 让内容自动换行 */
							}
							
			
							.content input {
								margin-left: 0rpx;
								margin-right: 0rpx;
								width: 150rpx;
								position: relative;
								padding-bottom: 5rpx;
								font-weight: 500 !important;
								flex-basis: 50%; /* 每个input占据一半的空间 */
							}
			
							.content input::after {
								content: '';
								display: block;
								width: 100%;
								height: 1px;
								background-color: #cecece;
								position: absolute;
								bottom: 15%;
								left: 0;
							}
						}


			.line {
				margin-top: 60%;
				width: 750rpx;
				height: 10rpx;
				background-color: #E5E5E5;
				margin-bottom: 60rpx;
				position: relative;
			}

			.import {
				margin-top: 15%;
				width: 100rpx;
				height: 100rpx;
				display: flex;
				position: absolute;
				top: 50%;
				/* 将 .import 定位到 .line 的中间 */
				left: 50%;
				transform: translate(-50%, -50%);
				/* 调整位置 */
				z-index: 1;
			}

			.result {
				font-size: 30rpx;
				display: flex;
				margin-top: 30rpx;
				justify-content: center;
				/* 水平居中 */
			}

			.flip {
				margin-top: 20rpx;
				display: flex;
				justify-content: space-around;
				align-items: center;

				.button {
					justify-content: center;
					/* 水平居中 */
					width: 30%;
					height: 60rpx;
					background-color: rgba(255, 141, 26, 0.73);
					color: #fff;
					font-size: 30rpx;
					display: flex;
					align-items: center;
					margin-top: 20rpx;
				}

				.button2 {
					justify-content: center;
					/* 水平居中 */
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

			.return {
				justify-content: center;
				/* 水平居中 */
				width: 30%;
				height: 60rpx;
				background-color: rgba(255, 141, 26, 0.73);
				color: #fff;
				font-size: 30rpx;
				display: flex;
				align-items: center;
				margin-top: 30rpx;
			}

			.return2 {
				justify-content: center;
				/* 水平居中 */
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