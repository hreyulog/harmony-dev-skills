---
name: harmonyos-atomic-service
description: 鸿蒙元服务开发指南。用于从零创建HarmonyOS Atomic Service（元服务）。当用户想要：(1) 创建新的鸿蒙元服务项目 (2) 开发服务卡片Widget (3) 构建免安装的轻量级应用 (4) 学习ArkTS/ArkUI开发元服务时触发。支持完整的项目结构、卡片开发、生命周期管理、上架流程。
---

# 鸿蒙元服务开发

元服务（Atomic Service）是HarmonyOS提供的一种免安装、轻量级应用形态，支持服务卡片、跨设备分发。

## 核心概念

- **免安装**：用户无需下载安装即可使用
- **服务卡片**：桌面Widget，展示关键信息
- **跨设备**：支持1+8+N设备运行
- **轻量级**：单个HAP包不超过2MB

## 项目结构

```
MyAtomicService/
├── AppScope/
│   └── app.json5              # 应用全局配置
├── entry/
│   ├── src/main/
│   │   ├── ets/
│   │   │   ├── entryability/
│   │   │   │   └── EntryAbility.ets    # 主入口
│   │   │   ├── entryformability/
│   │   │   │   └── EntryFormAbility.ets # 卡片生命周期
│   │   │   ├── pages/
│   │   │   │   └── Index.ets           # 主页面
│   │   │   └── widget/
│   │   │       └── pages/
│   │   │           └── WidgetCard.ets  # 卡片UI
│   │   ├── resources/
│   │   │   ├── base/
│   │   │   │   ├── element/            # 字符串、颜色等
│   │   │   │   ├── media/              # 图片资源
│   │   │   │   └── profile/
│   │   │   │       └── form_config.json # 卡片配置
│   │   │   └── rawfile/                # 原始文件（视频等）
│   │   └── module.json5                # 模块配置
│   └── build-profile.json5
└── build-profile.json5
```

## 快速开始

### 1. 创建项目

在DevEco Studio中：
1. File > New > Create Project
2. 选择 "Atomic Service" 模板
3. 配置项目名称和包名

### 2. 配置app.json5

```json
{
  "app": {
    "bundleName": "com.example.myatomic",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "bundleType": "atomicService"
  }
}
```

**关键：** `bundleType` 必须为 `"atomicService"`

### 3. 配置module.json5

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "deliveryWithInstall": true,
    "installationFree": true,
    "extensionAbilities": [
      {
        "name": "EntryFormAbility",
        "srcEntrance": "./ets/entryformability/EntryFormAbility.ts",
        "label": "$string:widget_name",
        "description": "$string:widget_desc",
        "type": "form",
        "metadata": [
          {
            "name": "ohos.extension.form",
            "resource": "$profile:form_config"
          }
        ]
      }
    ]
  }
}
```

## 页面开发 (ArkUI)

### 基础页面示例

```typescript
@Entry
@Component
struct Index {
  @State message: string = '欢迎使用元服务'

  build() {
    Column() {
      Text(this.message)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 50 })

      Button('开始使用')
        .width('80%')
        .height(50)
        .margin({ top: 30 })
        .onClick(() => {
          // 跳转逻辑
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#F5F5F5')
  }
}
```

### 常用布局组件

| 组件 | 用途 | 示例 |
|------|------|------|
| Column | 垂直布局 | `Column() { ... }` |
| Row | 水平布局 | `Row() { ... }` |
| Flex | 弹性布局 | `Flex({ wrap: FlexWrap.Wrap })` |
| Stack | 层叠布局 | `Stack() { ... }` |
| List | 列表 | `List() { ListItem() { ... } }` |
| Grid | 网格 | `Grid() { GridItem() { ... } }` |
| Scroll | 滚动容器 | `Scroll() { Column() { ... } }` |

### 常用UI组件

```typescript
// 文本
Text('内容')
  .fontSize(16)
  .fontColor(Color.Black)
  .maxLines(2)
  .textOverflow({ overflow: TextOverflow.Ellipsis })

// 图片
Image($r('app.media.logo'))
  .width(100)
  .height(100)
  .objectFit(ImageFit.Cover)

// 按钮
Button('点击')
  .width(200)
  .height(40)
  .backgroundColor('#007DFF')
  .onClick(() => {})

// 输入框
TextInput({ placeholder: '请输入' })
  .width('80%')
  .height(40)
  .onChange((value) => {})

// 视频
Video({
  src: $rawfile('video.mp4'),
  previewUri: $r('app.media.preview')
})
  .width('100%')
  .height(200)
```

### 页面路由

```typescript
import router from '@ohos.router'

// 跳转页面
router.pushUrl({
  url: 'pages/DetailPage',
  params: {
    id: '123',
    name: 'test'
  }
})

// 返回
router.back()

// 获取参数
const params = router.getParams()
```

## 服务卡片开发

### 卡片配置 (form_config.json)

```json
{
  "forms": [
    {
      "name": "WidgetCard",
      "description": "这是一个服务卡片",
      "src": "./ets/widget/pages/WidgetCard.ets",
      "uiSyntax": "arkts",
      "window": {
        "designWidth": 720,
        "autoDesignWidth": true
      },
      "colorMode": "auto",
      "isDefault": true,
      "updateEnabled": true,
      "updateDuration": 1,
      "scheduledUpdateTime": "10:30",
      "defaultDimension": "2*2",
      "supportDimensions": ["2*2", "2*4", "4*4"]
    }
  ]
}
```

### 卡片尺寸

| 尺寸 | 规格 | 适用场景 |
|------|------|----------|
| 1*2 | 小卡片 | 简单信息展示 |
| 2*2 | 四宫格 | 常用 |
| 2*4 | 横条 | 列表信息 |
| 4*4 | 大卡片 | 复杂内容 |

### 卡片UI (WidgetCard.ets)

```typescript
@Entry
@Component
struct WidgetCard {
  @State title: string = '今日天气'
  @State temp: string = '25°C'

  build() {
    Column() {
      Text(this.title)
        .fontSize(16)
        .fontWeight(FontWeight.Bold)

      Text(this.temp)
        .fontSize(32)
        .margin({ top: 10 })

      Button('刷新')
        .fontSize(12)
        .height(30)
        .margin({ top: 10 })
        .onClick(() => {
          postCardAction(this, {
            "action": "call",
            "abilityName": "EntryAbility",
            "params": { "method": "refresh" }
          })
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .padding(10)
  }
}
```

### 卡片生命周期 (EntryFormAbility.ets)

```typescript
import FormExtensionAbility from '@ohos.app.form.FormExtensionAbility'
import formBindingData from '@ohos.app.form.formBindingData'
import formProvider from '@ohos.app.form.formProvider'

export default class EntryFormAbility extends FormExtensionAbility {
  
  // 创建卡片时调用
  onAddForm(want) {
    let data = { 'title': 'Hello', 'value': 'World' }
    return formBindingData.createFormBindingData(data)
  }

  // 更新卡片时调用
  onUpdateForm(formId) {
    let data = { 'title': 'Updated', 'value': 'Data' }
    let formData = formBindingData.createFormBindingData(data)
    formProvider.updateForm(formId, formData)
  }

  // 删除卡片时调用
  onRemoveForm(formId) {
    console.info(`Form removed: ${formId}`)
  }
}
```

### 卡片点击事件

```typescript
// 跳转到应用
postCardAction(this, {
  "action": "router",
  "abilityName": "EntryAbility",
  "params": { "page": "pages/Detail" }
})

// 调用方法
postCardAction(this, {
  "action": "call",
  "abilityName": "EntryAbility",
  "params": { "method": "refreshData" }
})
```

## 数据存储

### 本地存储

```typescript
// Preferences (轻量级)
import preferences from '@ohos.data.preferences'

// 存储
let pref = await preferences.getPreferences(context, 'myStore')
await pref.put('key', 'value')
await pref.flush()

// 读取
let value = await pref.get('key', 'default')

// 应用级存储
@StorageLink('count') count: number = 0
@StorageProp('name') name: string = ''
```

### 网络请求

```typescript
import http from '@ohos.net.http'

let httpRequest = http.createHttp()
let response = await httpRequest.request(
  'https://api.example.com/data',
  {
    method: http.RequestMethod.GET,
    header: { 'Content-Type': 'application/json' }
  }
)
console.log(JSON.stringify(response.result))
```

## 打包上架

### 大小限制

| 类型 | 限制 |
|------|------|
| 单个HAP | ≤ 2MB |
| 同设备所有HAP总和 | ≤ 10MB |
| APP包 | ≤ 4GB |

### 签名配置

1. 生成密钥：Build > Generate Key and CSR
2. 申请证书：AppGallery Connect > 证书管理
3. 申请Profile：AGC > HAP Provision Profile管理
4. 配置签名：File > Project Structure > Signing Configs

### 打包

Build > Build Hap(s)/APP(s) > Build APP(s)

输出：`build/outputs/default/xxx.app`

### 上架流程

1. AppGallery Connect 创建元服务
2. 配置应用信息
3. 上传软件包
4. 填写版本信息
5. 提交审核

## 常见问题

### 1. 项目无法运行
- 检查 `bundleType` 是否为 `"atomicService"`
- 确认 `installationFree` 为 `true`

### 2. 卡片不显示
- 检查 `form_config.json` 配置
- 确认 `extensionAbilities` 配置正确
- 验证卡片尺寸 `supportDimensions`

### 3. 包大小超限
- 压缩图片资源
- 使用WebP格式
- 移除无用资源
- 考虑HSP共享包

### 4. 签名失败
- 确认密钥密码正确
- 检查证书有效期
- 验证Profile文件匹配

## 参考资源

- [华为开发者文档](https://developer.huawei.com/consumer/cn/doc/atomic-guides/atomic-service-development)
- [ArkUI组件参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/arkui-overview-V5)
- [AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html)
