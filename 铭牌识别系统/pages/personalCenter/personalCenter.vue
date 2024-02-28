<template>
  <view class="container">
    <!-- 用户头像和名称 -->
    <view class="user-info">
      <image class="user-avatar" src="/static/user.jpg"></image>
	  <view style="display: flex; flex-direction: column; align-items: center;">
		  <text class="user-name" style="font-size: 22px; margin-bottom: 10px;">李四</text>
		  <text class="user-role" style="font-size: 16px;text-align: center;">管理员</text>
	  </view>
  </view>
	<view style="position:fixed;top:34%;left:35%;text-align:center">
    <text class="title" style="font-size: 24px;">特色服务</text>
</view>
    <view class="middle-part" style="display:flex ;margin: 20px;position:fixed;top:40% ;">
		<view class="col-md-4" style="display:flex">
			<view style="display: flex; flex-direction: column; align-items: center;">
			    <img src="/static/问号.png" style="width: 40px; height: auto; max-height: 40px;">
			    <text style="margin:10px;text-align:center">常见问题</text>
			</view>
		</view>
		<view class="col-md-4" style="display:flex">
			<view style="display: flex; flex-direction: column; align-items: center;">
			    <img src="/static/留言.png" style="width: 40px; height: auto; max-height: 40px;">
			    <text style="margin:10px;text-align:center">意见建议</text>
			</view>
		</view>
		<view class="col-md-4" style="display:flex">
			<view style="display: flex; flex-direction: column; align-items: center;" @click="goToContactUs">
			    <img src="/static/电话.png" style="width: 40px; height: auto; max-height: 40px;">
			    <text style="margin:10px;text-align:center" >联系我们</text>
			</view>
			<view class="col-md-4" style="display:flex">
				<view style="display: flex; flex-direction: column; align-items: center;">
				    <img src="/static/设置.png" style="width: 40px; height: auto; max-height: 40px;">
				    <text style="margin:10px;text-align:center">退出登录</text>
				</view>
			</view>
		</view>
		
		
	</view>


	

    <view class="bottom-part" style="display: flex; justify-content: space-between; position:fixed; bottom:0; width: 100%;">
        <view class="col-md-4" style="flex: 1;">
            <view style="display: flex; flex-direction: column; align-items: center;">
                <img src="/static/首页.png" style="width: 40px; height: auto; max-height: 40px;">
                <text style="margin:10px;text-align:center">首页</text>
            </view>
        </view>
        <view class="col-md-4" style="flex: 1;">
            <view style="display: flex; flex-direction: column; align-items: center;">
                <img src="/static/扫码.png" style="width: 40px; height: auto; max-height: 40px;">
                <text style="margin:10px;text-align:center">扫一扫</text>
            </view>
        </view>
        <view class="col-md-4" style="flex: 1;">
            <view style="display: flex; flex-direction: column; align-items: center;">
                <img src="/static/个人中心.png" style="width: 40px; height: auto; max-height: 40px;">
                <text style="margin:10px;text-align:center">个人中心</text>
            </view>
        </view>
    </view>


  </view>
</template>

<style scoped>
.user-info {
  display: flex;
  align-items: center;
  margin-top: 20rpx;
}

.user-avatar {
  width: 150rpx;
  height: 150rpx;
  border-radius: 50%;
}

.user-name {
  font-size: 32rpx;
  color: #333;
  margin-left: 20rpx;
}
</style>

<script>
export default {
  methods: {
    goToContactUs() {
      uni.navigateTo({
        url: '/pages/conTactUs/conTactUs' // 假设联系我们页面的路径为 '/pages/contactUs/contactUs'
      });
    }
  }
}
</script>