---
name: harmonyos-widget-gallery
description: 鸿蒙服务卡片模板库。当用户需要：(1) 快速创建服务卡片 (2) 查找卡片UI模板 (3) 实现常见卡片样式（天气、时钟、待办、新闻等）时触发。提供即用型卡片模板和自定义指南。
---

# 鸿蒙服务卡片模板库

提供即用型服务卡片模板，快速实现各种常见卡片样式。

## 快速使用

选择模板 → 复制代码 → 自定义样式

### 卡片尺寸说明

| 尺寸 | 规格 | 适用场景 |
|------|------|----------|
| 1×2 | 小卡片 | 单行信息、开关 |
| 2×2 | 四宫格 | 天气、时钟、数据展示 |
| 2×4 | 横条 | 列表、音乐控制 |
| 4×4 | 大卡片 | 复杂内容、多数据 |

---

## 模板目录

### 1. 天气卡片 (2×2)

```typescript
@Entry
@Component
struct WeatherWidget {
  @State temp: string = '25°C'
  @State city: string = '北京'
  @State weather: string = '晴'
  @State icon: string = '☀️'

  build() {
    Column() {
      // 顶部：城市 + 天气图标
      Row() {
        Text(this.city)
          .fontSize(14)
          .fontColor('#666666')
        
        Blank()
        
        Text(this.icon)
          .fontSize(24)
      }
      .width('100%')
      .margin({ bottom: 8 })

      // 中间：温度
      Text(this.temp)
        .fontSize(48)
        .fontWeight(FontWeight.Bold)
        .fontColor('#333333')

      // 底部：天气描述
      Text(this.weather)
        .fontSize(16)
        .fontColor('#999999')
        .margin({ top: 4 })
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#F5F5F5')
    .borderRadius(16)
    .onClick(() => {
      postCardAction(this, {
        action: 'router',
        abilityName: 'EntryAbility',
        params: { page: 'pages/WeatherDetail' }
      })
    })
  }
}
```

---

### 2. 时钟卡片 (2×2)

```typescript
@Entry
@Component
struct ClockWidget {
  @State time: string = '14:30'
  @State date: string = '3月19日 周四'

  build() {
    Column() {
      Text(this.time)
        .fontSize(56)
        .fontWeight(FontWeight.Bold)
        .fontColor('#1A1A1A')

      Text(this.date)
        .fontSize(14)
        .fontColor('#888888')
        .margin({ top: 8 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#FFFFFF')
    .borderRadius(20)
  }
}
```

---

### 3. 待办卡片 (2×4)

```typescript
@Entry
@Component
struct TodoWidget {
  @State todos: Array<{text: string, done: boolean}> = [
    { text: '完成项目报告', done: false },
    { text: '回复邮件', done: true },
    { text: '团队会议 14:00', done: false }
  ]

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('待办事项')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
        
        Blank()
        
        Text(`${this.todos.filter(t => t.done).length}/${this.todos.length}`)
          .fontSize(14)
          .fontColor('#999999')
      }
      .width('100%')
      .margin({ bottom: 12 })

      // 待办列表
      ForEach(this.todos, (item, index) => {
        Row() {
          Checkbox()
            .select(item.done)
            .onChange((checked) => {
              this.todos[index].done = checked
            })

          Text(item.text)
            .fontSize(14)
            .fontColor(item.done ? '#CCCCCC' : '#333333')
            .decoration({ type: item.done ? TextDecorationType.LineThrough : TextDecorationType.None })
        }
        .width('100%')
        .margin({ bottom: 8 })
      })
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
  }
}
```

---

### 4. 音乐控制卡片 (2×4)

```typescript
@Entry
@Component
struct MusicWidget {
  @State title: string = '起风了'
  @State artist: string = '买辣椒也用券'
  @State isPlaying: boolean = true
  @State progress: number = 0.3

  build() {
    Column() {
      // 歌曲信息
      Row() {
        Image($r('app.media.album'))
          .width(50)
          .height(50)
          .borderRadius(8)

        Column() {
          Text(this.title)
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .maxLines(1)
          
          Text(this.artist)
            .fontSize(12)
            .fontColor('#999999')
            .margin({ top: 2 })
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Start)
        .margin({ left: 12 })
      }
      .width('100%')
      .margin({ bottom: 12 })

      // 进度条
      Progress({ value: this.progress * 100, total: 100 })
        .width('100%')
        .height(4)
        .color('#007DFF')
        .margin({ bottom: 12 })

      // 控制按钮
      Row() {
        Button() { Text('⏮').fontSize(20) }
          .width(40)
          .height(40)
          .backgroundColor(Color.Transparent)

        Button() { Text(this.isPlaying ? '⏸' : '▶️').fontSize(24) }
          .width(50)
          .height(50)
          .backgroundColor('#007DFF')
          .borderRadius(25)
          .onClick(() => {
            this.isPlaying = !this.isPlaying
            postCardAction(this, {
              action: 'call',
              abilityName: 'EntryAbility',
              params: { method: this.isPlaying ? 'play' : 'pause' }
            })
          })

        Button() { Text('⏭').fontSize(20) }
          .width(40)
          .height(40)
          .backgroundColor(Color.Transparent)
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceEvenly)
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#1A1A1A')
    .borderRadius(16)
  }
}
```

---

### 5. 新闻卡片 (2×4)

```typescript
@Entry
@Component
struct NewsWidget {
  @State headlines: Array<{title: string, source: string}> = [
    { title: '华为发布新款Mate手机', source: '科技日报' },
    { title: '鸿蒙系统市场份额突破20%', source: '新浪科技' },
    { title: 'AI大模型迎来新突破', source: '36氪' }
  ]

  build() {
    Column() {
      // 标题
      Row() {
        Text('今日头条')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
        
        Blank()
        
        Text('更多 >')
          .fontSize(12)
          .fontColor('#007DFF')
      }
      .width('100%')
      .margin({ bottom: 12 })

      // 新闻列表
      ForEach(this.headlines, (item, index) => {
        Column() {
          Text(item.title)
            .fontSize(14)
            .maxLines(2)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
          
          Text(item.source)
            .fontSize(11)
            .fontColor('#999999')
            .margin({ top: 4 })
        }
        .width('100%')
        .alignItems(HorizontalAlign.Start)
        .padding({ top: 8, bottom: 8 })
        .border({ width: { bottom: index < 2 ? 0.5 : 0 }, color: '#EEEEEE' })
        .onClick(() => {
          postCardAction(this, {
            action: 'router',
            abilityName: 'EntryAbility',
            params: { page: 'pages/NewsDetail', index: index }
          })
        })
      })
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
  }
}
```

---

### 6. 计步卡片 (2×2)

```typescript
@Entry
@Component
struct StepsWidget {
  @State steps: number = 6842
  @State goal: number = 10000
  @State calories: number = 256

  build() {
    Column() {
      // 步数
      Stack() {
        // 进度环
        Progress({ value: this.steps, total: this.goal, type: ProgressType.Ring })
          .width(100)
          .height(100)
          .color('#4CAF50')

        Column() {
          Text(this.steps.toString())
            .fontSize(28)
            .fontWeight(FontWeight.Bold)
          
          Text('步')
            .fontSize(12)
            .fontColor('#999999')
        }
      }
      .margin({ top: 8 })

      // 卡路里
      Row() {
        Text('🔥')
        Text(`${this.calories} 千卡`)
          .fontSize(14)
          .margin({ left: 4 })
      }
      .margin({ top: 12 })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
  }
}
```

---

### 7. 快捷开关卡片 (2×2)

```typescript
@Entry
@Component
struct QuickSettingsWidget {
  @State wifi: boolean = true
  @State bluetooth: boolean = false
  @State flashlight: boolean = false
  @State mute: boolean = false

  build() {
    Grid() {
      GridItem() {
        this.SettingItem('📶', 'WiFi', this.wifi, () => { this.wifi = !this.wifi })
      }
      GridItem() {
        this.SettingItem('🔵', '蓝牙', this.bluetooth, () => { this.bluetooth = !this.bluetooth })
      }
      GridItem() {
        this.SettingItem('🔦', '手电', this.flashlight, () => { this.flashlight = !this.flashlight })
      }
      GridItem() {
        this.SettingItem('🔇', '静音', this.mute, () => { this.mute = !this.mute })
      }
    }
    .columnsTemplate('1fr 1fr')
    .rowsTemplate('1fr 1fr')
    .width('100%')
    .height('100%')
    .padding(8)
    .backgroundColor('#F0F0F0')
    .borderRadius(16)
  }

  @Builder
  SettingItem(icon: string, label: string, active: boolean, onClick: () => void) {
    Column() {
      Text(icon)
        .fontSize(28)
      
      Text(label)
        .fontSize(12)
        .margin({ top: 4 })
        .fontColor(active ? '#007DFF' : '#666666')
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .backgroundColor(active ? '#E3F2FD' : '#FFFFFF')
    .borderRadius(12)
    .onClick(onClick)
  }
}
```

---

### 8. 日程卡片 (2×4)

```typescript
@Entry
@Component
struct ScheduleWidget {
  @State today: string = '3月19日'
  @State events: Array<{time: string, title: string, location: string}> = [
    { time: '09:00', title: '晨会', location: '会议室A' },
    { time: '14:00', title: '项目评审', location: '301室' },
    { time: '16:30', title: '客户电话', location: '' }
  ]

  build() {
    Column() {
      // 日期标题
      Row() {
        Text(this.today)
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
        
        Blank()
        
        Text('+ 添加')
          .fontSize(12)
          .fontColor('#007DFF')
      }
      .width('100%')
      .margin({ bottom: 12 })

      // 日程列表
      ForEach(this.events, (item) => {
        Row() {
          // 时间线
          Column() {
            Text(item.time)
              .fontSize(12)
              .fontColor('#007DFF')
            
            Line()
              .width(1)
              .height(30)
              .backgroundColor('#DDDDDD')
          }
          .width(50)

          // 内容
          Column() {
            Text(item.title)
              .fontSize(14)
              .fontWeight(FontWeight.Medium)
            
            if (item.location) {
              Text(`📍 ${item.location}`)
                .fontSize(11)
                .fontColor('#999999')
                .margin({ top: 2 })
            }
          }
          .layoutWeight(1)
          .alignItems(HorizontalAlign.Start)
        }
        .width('100%')
        .margin({ bottom: 8 })
      })
    }
    .width('100%')
    .height('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
  }
}
```

---

## 自定义指南

### 修改尺寸

编辑 `form_config.json`：
```json
{
  "forms": [{
    "defaultDimension": "2*2",
    "supportDimensions": ["2*2", "2*4", "4*4"]
  }]
}
```

### 添加刷新

```typescript
// 卡片内
Button('刷新')
  .onClick(() => {
    postCardAction(this, {
      action: 'call',
      abilityName: 'EntryAbility',
      params: { method: 'refreshData' }
    })
  })

// EntryAbility 中处理
onNewWant(want) {
  if (want.parameters?.method === 'refreshData') {
    // 更新数据
    formProvider.updateForm(formId, formData)
  }
}
```

### 样式定制

```typescript
// 渐变背景
.linearGradient({
  angle: 135,
  colors: [['#667eea', 0], ['#764ba2', 1]]
})

// 阴影
.shadow({
  radius: 10,
  color: '#1A000000',
  offsetX: 0,
  offsetY: 4
})

// 毛玻璃效果
.backdropBlur(20)
```

---

## 参考资源

- [服务卡片开发指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/service-widget-overview-V5)
- [ArkUI组件参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/arkui-overview-V5)
