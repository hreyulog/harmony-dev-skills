# 鸿蒙元服务配置文件详解

## app.json5 完整配置

```json
{
  "app": {
    "bundleName": "com.example.myapp",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:app_icon",
    "label": "$string:app_name",
    "description": "$string:app_desc",
    "minCompatibleVersionCode": 1000000,
    "targetAPIVersion": 10,
    "apiReleaseType": "Release",
    "debug": false,
    "bundleType": "atomicService",
    "virtualMachine": "ark",
    "compileSdkType": "HarmonyOS",
    "compileSdkVersion": "4.0.0",
    "compileSdkVersionCanOverride": true
  }
}
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| bundleName | 是 | 应用包名，至少三段 |
| vendor | 是 | 开发者名称 |
| versionCode | 是 | 版本号，递增 |
| versionName | 是 | 版本名称 |
| icon | 是 | 应用图标 |
| label | 是 | 应用名称 |
| bundleType | 是 | 必须为 `atomicService` |
| targetAPIVersion | 否 | 目标API版本 |

## module.json5 完整配置

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "description": "$string:module_desc",
    "mainElement": "EntryAbility",
    "deviceTypes": [
      "phone",
      "tablet",
      "2in1"
    ],
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
        "startWindowIcon": "$media:startIcon",
        "startWindowBackground": "$color:start_window_background",
        "exported": true,
        "skills": [
          {
            "entities": ["entity.system.home"],
            "actions": ["action.system.home"]
          }
        ]
      }
    ],
    "extensionAbilities": [
      {
        "name": "EntryFormAbility",
        "srcEntrance": "./ets/entryformability/EntryFormAbility.ts",
        "label": "$string:widget_name",
        "description": "$string:widget_desc",
        "type": "form",
        "exported": true,
        "metadata": [
          {
            "name": "ohos.extension.form",
            "resource": "$profile:form_config"
          }
        ]
      }
    ],
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      },
      {
        "name": "ohos.permission.GET_NETWORK_INFO"
      }
    ]
  }
}
```

## form_config.json 卡片配置

```json
{
  "forms": [
    {
      "name": "WidgetCard",
      "displayName": "$string:widget_name",
      "description": "$string:widget_desc",
      "src": "./ets/widget/pages/WidgetCard.ets",
      "uiSyntax": "arkts",
      "window": {
        "designWidth": 720,
        "autoDesignWidth": true
      },
      "colorMode": "auto",
      "isDefault": true,
      "updateEnabled": true,
      "scheduledUpdateTime": "10:30",
      "updateDuration": 1,
      "defaultDimension": "2*2",
      "supportDimensions": [
        "2*2",
        "2*4",
        "4*4"
      ],
      "formConfigAbility": "ability://EntryFormAbility",
      "formVisibleNotify": true,
      "metadata": {
        "customizeData": [
          {
            "name": "theme",
            "value": "light"
          }
        ]
      }
    }
  ]
}
```

### 卡片尺寸计算

| 尺寸 | 像素 (720设计稿) | 说明 |
|------|------------------|------|
| 1*2 | 1/4行, 1/2列 | 小卡片 |
| 2*2 | 1/2行, 1/2列 | 标准卡片 |
| 2*4 | 1/2行, 1列 | 横向卡片 |
| 4*4 | 1行, 1列 | 大卡片 |

## main_pages.json 页面路由

```json
{
  "src": [
    "pages/Index",
    "pages/List",
    "pages/Detail"
  ]
}
```

## 常用权限配置

```json
{
  "requestPermissions": [
    {
      "name": "ohos.permission.INTERNET",
      "reason": "$string:permission_internet_reason",
      "usedScene": {
        "abilities": ["EntryAbility"],
        "when": "always"
      }
    },
    {
      "name": "ohos.permission.GET_NETWORK_INFO",
      "reason": "$string:permission_network_reason"
    },
    {
      "name": "ohos.permission.LOCATION",
      "reason": "$string:permission_location_reason",
      "usedScene": {
        "abilities": ["EntryAbility"],
        "when": "inuse"
      }
    },
    {
      "name": "ohos.permission.APPROXIMATELY_LOCATION",
      "reason": "$string:permission_location_reason"
    },
    {
      "name": "ohos.permission.CAMERA",
      "reason": "$string:permission_camera_reason"
    },
    {
      "name": "ohos.permission.READ_MEDIA",
      "reason": "$string:permission_media_reason"
    },
    {
      "name": "ohos.permission.WRITE_MEDIA",
      "reason": "$string:permission_media_reason"
    }
  ]
}
```

## 资源文件结构

```
resources/
├── base/
│   ├── element/
│   │   ├── color.json         # 颜色
│   │   └── string.json        # 字符串
│   ├── media/
│   │   ├── app_icon.png       # 应用图标
│   │   └── startIcon.png      # 启动图标
│   └── profile/
│       ├── main_pages.json    # 页面路由
│       └── form_config.json   # 卡片配置
├── rawfile/
│   ├── video.mp4              # 视频文件
│   └── data.json              # 数据文件
├── en_US/                     # 英文资源
│   └── element/
│       └── string.json
└── zh_CN/                     # 中文资源
    └── element/
        └── string.json
```

## string.json 示例

```json
{
  "string": [
    {
      "name": "app_name",
      "value": "我的元服务"
    },
    {
      "name": "app_desc",
      "value": "这是一个示例元服务"
    },
    {
      "name": "widget_name",
      "value": "服务卡片"
    },
    {
      "name": "widget_desc",
      "value": "展示重要信息"
    },
    {
      "name": "permission_internet_reason",
      "value": "用于获取网络数据"
    }
  ]
}
```

## color.json 示例

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
    },
    {
      "name": "text_primary",
      "value": "#182431"
    },
    {
      "name": "text_secondary",
      "value": "#99182431"
    },
    {
      "name": "divider_color",
      "value": "#33182431"
    }
  ]
}
```

## build-profile.json5

```json
{
  "apiType": "stageMode",
  "buildOption": {
    "externalNativeOptions": {
      "path": "./src/main/cpp/CMakeLists.txt",
      "arguments": "",
      "cppFlags": ""
    }
  },
  "targets": [
    {
      "name": "default",
      "runtimeOS": "HarmonyOS"
    }
  ]
}
```
