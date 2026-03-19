---
name: harmonyos-api-snippets
description: 鸿蒙API代码片段库。当用户需要：(1) 网络请求 (2) 数据存储 (3) 路由导航 (4) 权限申请 (5) 媒体处理 (6) 设备能力调用时触发。提供常用API的即用代码片段。
---

# 鸿蒙 API 代码片段库

常用鸿蒙 API 的即用代码片段，复制粘贴即可使用。

---

## 一、网络请求

### HTTP GET 请求

```typescript
import http from '@ohos.net.http'

async function fetchData(url: string): Promise<string> {
  let httpRequest = http.createHttp()
  try {
    let response = await httpRequest.request(url, {
      method: http.RequestMethod.GET,
      header: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer your_token'
      },
      connectTimeout: 60000,
      readTimeout: 60000
    })
    
    if (response.responseCode === 200) {
      return response.result as string
    }
    throw new Error(`HTTP ${response.responseCode}`)
  } finally {
    httpRequest.destroy()
  }
}

// 使用
let data = await fetchData('https://api.example.com/data')
let json = JSON.parse(data)
```

### HTTP POST 请求

```typescript
async function postData(url: string, body: object): Promise<string> {
  let httpRequest = http.createHttp()
  try {
    let response = await httpRequest.request(url, {
      method: http.RequestMethod.POST,
      header: { 'Content-Type': 'application/json' },
      extraData: body  // 自动序列化
    })
    return response.result as string
  } finally {
    httpRequest.destroy()
  }
}

// 使用
let result = await postData('https://api.example.com/login', {
  username: 'user',
  password: 'pass'
})
```

### 文件上传

```typescript
import request from '@ohos.request'

async function uploadFile(filePath: string, uploadUrl: string): Promise<void> {
  let uploadConfig: request.UploadConfig = {
    url: uploadUrl,
    header: { 'Authorization': 'Bearer token' },
    method: 'POST',
    files: [{ filename: 'file', name: 'file', uri: `internal://${filePath}`, type: 'image/jpeg' }],
    data: [{ name: 'userId', value: '123' }]
  }
  
  let uploadTask = await request.uploadFile(context, uploadConfig)
  
  uploadTask.on('progress', (uploadedSize, totalSize) => {
    console.log(`上传进度: ${uploadedSize}/${totalSize}`)
  })
  
  uploadTask.on('complete', () => {
    console.log('上传完成')
  })
}
```

---

## 二、数据存储

### Preferences (轻量级存储)

```typescript
import preferences from '@ohos.data.preferences'

// 获取 Preferences 实例
async function getPreferences(context: Context) {
  return await preferences.getPreferences(context, 'my_app_store')
}

// 存储数据
async function saveData(context: Context, key: string, value: string | number | boolean) {
  let pref = await getPreferences(context)
  await pref.put(key, value)
  await pref.flush()  // 必须调用 flush 持久化
}

// 读取数据
async function loadData(context: Context, key: string, defaultValue: string = ''): Promise<string> {
  let pref = await getPreferences(context)
  return await pref.get(key, defaultValue) as string
}

// 删除数据
async function deleteData(context: Context, key: string) {
  let pref = await getPreferences(context)
  await pref.delete(key)
  await pref.flush()
}

// 检查是否存在
async function hasKey(context: Context, key: string): Promise<boolean> {
  let pref = await getPreferences(context)
  return await pref.has(key)
}
```

### 关系型数据库 (RdbStore)

```typescript
import relationalStore from '@ohos.data.relationalStore'

// 创建数据库
async function createRdbStore(context: Context): Promise<relationalStore.RdbStore> {
  const config: relationalStore.StoreConfig = {
    name: 'MyDatabase.db',
    securityLevel: relationalStore.SecurityLevel.S1
  }
  
  let rdbStore = await relationalStore.getRdbStore(context, config)
  
  // 创建表
  const sql = `CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    created_at INTEGER
  )`
  await rdbStore.executeSql(sql)
  
  return rdbStore
}

// 插入数据
async function insertUser(rdbStore: relationalStore.RdbStore, name: string, email: string) {
  const valueBucket: relationalStore.ValuesBucket = {
    name: name,
    email: email,
    created_at: Date.now()
  }
  let rowId = await rdbStore.insert('users', valueBucket)
  return rowId
}

// 查询数据
async function queryUsers(rdbStore: relationalStore.RdbStore): Promise<Array<any>> {
  let predicates = new relationalStore.RdbPredicates('users')
  predicates.equalTo('name', '张三')  // 条件
  predicates.orderByDesc('created_at')  // 排序
  predicates.limitAs(10)  // 限制条数
  
  let resultSet = await rdbStore.query(predicates, ['id', 'name', 'email'])
  
  let results: Array<any> = []
  while (resultSet.goToNextRow()) {
    results.push({
      id: resultSet.getLong(resultSet.getColumnIndex('id')),
      name: resultSet.getString(resultSet.getColumnIndex('name')),
      email: resultSet.getString(resultSet.getColumnIndex('email'))
    })
  }
  resultSet.close()
  
  return results
}

// 更新数据
async function updateUser(rdbStore: relationalStore.RdbStore, id: number, newName: string) {
  const valueBucket: relationalStore.ValuesBucket = { name: newName }
  let predicates = new relationalStore.RdbPredicates('users')
  predicates.equalTo('id', id)
  let changed = await rdbStore.update(valueBucket, predicates)
  return changed
}

// 删除数据
async function deleteUser(rdbStore: relationalStore.RdbStore, id: number) {
  let predicates = new relationalStore.RdbPredicates('users')
  predicates.equalTo('id', id)
  let deleted = await rdbStore.delete(predicates)
  return deleted
}
```

---

## 三、路由导航

```typescript
import router from '@ohos.router'

// 跳转页面
function navigateTo(url: string, params?: object) {
  router.pushUrl({
    url: url,
    params: params || {}
  }, router.RouterMode.Standard)
}

// 替换页面（不能返回）
function replaceTo(url: string, params?: object) {
  router.replaceUrl({
    url: url,
    params: params || {}
  })
}

// 返回
function goBack() {
  router.back()
}

// 返回指定页面
function backTo(url: string) {
  router.back({ url: url })
}

// 获取参数
function getRouteParams(): object {
  return router.getParams() as object || {}
}

// 使用示例
// 跳转
navigateTo('pages/Detail', { id: 123, name: 'test' })

// 目标页面获取参数
aboutToAppear() {
  let params = getRouteParams()
  this.itemId = params['id']
}
```

---

## 四、权限申请

```typescript
import abilityAccessCtrl, { Permissions } from '@ohos.abilityAccessCtrl'
import { BusinessError } from '@ohos.base'

// 检查权限
async function checkPermission(context: Context, permission: Permissions): Promise<boolean> {
  let atManager = abilityAccessCtrl.createAtManager()
  try {
    let grantStatus = await atManager.checkAccessToken(
      context.applicationInfo.accessTokenId,
      permission
    )
    return grantStatus === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED
  } catch {
    return false
  }
}

// 请求权限
async function requestPermissions(context: Context, permissions: Permissions[]): Promise<boolean> {
  let atManager = abilityAccessCtrl.createAtManager()
  try {
    let result = await atManager.requestPermissionsFromUser(context, permissions)
    
    // 检查是否全部授权
    for (let i = 0; i < result.authResults.length; i++) {
      if (result.authResults[i] !== 0) {
        return false
      }
    }
    return true
  } catch (err) {
    console.error('请求权限失败:', err)
    return false
  }
}

// 常用权限
const COMMON_PERMISSIONS = {
  INTERNET: 'ohos.permission.INTERNET',
  CAMERA: 'ohos.permission.CAMERA',
  MICROPHONE: 'ohos.permission.MICROPHONE',
  LOCATION: 'ohos.permission.LOCATION',
  READ_MEDIA: 'ohos.permission.READ_MEDIA',
  WRITE_MEDIA: 'ohos.permission.WRITE_MEDIA',
  READ_CALENDAR: 'ohos.permission.READ_CALENDAR',
  WRITE_CALENDAR: 'ohos.permission.WRITE_CALENDAR'
}

// 使用示例
async function checkAndRequestCamera(context: Context): Promise<boolean> {
  let hasPermission = await checkPermission(context, COMMON_PERMISSIONS.CAMERA)
  if (hasPermission) {
    return true
  }
  return await requestPermissions(context, [COMMON_PERMISSIONS.CAMERA])
}
```

---

## 五、提示与弹窗

```typescript
import promptAction from '@ohos.promptAction'
import AlertDialog from '@ohos.alertDialog'

// Toast 提示
function showToast(message: string) {
  promptAction.showToast({
    message: message,
    duration: 2000
  })
}

// 加载提示
async function showLoading(message: string = '加载中...'): Promise<number> {
  return await promptAction.showDialog({
    title: message,
    buttons: []
  })
}

// 关闭提示
function closeLoading(dialogId: number) {
  promptAction.closeDialog(dialogId)
}

// 确认对话框
function showConfirm(
  title: string,
  message: string,
  onConfirm: () => void,
  onCancel?: () => void
) {
  AlertDialog.show({
    title: title,
    message: message,
    buttons: [
      {
        text: '取消',
        color: '#999999',
        action: () => {
          onCancel?.()
        }
      },
      {
        text: '确定',
        color: '#007DFF',
        action: () => {
          onConfirm()
        }
      }
    ]
  })
}

// 操作菜单
function showActionSheet(title: string, buttons: string[], onSelect: (index: number) => void) {
  promptAction.showActionMenu({
    title: title,
    buttons: buttons.map(text => ({ text })),
    show: true
  }).then(result => {
    if (result.index !== undefined) {
      onSelect(result.index)
    }
  })
}
```

---

## 六、图片选择与相机

```typescript
import picker from '@ohos.file.picker'
import camera from '@ohos.multimedia.camera'

// 选择图片
async function pickImages(context: Context, maxCount: number = 9): Promise<Array<string>> {
  let photoPicker = new picker.PhotoViewPicker()
  let result = await photoPicker.select({
    MIMEType: picker.PhotoViewMIMETypes.IMAGE_TYPE,
    maxSelectNumber: maxCount
  })
  return result.photoUris
}

// 选择视频
async function pickVideos(context: Context, maxCount: number = 1): Promise<Array<string>> {
  let photoPicker = new picker.PhotoViewPicker()
  let result = await photoPicker.select({
    MIMEType: picker.PhotoViewMIMETypes.VIDEO_TYPE,
    maxSelectNumber: maxCount
  })
  return result.photoUris
}

// 拍照
async function takePhoto(context: Context): Promise<string> {
  let cameraPicker = new camera.Picker(context)
  let result = await cameraPicker.pick({
    mediaType: [camera.MediaType.PHOTO],
    cameraPosition: camera.CameraPosition.CAMERA_POSITION_BACK
  })
  return result.resultUri
}

// 录像
async function recordVideo(context: Context): Promise<string> {
  let cameraPicker = new camera.Picker(context)
  let result = await cameraPicker.pick({
    mediaType: [camera.MediaType.VIDEO],
    cameraPosition: camera.CameraPosition.CAMERA_POSITION_BACK
  })
  return result.resultUri
}
```

---

## 七、位置服务

```typescript
import geoLocationManager from '@ohos.geoLocationManager'

// 获取当前位置
async function getCurrentLocation(): Promise<{latitude: number, longitude: number}> {
  let location = await geoLocationManager.getCurrentLocation({
    priority: geoLocationManager.LocationRequestPriority.FIRST_FIX,
    scenario: geoLocationManager.LocationRequestScenario.UNSET
  })
  
  return {
    latitude: location.latitude,
    longitude: location.longitude
  }
}

// 持续监听位置
let locationCallbackId: number = -1

function startLocationUpdates(callback: (location: {lat: number, lng: number}) => void) {
  let requestInfo: geoLocationManager.LocationRequest = {
    priority: geoLocationManager.LocationRequestPriority.ACCURACY,
    timeInterval: 5,  // 5秒更新一次
    distanceInterval: 10  // 或移动10米更新
  }
  
  locationCallbackId = geoLocationManager.on('locationChange', requestInfo, (location) => {
    callback({
      lat: location.latitude,
      lng: location.longitude
    })
  })
}

function stopLocationUpdates() {
  if (locationCallbackId !== -1) {
    geoLocationManager.off('locationChange', locationCallbackId)
    locationCallbackId = -1
  }
}

// 地理编码（地址转坐标）
async function geocode(address: string): Promise<{lat: number, lng: number}> {
  let result = await geoLocationManager.getAddressesFromLocationName(address, 1)
  if (result && result.length > 0) {
    return {
      lat: result[0].latitude,
      lng: result[0].longitude
    }
  }
  throw new Error('地址解析失败')
}

// 逆地理编码（坐标转地址）
async function reverseGeocode(lat: number, lng: number): Promise<string> {
  let result = await geoLocationManager.getAddressFromLocation(lat, lng)
  return result.placeName || ''
}
```

---

## 八、传感器

```typescript
import sensor from '@ohos.sensor'

// 加速度传感器
function onAccelerometer(callback: (x: number, y: number, z: number) => void): number {
  return sensor.on(sensor.SensorType.ACCELEROMETER, (data) => {
    callback(data.x, data.y, data.z)
  }, { interval: 100000000 })  // 100ms
}

// 陀螺仪
function onGyroscope(callback: (x: number, y: number, z: number) => void): number {
  return sensor.on(sensor.SensorType.GYROSCOPE, (data) => {
    callback(data.x, data.y, data.z)
  }, { interval: 100000000 })
}

// 计步器
function onStepCounter(callback: (steps: number) => void): number {
  return sensor.on(sensor.SensorType.STEP_COUNTER, (data) => {
    callback(data.steps)
  })
}

// 取消监听
function offSensor(type: sensor.SensorType, sensorId: number) {
  sensor.off(type, sensorId)
}
```

---

## 九、日志

```typescript
import hilog from '@ohos.hilog'

const TAG = 'MyApp'
const DOMAIN = 0x0001

// 不同级别日志
hilog.debug(DOMAIN, TAG, 'Debug message: %{public}s', 'value')
hilog.info(DOMAIN, TAG, 'Info message')
hilog.warn(DOMAIN, TAG, 'Warning: %{public}d', 123)
hilog.error(DOMAIN, TAG, 'Error occurred: %{public}s', 'reason')

// 格式化输出
let userId = 123
let userName = 'Tom'
hilog.info(DOMAIN, TAG, 'User: id=%{public}d, name=%{public}s', userId, userName)
```

---

## 十、应用生命周期

```typescript
// EntryAbility.ets
import UIAbility from '@ohos.app.ability.UIAbility'
import window from '@ohos.window'

export default class EntryAbility extends UIAbility {
  
  onCreate(want, launchParam) {
    // 应用启动时
    hilog.info(0x0001, 'MyApp', 'Ability onCreate')
    
    // 获取启动参数
    let params = want.parameters
    console.log('启动参数:', JSON.stringify(params))
  }

  onDestroy() {
    // 应用销毁时
    console.log('Ability onDestroy')
  }

  onWindowStageCreate(windowStage: window.WindowStage) {
    // 创建窗口
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        console.error('加载页面失败:', err.message)
        return
      }
      console.log('页面加载成功')
    })
  }

  onForeground() {
    // 切换到前台
    console.log('Ability onForeground')
  }

  onBackground() {
    // 切换到后台
    console.log('Ability onBackground')
  }

  onNewWant(want) {
    // 已启动时收到新的启动请求（卡片点击等）
    let method = want.parameters?.method
    console.log('收到新请求:', method)
  }
}
```

---

## 参考资源

- [API参考文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/)
- [应用开发指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/application-dev-guide-V5)
