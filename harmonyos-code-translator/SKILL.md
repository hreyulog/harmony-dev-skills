---
name: harmonyos-code-translator
description: 代码转鸿蒙元服务翻译器。将其他平台/语言的代码翻译为HarmonyOS ArkTS/ArkUI元服务代码。当用户想要：(1) 将微信小程序转为鸿蒙元服务 (2) 将React Native/Flutter代码转鸿蒙 (3) 将Vue/React组件转ArkUI (4) 将iOS/Android原生代码转鸿蒙时触发。提供组件映射、语法对照、架构转换指南。
---

# 代码转鸿蒙元服务翻译器

将其他平台代码翻译为HarmonyOS ArkTS/ArkUI元服务代码。

## 核心映射关系

### 小程序 → 鸿蒙

#### 目录结构对比

| 小程序 | 鸿蒙元服务 |
|--------|-----------|
| pages/ | ets/pages/ |
| components/ | ets/components/ |
| utils/ | ets/common/ |
| app.json | app.json5 + module.json5 |
| app.wxss | resources/base/element/ |

#### 页面结构对比

**小程序 WXML:**
```xml
<view class="container">
  <text>{{message}}</text>
  <button bindtap="handleClick">点击</button>
</view>
```

**鸿蒙 ArkTS:**
```typescript
@Entry
@Component
struct Page {
  @State message: string = 'Hello'

  build() {
    Column() {
      Text(this.message)
      Button('点击')
        .onClick(() => this.handleClick())
    }
    .width('100%')
    .height('100%')
  }

  handleClick() {
    // 处理逻辑
  }
}
```

#### 组件映射表

| 小程序 | 鸿蒙ArkUI | 说明 |
|--------|-----------|------|
| view | Column / Row | 容器组件 |
| text | Text | 文本 |
| image | Image | 图片 |
| button | Button | 按钮 |
| input | TextInput | 输入框 |
| scroll-view | Scroll | 滚动容器 |
| swiper | Swiper | 轮播 |
| list | List | 列表 |
| navigator | (router.pushUrl) | 页面跳转 |
| rich-text | RichText | 富文本 |
| video | Video | 视频 |
| audio | (AVPlayer) | 音频 |
| canvas | Canvas | 画布 |
| map | MapComponent | 地图 |
| web-view | Web | 网页 |
| icon | SymbolGlyph / Image | 图标 |
| progress | Progress | 进度条 |
| slider | Slider | 滑块 |
| switch | Toggle | 开关 |
| picker | (自定义) | 选择器 |
| checkbox | Checkbox | 复选框 |
| radio | Radio | 单选框 |

#### 样式映射

**小程序 WXSS:**
```css
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  background-color: #f5f5f5;
}
.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}
```

**鸿蒙 ArkTS:**
```typescript
Column() {
  Text('Title')
    .fontSize(18)
    .fontWeight(FontWeight.Bold)
    .fontColor('#333')
}
.width('100%')
.height('100%')
.justifyContent(FlexAlign.Center)
.padding(20)
.backgroundColor('#F5F5F5')
```

#### 样式属性映射表

| CSS/WXSS | ArkUI属性 |
|----------|-----------|
| width | width() |
| height | height() |
| padding | padding() |
| margin | margin() |
| background-color | backgroundColor() |
| border-radius | borderRadius() |
| border | border() |
| font-size | fontSize() |
| font-weight | fontWeight() |
| color | fontColor() |
| text-align | textAlign() |
| line-height | lineHeight() |
| opacity | opacity() |
| display: flex | Flex/Row/Column |
| flex-direction | direction in Flex |
| justify-content | justifyContent() |
| align-items | alignItems() |
| position | position() |
| z-index | zIndex() |
| box-shadow | shadow() |

#### 事件映射

| 小程序 | 鸿蒙ArkUI |
|--------|-----------|
| bindtap | onClick() |
| bindinput | onChange() |
| bindfocus | onFocus() |
| bindblur | onBlur() |
| bindchange | onChange() |
| bindsubmit | onSubmit() |
| bindscroll | onScroll() |
| bindload | onComplete() |
| binderror | onError() |

#### 数据绑定

**小程序:**
```javascript
Page({
  data: {
    message: 'Hello',
    list: []
  },
  onLoad() {
    this.setData({ message: 'World' })
  }
})
```

**鸿蒙:**
```typescript
@Entry
@Component
struct Page {
  @State message: string = 'Hello'
  @State list: Array<any> = []

  aboutToAppear() {
    this.message = 'World'
  }
}
```

#### 列表渲染

**小程序:**
```xml
<block wx:for="{{list}}" wx:key="id">
  <view>{{item.name}}</view>
</block>
```

**鸿蒙:**
```typescript
ForEach(this.list, (item: any) => {
  Text(item.name)
}, (item: any) => item.id)
```

#### 条件渲染

**小程序:**
```xml
<view wx:if="{{show}}">显示</view>
<view wx:else>隐藏</view>
```

**鸿蒙:**
```typescript
if (this.show) {
  Text('显示')
} else {
  Text('隐藏')
}
```

#### API映射

| 小程序API | 鸿蒙API |
|-----------|---------|
| wx.request | http.createHttp().request() |
| wx.setStorage | preferences.put() |
| wx.getStorage | preferences.get() |
| wx.navigateTo | router.pushUrl() |
| wx.navigateBack | router.back() |
| wx.showToast | promptAction.showToast() |
| wx.showModal | AlertDialog.show() |
| wx.getLocation | geoLocationManager |
| wx.scanCode | (scanBarcode) |
| wx.chooseImage | picker.select() |
| wx.uploadFile | request.upload() |

---

## React Native → 鸿蒙

### 组件映射

| React Native | 鸿蒙ArkUI |
|--------------|-----------|
| View | Column/Row |
| Text | Text |
| Image | Image |
| TextInput | TextInput |
| ScrollView | Scroll |
| FlatList | List |
| TouchableOpacity | Button/onClick |
| StyleSheet | 链式调用样式 |

### 示例转换

**React Native:**
```jsx
import { View, Text, StyleSheet } from 'react-native'

const App = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold'
  }
})
```

**鸿蒙:**
```typescript
@Entry
@Component
struct App {
  build() {
    Column() {
      Text('Hello')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }
}
```

### 状态管理

| React Native | 鸿蒙 |
|--------------|------|
| useState | @State |
| useContext | @StorageLink/@StorageProp |
| Redux | AppStorage |
| useEffect | aboutToAppear/aboutToDisappear |

---

## Flutter → 鸿蒙

### Widget → Component映射

| Flutter | 鸿蒙ArkUI |
|---------|-----------|
| Container | Column/Row + 样式 |
| Text | Text |
| Image | Image |
| ElevatedButton | Button |
| TextField | TextInput |
| ListView | List |
| GridView | Grid |
| Stack | Stack |
| Row | Row |
| Column | Column |
| Expanded | layoutWeight() |
| SizedBox | width()/height() |
| Padding | padding() |
| Center | justifyContent(FlexAlign.Center) |

### 示例转换

**Flutter:**
```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text('Hello Flutter',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)
        )
      )
    );
  }
}
```

**鸿蒙:**
```typescript
@Entry
@Component
struct MyApp {
  build() {
    Column() {
      Text('Hello Flutter')
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
```

---

## Vue → 鸿蒙

### 模板映射

**Vue:**
```vue
<template>
  <div class="container">
    <h1>{{ title }}</h1>
    <button @click="handleClick">点击</button>
    <ul>
      <li v-for="item in list" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      title: 'Hello',
      list: []
    }
  },
  methods: {
    handleClick() {}
  }
}
</script>
```

**鸿蒙:**
```typescript
@Entry
@Component
struct Page {
  @State title: string = 'Hello'
  @State list: Array<any> = []

  build() {
    Column() {
      Text(this.title)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)

      Button('点击')
        .onClick(() => this.handleClick())

      List() {
        ForEach(this.list, (item: any) => {
          ListItem() {
            Text(item.name)
          }
        }, (item: any) => item.id)
      }
    }
    .width('100%')
    .height('100%')
  }

  handleClick() {}
}
```

### 生命周期映射

| Vue | 鸿蒙 |
|-----|------|
| created | aboutToAppear |
| mounted | aboutToAppear |
| updated | @State 变化自动触发 |
| destroyed | aboutToDisappear |
| computed | @State + get方法 |

---

## Android → 鸿蒙

### 组件映射

| Android | 鸿蒙ArkUI |
|---------|-----------|
| LinearLayout | Column/Row |
| RelativeLayout | Stack/Flex |
| FrameLayout | Stack |
| TextView | Text |
| EditText | TextInput |
| Button | Button |
| ImageView | Image |
| ListView | List |
| RecyclerView | List |
| WebView | Web |
| ScrollView | Scroll |

### Activity → UIAbility

**Android Activity:**
```java
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}
```

**鸿蒙 UIAbility:**
```typescript
import UIAbility from '@ohos.app.ability.UIAbility'

export default class MainAbility extends UIAbility {
  onCreate(want, launchParam) {
    // 初始化
  }

  onWindowStageCreate(windowStage) {
    windowStage.loadContent('pages/Index')
  }
}
```

---

## iOS/SwiftUI → 鸿蒙

### SwiftUI → ArkTS 映射

| SwiftUI | 鸿蒙ArkUI |
|---------|-----------|
| VStack | Column |
| HStack | Row |
| ZStack | Stack |
| Text | Text |
| Image | Image |
| Button | Button |
| TextField | TextInput |
| List | List |
| ScrollView | Scroll |

### 示例转换

**SwiftUI:**
```swift
struct ContentView: View {
  @State private var message = "Hello"

  var body: some View {
    VStack {
      Text(message)
        .font(.title)
      Button("Click") {
        message = "Clicked"
      }
    }
  }
}
```

**鸿蒙:**
```typescript
@Entry
@Component
struct ContentView {
  @State message: string = 'Hello'

  build() {
    Column() {
      Text(this.message)
        .fontSize(24)
      Button('Click')
        .onClick(() => {
          this.message = 'Clicked'
        })
    }
  }
}
```

---

## 翻译工作流

### Step 1: 分析源代码结构

1. 识别页面/组件层级
2. 提取数据模型
3. 梳理业务逻辑
4. 确认API调用

### Step 2: 创建鸿蒙项目结构

```
MyAtomicService/
├── AppScope/app.json5
├── entry/
│   ├── src/main/
│   │   ├── ets/
│   │   │   ├── pages/          # 页面
│   │   │   ├── components/      # 组件
│   │   │   ├── common/          # 工具类
│   │   │   └── models/          # 数据模型
│   │   └── resources/
│   └── module.json5
```

### Step 3: 翻译组件

1. 替换容器组件
2. 转换样式语法
3. 适配事件处理
4. 调整数据绑定

### Step 4: 迁移业务逻辑

1. 转换网络请求
2. 适配存储方式
3. 处理路由导航
4. 移植工具函数

### Step 5: 优化适配

1. 压缩资源文件
2. 确保包大小合规（≤2MB）
3. 添加服务卡片
4. 测试多设备适配

## 常见陷阱

### 1. 包大小超限
- 小程序通常较大，需要精简
- 使用WebP图片
- 移除未使用资源

### 2. API差异
- 部分API需要权限申请
- 异步处理方式不同
- 生命周期时机不同

### 3. 样式兼容
- 部分CSS属性不支持
- 布局方式需重新适配
- 字体单位换算

### 4. 第三方库
- 无直接对应库时需自行实现
- 参考OpenHarmony三方库中心
- 考虑原生能力替代方案

## 参考资源

- [ArkUI组件文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/arkui-overview-V5)
- [OpenHarmony三方库](https://ohpm.openharmony.cn/)
- [API参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/)
