<template>
	<view>
		<button @click="clickScan">拍照</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
			}
		},
		methods: {
			clickScan(){
				uni.scanCode({
					onlyFromCamera: true,
					success: function(res){
						const scannedImagePath = res.path;
						this.cropAndUpload(scannedImagePath);
					},
					fail: (err) =>{
						console.error('扫描失败',err);
					}
				});
			},
			cropAndUpload(imagePath){
				
			}
		}
	}
</script>

<style lang="scss">
	
</style>
