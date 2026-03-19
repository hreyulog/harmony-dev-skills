# 鸿蒙元服务基础模板

这是一个最简单的鸿蒙元服务项目模板，可以作为起点。

## 文件清单

### AppScope/app.json5
```json
{
  "app": {
    "bundleName": "com.example.myapp",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:app_icon",
    "label": "$string:app_name",
    "bundleType": "atomicService"
  }
}
```

### entry/src/main/module.json5
```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": ["phone", "tablet"],
    "deliveryWithInstall": true,
    "installationFree": true,
    "pages": "$profile:main_pages",
    "abilities": [
      {
        "name": "EntryAbility",
        "srcEntrance": "./ets/entryability/EntryAbility.ts",
        "description": "$string:EntryAbility_desc",
        "icon": "$media:icon",
        "label": "$string:EntryAbility_label",
        "exported": true,
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["action.system.home"]
          }
        ]
      }
    ]
  }
}
```

### entry/src/main/ets/entryability/EntryAbility.ts
```typescript
import UIAbility from '@ohos.app.ability.UIAbility'
import window from '@ohos.window'

export default class EntryAbility extends UIAbility {
  onCreate(want, launchParam) {
    console.info('EntryAbility onCreate')
  }

  onDestroy() {
    console.info('EntryAbility onDestroy')
  }

  onWindowStageCreate(windowStage: window.WindowStage) {
    console.info('EntryAbility onWindowStageCreate')

    windowStage.loadContent('pages/Index', (err, data) => {
      if (err.code) {
        console.error('Failed to load content:', err)
        return
      }
      console.info('Succeeded in loading content')
    })
  }

  onWindowStageDestroy() {
    console.info('EntryAbility onWindowStageDestroy')
  }

  onForeground() {
    console.info('EntryAbility onForeground')
  }

  onBackground() {
    console.info('EntryAbility onBackground')
  }
}
```

### entry/src/main/ets/pages/Index.ets
```typescript
@Entry
@Component
struct Index {
  @State message: string = '欢迎使用鸿蒙元服务'

  build() {
    Column() {
      // 标题
      Text('Hello HarmonyOS')
        .fontSize(28)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 20 })

      // 内容
      Text(this.message)
        .fontSize(16)
        .fontColor('#666666')
        .textAlign(TextAlign.Center)
        .margin({ bottom: 30 })

      // 按钮
      Button('开始使用')
        .width('80%')
        .height(50)
        .fontSize(18)
        .backgroundColor('#007DFF')
        .borderRadius(25)
        .onClick(() => {
          this.message = '点击成功！'
        })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#F5F5F5')
    .padding(20)
  }
}
```

### entry/src/main/resources/base/profile/main_pages.json
```json
{
  "src": ["pages/Index"]
}
```

### entry/src/main/resources/base/element/string.json
```json
{
  "string": [
    {
      "name": "app_name",
      "value": "我的元服务"
    },
    {
      "name": "module_desc",
      "value": "示例元服务模块"
    },
    {
      "name": "EntryAbility_desc",
      "value": "主入口"
    },
    {
      "name": "EntryAbility_label",
      "value": "我的元服务"
    }
  ]
}
```

### entry/src/main/resources/base/element/color.json
```json
{
  "color": [
    {
      "name": "start_window_background",
      "value": "#FFFFFF"
    },
    {
      "name": "primary_color",
      "value": "#007DFF"
    }
  ]
}
```

## 快速创建步骤

1. 在 DevEco Studio 中新建项目
2. 选择 "Empty Ability" 模板
3. 项目类型选择 "Atomic Service"
4. 将上述文件内容替换到对应位置
5. 添加应用图标到 `resources/base/media/app_icon.png`
6. 运行项目

## 注意事项

- 确保 `bundleType` 为 `atomicService`
- 确保 `installationFree` 为 `true`
- 应用图标建议 256x256 像素
- 包名格式：至少三段，如 `com.example.myapp`
