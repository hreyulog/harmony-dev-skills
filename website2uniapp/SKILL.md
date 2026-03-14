---
name: website-to-harmonyos
description: 将网站转换为鸿蒙元服务（原生重写模式）。当用户想要：(1) 把现有网站转成鸿蒙App (2) 将Web页面迁移到HarmonyOS (3) 网站内容本地化为元服务 (4) 创建网站的鸿蒙客户端时触发。提供页面分析、HTML/CSS转ArkUI、功能迁移完整流程。
---

# 网站转鸿蒙元服务

将现有网站原生重写为鸿蒙元服务，获得最佳用户体验。

## 转换工作流

```
1. 分析网站结构
   ├── 爬取页面列表
   ├── 提取UI组件
   ├── 分析API接口
   └── 确定数据模型

2. 创建鸿蒙项目
   ├── 初始化项目
   ├── 配置app.json5
   └── 申请权限

3. 页面转换
   ├── HTML → ArkUI组件
   ├── CSS → ArkTS样式
   └── JS逻辑 → TypeScript

4. 功能实现
   ├── API对接
   ├── 数据存储
   └── 交互逻辑

5. 测试上架
   ├── 功能测试
   ├── 包大小检查(≤2MB)
   └── 签名上架
```

---

## 一、分析网站

### 提取页面结构

**使用浏览器开发者工具(F12)：**
1. 查看DOM结构 → 确定组件层级
2. Network面板 → 获取API接口
3. Application → 查看本地存储数据

**需要记录：**
- 页面列表和路由关系
- 每个页面的主要区块
- 表单和交互元素
- 图片资源URL

### 提取数据模型

从API响应中提取数据结构：

```typescript
// 例如商品列表API返回
{
  "products": [
    {
      "id": "001",
      "name": "商品名称",
      "price": 99.00,
      "image": "https://...",
      "description": "描述"
    }
  ],
  "total": 100,
  "page": 1
}

// 转为TypeScript接口
interface Product {
  id: string
  name: string
  price: number
  image: string
  description: string
}

interface ProductListResponse {
  products: Product[]
  total: number
  page: number
}
```

---

## 二、HTML → ArkUI 转换

### 页面结构映射

| HTML元素 | ArkUI组件 | 用途 |
|----------|-----------|------|
| `<div>` | Column / Row | 容器 |
| `<header>` | Row | 顶部栏 |
| `<nav>` | Row / Tabs | 导航 |
| `<main>` | Column | 主内容区 |
| `<section>` | Column | 内容分区 |
| `<article>` | Column | 文章块 |
| `<footer>` | Row | 底部栏 |
| `<aside>` | Column | 侧边栏 |
| `<ul>/<ol>` | List | 列表 |
| `<li>` | ListItem | 列表项 |
| `<form>` | Column | 表单容器 |
| `<table>` | Grid / 自定义 | 表格 |
| `<dialog>` | CustomDialog | 对话框 |

### 组件映射表

| HTML元素 | ArkUI组件 | 示例 |
|----------|-----------|------|
| `<h1>`-`<h6>` | Text | 标题文本 |
| `<p>` | Text | 段落 |
| `<span>` | Text / Span | 行内文本 |
| `<a>` | Text + onClick | 链接 |
| `<img>` | Image | 图片 |
| `<video>` | Video | 视频 |
| `<audio>` | AVPlayer | 音频 |
| `<button>` | Button | 按钮 |
| `<input type="text">` | TextInput | 文本输入 |
| `<input type="password">` | TextInput (Password) | 密码输入 |
| `<input type="number">` | TextInput (Number) | 数字输入 |
| `<textarea>` | TextArea | 多行文本 |
| `<select>` | Select | 下拉选择 |
| `<input type="checkbox">` | Checkbox | 复选框 |
| `<input type="radio">` | Radio | 单选框 |
| `<input type="range">` | Slider | 滑块 |
| `<progress>` | Progress | 进度条 |
| `<canvas>` | Canvas | 画布 |

---

## 三、CSS → ArkTS 样式转换

### 布局转换

#### Flexbox → Column/Row

**CSS:**
```css
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 20px;
}
```

**ArkTS:**
```typescript
Column() {
  // children
}
.width('100%')
.height('100%')
.justifyContent(FlexAlign.Center)
.alignItems(HorizontalAlign.Center)
.space(10)
.padding(20)
```

#### Flex Row

**CSS:**
```css
.row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
```

**ArkTS:**
```typescript
Row() {
  // children
}
.width('100%')
.justifyContent(FlexAlign.SpaceBetween)
.alignItems(VerticalAlign.Center)
```

#### Grid → Grid组件

**CSS:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}
```

**ArkTS:**
```typescript
Grid() {
  ForEach(items, (item) => {
    GridItem() {
      // content
    }
  })
}
.columnsTemplate('1fr 1fr 1fr')
.rowsGap(10)
.columnsGap(10)
```

#### 绝对定位

**CSS:**
```css
.box {
  position: absolute;
  top: 10px;
  left: 20px;
  z-index: 10;
}
```

**ArkTS:**
```typescript
Stack() {
  Column() {
    // content
  }
  .position({ x: 20, y: 10 })
  .zIndex(10)
}
```

### 样式属性映射表

| CSS属性 | ArkTS方法 | 示例 |
|---------|-----------|------|
| width | width() | `.width(100)` 或 `.width('100%')` |
| height | height() | `.height(50)` |
| padding | padding() | `.padding(10)` 或 `.padding({ top: 5, bottom: 10 })` |
| margin | margin() | `.margin(10)` 或 `.margin({ left: 20 })` |
| background-color | backgroundColor() | `.backgroundColor('#FFFFFF')` |
| border-radius | borderRadius() | `.borderRadius(8)` |
| border | border() | `.border({ width: 1, color: '#CCCCCC' })` |
| font-size | fontSize() | `.fontSize(16)` |
| font-weight | fontWeight() | `.fontWeight(FontWeight.Bold)` |
| font-family | fontFamily() | `.fontFamily('HarmonyOS Sans')` |
| color | fontColor() | `.fontColor('#333333')` |
| text-align | textAlign() | `.textAlign(TextAlign.Center)` |
| line-height | lineHeight() | `.lineHeight(24)` |
| letter-spacing | letterSpacing() | `.letterSpacing(1)` |
| opacity | opacity() | `.opacity(0.8)` |
| box-shadow | shadow() | `.shadow({ radius: 4, color: '#1A000000' })` |
| visibility | visibility() | `.visibility(Visibility.None)` |
| display: none | visibility() | `.visibility(Visibility.None)` |
| overflow: hidden | clip() | `.clip(true)` |
| transform | rotate/scale/translate | `.rotate({ angle: 45 })` |
| animation | animateTo | `animateTo({ duration: 1000 }, () => {})` |

### 颜色转换

| CSS颜色格式 | ArkTS格式 |
|-------------|-----------|
| `#FFF` | `'#FFFFFF'` |
| `#FFFFFF` | `'#FFFFFF'` |
| `rgb(255,0,0)` | `'#FF0000'` |
| `rgba(0,0,0,0.5)` | `'#80000000'` (AA RR GG BB) |
| `red` | `Color.Red` |

---

## 四、JavaScript → TypeScript 转换

### 变量声明

```javascript
// JavaScript
var name = 'test'
let age = 18
const PI = 3.14
```

```typescript
// TypeScript
let name: string = 'test'
let age: number = 18
const PI: number = 3.14
```

### 函数定义

```javascript
// JavaScript
function getData(id) {
  return fetch('/api/' + id)
}

const handleSubmit = (e) => {
  e.preventDefault()
}
```

```typescript
// TypeScript
async function getData(id: string): Promise<Response> {
  return await fetch('/api/' + id)
}

const handleSubmit = (e: Event) => {
  e.preventDefault()
}
```

### 事件处理

```javascript
// JavaScript
document.getElementById('btn').addEventListener('click', function() {
  console.log('clicked')
})
```

```typescript
// ArkTS
Button('点击')
  .onClick(() => {
    console.info('clicked')
  })
```

### 数据绑定

```javascript
// JavaScript/Vue
data() {
  return {
    message: 'Hello'
  }
}

// React
const [message, setMessage] = useState('Hello')
```

```typescript
// ArkTS
@State message: string = 'Hello'

// 更新数据
this.message = 'World'
```

### 列表渲染

```javascript
// JavaScript
items.map(item => `<li>${item.name}</li>`)
```

```typescript
// ArkTS
List() {
  ForEach(this.items, (item: Item) => {
    ListItem() {
      Text(item.name)
    }
  }, (item: Item) => item.id)
}
```

### 条件渲染

```javascript
// JavaScript
{show ? <div>显示</div> : <div>隐藏</div>}
```

```typescript
// ArkTS
if (this.show) {
  Text('显示')
} else {
  Text('隐藏')
}
```

---

## 五、API调用转换

### Fetch → HTTP模块

**JavaScript Fetch:**
```javascript
fetch('https://api.example.com/products', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  }
})
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err))
```

**ArkTS HTTP:**
```typescript
import http from '@ohos.net.http'

async function fetchProducts(): Promise<Product[]> {
  let httpRequest = http.createHttp()
  try {
    let response = await httpRequest.request(
      'https://api.example.com/products',
      {
        method: http.RequestMethod.GET,
        header: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + this.token
        }
      }
    )
    let result = JSON.parse(response.result as string) as ProductListResponse
    return result.products
  } catch (err) {
    console.error(err.message)
    return []
  } finally {
    httpRequest.destroy()
  }
}
```

### POST请求

**JavaScript:**
```javascript
fetch('/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user', password: 'pass' })
})
```

**ArkTS:**
```typescript
async function login(username: string, password: string) {
  let httpRequest = http.createHttp()
  try {
    let response = await httpRequest.request(
      'https://api.example.com/login',
      {
        method: http.RequestMethod.POST,
        header: { 'Content-Type': 'application/json' },
        extraData: { username, password }
      }
    )
    return JSON.parse(response.result as string)
  } finally {
    httpRequest.destroy()
  }
}
```

---

## 六、完整转换示例

### 示例：商品列表页

**原HTML页面:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; font-family: sans-serif; background: #f5f5f5; }
    .header { 
      display: flex; justify-content: space-between; 
      padding: 16px; background: white; 
    }
    .search { padding: 8px 16px; border-radius: 20px; border: 1px solid #ddd; }
    .product-list { padding: 16px; }
    .product-card { 
      display: flex; background: white; 
      margin-bottom: 12px; padding: 12px; border-radius: 12px;
    }
    .product-card img { width: 100px; height: 100px; border-radius: 8px; }
    .product-info { margin-left: 12px; flex: 1; }
    .product-name { font-size: 16px; font-weight: bold; }
    .product-price { color: #f44; font-size: 18px; margin-top: 8px; }
    .btn-cart { 
      background: #007dff; color: white; 
      padding: 8px 16px; border-radius: 4px; border: none;
    }
  </style>
</head>
<body>
  <header class="header">
    <h1>商品列表</h1>
    <input type="search" class="search" placeholder="搜索商品">
  </header>
  <div class="product-list" id="list"></div>

  <script>
    let products = []
    
    async function loadProducts() {
      const res = await fetch('/api/products')
      products = await res.json()
      renderProducts(products)
    }
    
    function renderProducts(items) {
      const html = items.map(p => `
        <div class="product-card">
          <img src="${p.image}">
          <div class="product-info">
            <div class="product-name">${p.name}</div>
            <div class="product-price">¥${p.price}</div>
            <button class="btn-cart" onclick="addToCart(${p.id})">加入购物车</button>
          </div>
        </div>
      `).join('')
      document.getElementById('list').innerHTML = html
    }
    
    function addToCart(id) {
      fetch('/api/cart', { method: 'POST', body: JSON.stringify({ productId: id }) })
      alert('已加入购物车')
    }
    
    loadProducts()
  </script>
</body>
</html>
```

**转换后ArkTS:**
```typescript
import http from '@ohos.net.http'
import promptAction from '@ohos.promptAction'

interface Product {
  id: number
  name: string
  price: number
  image: string
}

@Entry
@Component
struct ProductListPage {
  @State products: Product[] = []
  @State searchText: string = ''
  @State isLoading: boolean = true

  aboutToAppear() {
    this.loadProducts()
  }

  async loadProducts() {
    this.isLoading = true
    let httpRequest = http.createHttp()
    try {
      let response = await httpRequest.request(
        'https://api.example.com/products',
        { method: http.RequestMethod.GET }
      )
      this.products = JSON.parse(response.result as string)
    } catch (err) {
      console.error(err.message)
    } finally {
      httpRequest.destroy()
      this.isLoading = false
    }
  }

  async addToCart(productId: number) {
    let httpRequest = http.createHttp()
    try {
      await httpRequest.request(
        'https://api.example.com/cart',
        {
          method: http.RequestMethod.POST,
          header: { 'Content-Type': 'application/json' },
          extraData: { productId }
        }
      )
      promptAction.showToast({ message: '已加入购物车' })
    } finally {
      httpRequest.destroy()
    }
  }

  build() {
    Column() {
      // Header
      Row() {
        Text('商品列表')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .layoutWeight(1)

        TextInput({ placeholder: '搜索商品', text: this.searchText })
          .width(200)
          .height(40)
          .borderRadius(20)
          .backgroundColor('#F5F5F5')
          .onChange((value) => {
            this.searchText = value
          })
      }
      .width('100%')
      .padding(16)
      .backgroundColor('#FFFFFF')

      // Product List
      if (this.isLoading) {
        LoadingProgress()
          .width(50)
          .height(50)
          .margin({ top: 100 })
      } else {
        List() {
          ForEach(this.products, (item: Product) => {
            ListItem() {
              this.ProductCard(item)
            }
          }, (item: Product) => item.id.toString())
        }
        .width('100%')
        .layoutWeight(1)
        .padding(16)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }

  @Builder
  ProductCard(item: Product) {
    Row() {
      Image(item.image)
        .width(100)
        .height(100)
        .borderRadius(8)
        .objectFit(ImageFit.Cover)

      Column() {
        Text(item.name)
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        Text(`¥${item.price}`)
          .fontSize(18)
          .fontColor('#FF4444')
          .margin({ top: 8 })

        Button('加入购物车')
          .height(32)
          .fontSize(14)
          .backgroundColor('#007DFF')
          .margin({ top: 8 })
          .onClick(() => this.addToCart(item.id))
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
      .margin({ left: 12 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#FFFFFF')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }
}
```

---

## 七、注意事项

### 包大小限制
- 单个HAP ≤ 2MB
- 使用在线图片URL代替本地图片
- 压缩必要的图片资源

### 网络安全
- 配置 `ohos.permission.INTERNET` 权限
- HTTPS接口更安全

### 离线支持
- 使用 Preferences 存储关键数据
- 缓存API响应数据

### 性能优化
- 使用 LazyForEach 懒加载长列表
- 图片使用 ObjectFit 控制显示
- 避免过深的组件嵌套

---

## 参考资源

- [ArkUI组件文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/arkui-overview-V5)
- [HTTP数据请求](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/http-request-overview-V5)
- [应用开发指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/application-dev-guide-V5)
