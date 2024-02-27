<template>
	<view class="container" v-show="isShow">
		<bt-cropper ref="cropper" :fileType="'jpg'" :ratio="16/20" :imageSrc="tempImagePath" />
		<view class="footer">
			<view class="btn-1">
				<u-button shape="circle" type="warning" text="重新拍照" @click="close" />
			</view>
			<view class="btn-2">
				<u-button shape="circle" type="primary" text="确定选择" @click="crop" />
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				isShow: false,
				tempImagePath: "",
			}
		},
		methods: {
			// 打开回调函数方法
			open(tempImagePath) {
				this.isShow = true
				this.tempImagePath = tempImagePath
			},
			// 裁剪回调函数方法
			crop() {
				// 通过组件定义的ref调用cropper方法，返回一个promise对象
				this.$refs.cropper.crop().then((res) => {
					let pages = getCurrentPages() //获取当前页面栈实例
					let prevPage = pages[pages.length - 2] //获取上一页面栈实例，-3 == 上上一个页面栈实例
					//返回上一页并传递所需当前页面栈参数
					prevPage.$vm.getChildValue(JSON.stringify({
						tempFilePath: res
					}))
					// 返回页面栈
					uni.navigateBack({
						delta: 1
					})
				})
			},
			// 重新拍照，关闭裁剪
			close() {
				this.isShow = false
				this.$emit('close')
			}
		}
	}
</script>

<style lang="scss" scoped>
	.container {
		/** 外层一定要指定大小 */
		height: 100vh;
		z-index: 20;
 
		.footer {
			width: 100%;
			position: fixed;
			left: 0;
			right: 0;
			bottom: 0;
			z-index: 30;
			background: #000;
			display: flex;
			align-items: center;
			padding-top: 25rpx;
			padding-bottom: 50rpx;
 
			.btn-1,
			.btn-2 {
				width: 40%;
				margin: auto;
			}
		}
	}
</style>
