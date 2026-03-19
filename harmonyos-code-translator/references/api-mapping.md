# API 翻译对照表

## 网络请求

### 微信小程序
```javascript
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  data: { id: 1 },
  header: { 'Content-Type': 'application/json' },
  success(res) {
    console.log(res.data)
  },
  fail(err) {
    console.error(err)
  }
})
```

### 鸿蒙 ArkTS
```typescript
import http from '@ohos.net.http'

async function fetchData() {
  let httpRequest = http.createHttp()
  try {
    let response = await httpRequest.request(
      'https://api.example.com/data',
      {
        method: http.RequestMethod.GET,
        extraData: { id: 1 },
        header: { 'Content-Type': 'application/json' }
      }
    )
    console.log(JSON.stringify(response.result))
  } catch (err) {
    console.error(err.message)
  } finally {
    httpRequest.destroy()
  }
}
```

---

## 本地存储

### 微信小程序
```javascript
// 存储
wx.setStorageSync('key', 'value')
wx.setStorage({
  key: 'key',
  data: 'value'
})

// 读取
const value = wx.getStorageSync('key')
wx.getStorage({
  key: 'key',
  success(res) {
    console.log(res.data)
  }
})

// 删除
wx.removeStorageSync('key')
wx.clearStorageSync()
```

### 鸿蒙 ArkTS
```typescript
import preferences from '@ohos.data.preferences'

// 获取Preferences实例
let context = getContext(this) as common.UIAbilityContext
let pref = await preferences.getPreferences(context, 'myStore')

// 存储
await pref.put('key', 'value')
await pref.flush()

// 读取
let value = await pref.get('key', 'defaultValue')

// 删除
await pref.delete('key')
await pref.flush()

// 清空
await pref.clear()
await pref.flush()
```

---

## 页面路由

### 微信小程序
```javascript
// 跳转
wx.navigateTo({
  url: '/pages/detail/detail?id=123'
})

// 重定向
wx.redirectTo({
  url: '/pages/index/index'
})

// 返回
wx.navigateBack({
  delta: 1
})

// 切换Tab
wx.switchTab({
  url: '/pages/index/index'
})
```

### 鸿蒙 ArkTS
```typescript
import router from '@ohos.router'

// 跳转（保留当前页）
router.pushUrl({
  url: 'pages/Detail',
  params: { id: '123' }
})

// 替换当前页
router.replaceUrl({
  url: 'pages/Index'
})

// 返回
router.back()
router.back({ delta: 2 })  // 返回上两级

// 获取参数
let params = router.getParams()
```

---

## 提示框

### 微信小程序
```javascript
// Toast
wx.showToast({
  title: '操作成功',
  icon: 'success',
  duration: 2000
})

// Modal
wx.showModal({
  title: '提示',
  content: '确定删除吗？',
  success(res) {
    if (res.confirm) {
      console.log('确认')
    }
  }
})

// Loading
wx.showLoading({
  title: '加载中'
})
wx.hideLoading()
```

### 鸿蒙 ArkTS
```typescript
import promptAction from '@ohos.promptAction'
import AlertDialog from '@ohos.arkui.advanced.Dialog'

// Toast
promptAction.showToast({
  message: '操作成功',
  duration: 2000
})

// AlertDialog
AlertDialog.show({
  title: '提示',
  message: '确定删除吗？',
  primaryButton: {
    value: '取消',
    action: () => {}
  },
  secondaryButton: {
    value: '确定',
    action: () => {
      console.log('确认')
    }
  }
})

// Loading (使用自定义组件)
// 推荐使用 @State + 自定义Loading组件
```

---

## 图片选择

### 微信小程序
```javascript
wx.chooseImage({
  count: 9,
  sizeType: ['original', 'compressed'],
  sourceType: ['album', 'camera'],
  success(res) {
    const tempFilePaths = res.tempFilePaths
  }
})

wx.chooseMedia({
  count: 9,
  mediaType: ['image', 'video'],
  sourceType: ['album', 'camera'],
  success(res) {
    console.log(res.tempFiles)
  }
})
```

### 鸿蒙 ArkTS
```typescript
import picker from '@ohos.file.picker'
import { BusinessError } from '@ohos.base'

// 选择图片
async function selectImages() {
  let photoSelectOptions = new picker.PhotoSelectOptions()
  photoSelectOptions.MIMEType = picker.PhotoViewMIMETypes.IMAGE_TYPE
  photoSelectOptions.maxSelectNumber = 9

  let photoPicker = new picker.PhotoViewPicker()
  try {
    let result = await photoPicker.select(photoSelectOptions)
    console.log(result.photoUris)
  } catch (err) {
    console.error((err as BusinessError).message)
  }
}
```

---

## 文件上传

### 微信小程序
```javascript
wx.uploadFile({
  url: 'https://api.example.com/upload',
  filePath: tempFilePath,
  name: 'file',
  formData: {
    'userId': '123'
  },
  success(res) {
    console.log(res.data)
  }
})
```

### 鸿蒙 ArkTS
```typescript
import request from '@ohos.request'

async function uploadFile(filePath: string) {
  let uploadConfig: request.UploadConfig = {
    url: 'https://api.example.com/upload',
    header: { 'Content-Type': 'multipart/form-data' },
    method: 'POST',
    files: [
      { filename: 'file', name: 'file', uri: `internal://cache/${filePath}` }
    ],
    data: [
      { name: 'userId', value: '123' }
    ]
  }

  try {
    let uploadTask = await request.uploadFile(getContext(), uploadConfig)
    uploadTask.on('complete', () => {
      console.log('Upload complete')
    })
  } catch (err) {
    console.error(err.message)
  }
}
```

---

## 定位

### 微信小程序
```javascript
wx.getLocation({
  type: 'gcj02',
  success(res) {
    const latitude = res.latitude
    const longitude = res.longitude
  }
})

wx.chooseLocation({
  success(res) {
    console.log(res.name, res.address)
  }
})
```

### 鸿蒙 ArkTS
```typescript
import geoLocationManager from '@ohos.geoLocationManager'

// 获取位置
async function getLocation() {
  let requestInfo: geoLocationManager.SingleLocationRequest = {
    scenario: geoLocationManager.UserRequestScenario.UNSET,
    setting: {
      accuracy: 100,
      timeoutMs: 10000
    }
  }

  try {
    let location = await geoLocationManager.getCurrentLocation(requestInfo)
    console.log(location.latitude, location.longitude)
  } catch (err) {
    console.error(err.message)
  }
}
```

---

## 扫码

### 微信小程序
```javascript
wx.scanCode({
  success(res) {
    console.log(res.result)
  }
})
```

### 鸿蒙 ArkTS
```typescript
import scanBarcode from '@ohos.scanBarcode'
import { BusinessError } from '@ohos.base'

async function scanCode() {
  let options: scanBarcode.ScanOptions = {
    scanTypes: [scanBarcode.ScanType.ALL],
    enableMultiMode: false,
    enableAlbum: true
  }

  try {
    let result = await scanBarcode.startScanForResult(getContext(), options)
    console.log(result.originalValue)
  } catch (err) {
    console.error((err as BusinessError).message)
  }
}
```

---

## 支付

### 微信小程序
```javascript
wx.requestPayment({
  timeStamp: '',
  nonceStr: '',
  package: '',
  signType: 'MD5',
  paySign: '',
  success(res) {
    console.log('支付成功')
  },
  fail(res) {
    console.log('支付失败')
  }
})
```

### 鸿蒙 ArkTS
```typescript
// 需要集成华为支付SDK
// 参考华为IAP Kit文档
import iap from '@ohos.iap'

// 具体实现参考华为官方文档
```

---

## 分享

### 微信小程序
```javascript
// 页面内分享
onShareAppMessage() {
  return {
    title: '分享标题',
    path: '/pages/index/index',
    imageUrl: '/images/share.png'
  }
}

// 按钮分享
<button open-type="share">分享</button>
```

### 鸿蒙 ArkTS
```typescript
// 使用系统分享面板
import share from '@ohos.share'

async function shareContent() {
  let shareData: share.ShareData = {
    text: '分享内容',
    imageUris: ['internal://cache/share.jpg']
  }

  try {
    await share.share(getContext(), shareData)
  } catch (err) {
    console.error(err.message)
  }
}
```

---

## 音视频

### 微信小程序
```html
<!-- 音频 -->
<audio src="{{src}}" controls></audio>

<!-- 视频 -->
<video src="{{src}}" controls></video>
```

### 鸿蒙 ArkTS
```typescript
// 音频播放
import media from '@ohos.multimedia.media'

let audioPlayer = await media.createAVPlayer()
audioPlayer.url = 'internal://cache/audio.mp3'
audioPlayer.on('stateChange', (state) => {
  if (state === 'prepared') {
    audioPlayer.play()
  }
})
await audioPlayer.prepare()

// 视频播放
Video({
  src: $rawfile('video.mp4'),
  controller: this.videoController
})
  .width('100%')
  .height(200)
  .autoPlay(true)
```

---

## WebView

### 微信小程序
```html
<web-view src="{{url}}"></web-view>
```

### 鸿蒙 ArkTS
```typescript
import webview from '@ohos.web.webview'

Web({ src: 'https://example.com', controller: this.webController })
  .width('100%')
  .height('100%')
  .javaScriptAccess(true)
  .domStorageAccess(true)
```
