# 鸿蒙编译错误模式库

本文档包含所有常见编译错误的模式、原因和修复方案。

## 错误解析格式

每个错误记录包含：
- **错误码**：官方错误码（如有）
- **错误模式**：正则匹配模式
- **原因分析**：为什么会出现这个错误
- **修复方案**：具体修复步骤
- **示例**：错误代码与修复后代码对比

---

## 一、ArkTS 编译错误 (ARKTS-XXXX)

### ARKTS-1001: Cannot find name

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Cannot find name '(\w+)'.
```

**原因：**
- 变量未声明
- 函数未定义
- 缺少导入
- 作用域问题

**修复方案：**

1. 检查是否需要添加导入：
```typescript
// 添加导入
import router from '@ohos.router'
import http from '@ohos.net.http'
```

2. 检查是否需要声明状态变量：
```typescript
// 在组件中添加 @State 声明
@State message: string = ''
```

3. 检查 this 引用：
```typescript
// 错误：直接使用
Text(message)

// 正确：使用 this
Text(this.message)
```

---

### ARKTS-1002: Type mismatch

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Type '(\w+)' is not assignable to type '(\w+)'.
```

**常见类型不匹配：**

| 源类型 | 目标类型 | 修复方法 |
|--------|----------|----------|
| string | number | `parseInt()` / `parseFloat()` |
| number | string | `toString()` / `String()` |
| null | Object | 添加 null 检查或使用 `!` |
| undefined | T | 添加默认值或 null 检查 |
| any | T | 添加类型断言 `as T` |

**示例：**

```typescript
// 错误
let count: number = '10'
let name: string = 123

// 修复
let count: number = parseInt('10')
let name: string = 123.toString()
```

---

### ARKTS-1003: Property does not exist

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Property '(\w+)' does not exist on type '(\w+)'.
```

**常见原因：**
1. 接口定义不完整
2. 使用了错误的对象类型
3. API 版本变更

**示例：**

```typescript
// 错误：接口缺少属性
interface User {
  name: string
}
let user: User = { name: 'Tom', age: 18 }  // age 不在接口中

// 修复：完善接口
interface User {
  name: string
  age: number
}
```

---

### ARKTS-1004: Cannot find module

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Cannot find module '([^']+)' or its corresponding type declarations.
```

**修复方案：**

1. 检查模块路径：
```typescript
// 相对路径
import { User } from '../models/User'

// @ohos 模块
import router from '@ohos.router'
```

2. 安装缺失依赖：
```bash
ohpm install @ohos/xxx
```

3. 检查 oh-package.json5：
```json
{
  "dependencies": {
    "@ohos/xxx": "^1.0.0"
  }
}
```

---

### ARKTS-1005: Function signature mismatch

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Argument of type '([^']+)' is not assignable to parameter of type '([^']+)'.
```

**示例：**

```typescript
// 错误：参数类型不匹配
function greet(name: string): void {}
greet(123)  // number 不能赋给 string

// 修复
greet('123')
greet(123.toString())
```

---

### ARKTS-1006: Duplicate identifier

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
Duplicate identifier '(\w+)'.
```

**原因：**
- 重复声明变量
- 重复定义函数
- 重复导入

**修复：**
```typescript
// 错误
let name = 'Tom'
let name = 'Jerry'  // 重复

// 修复
let name = 'Tom'
// 删除重复声明，或使用不同变量名
let name2 = 'Jerry'
```

---

### ARKTS-1007: Missing return statement

**错误模式：**
```
ArkTS:ERROR File: (.+):(\d+):(\d+)
A function whose declared type is neither 'void' nor 'any' must return a value.
```

**修复：**
```typescript
// 错误
function add(a: number, b: number): number {
  console.log(a + b)
  // 缺少 return
}

// 修复
function add(a: number, b: number): number {
  return a + b
}
```

---

## 二、组件相关错误

### Component-001: @State type error

**错误模式：**
```
Property '(\w+)' has no initializer and is not definitely assigned.
```

**修复：**
```typescript
// 错误
@State message: string  // 未初始化

// 修复
@State message: string = ''  // 添加初始值
@State count: number = 0
@State list: Array<any> = []
```

---

### Component-002: @Builder usage error

**错误模式：**
```
@Builder can only be used in struct or class.
```

**正确用法：**
```typescript
@Entry
@Component
struct Page {
  // 正确：在 struct 内定义
  @Builder
  myBuilder() {
    Text('Builder content')
  }

  build() {
    Column() {
      this.myBuilder()  // 正确调用
    }
  }
}
```

---

### Component-003: @Link binding error

**错误模式：**
```
@Link property must be initialized with @State property from parent.
```

**正确用法：**
```typescript
// 父组件
@Entry
@Component
struct Parent {
  @State count: number = 0

  build() {
    Column() {
      Child({ count: $count })  // 使用 $ 传递引用
    }
  }
}

// 子组件
@Component
struct Child {
  @Link count: number  // 接收引用

  build() {
    Text(`${this.count}`)
  }
}
```

---

## 三、API 兼容性错误

### API-001: Deprecated API

**错误模式：**
```
Attribute '(\w+)' is deprecated. Use '(\w+)' instead.
```

**常见废弃API替换：**

| 废弃API | 新API | 说明 |
|---------|-------|------|
| `router.push()` | `router.pushUrl()` | 路由跳转 |
| `router.replace()` | `router.replaceUrl()` | 替换页面 |
| `featureAbility` | `@ohos.app.ability` | 能力模块 |
| `@ohos.data.storage` | `@ohos.data.preferences` | 数据存储 |

**示例：**
```typescript
// 废弃
router.push({ url: 'pages/Detail' })

// 推荐
router.pushUrl({ url: 'pages/Detail' })
```

---

### API-002: Permission denied

**错误模式：**
```
Permission denied: (\w+)
```

**修复步骤：**

1. 在 module.json5 中添加权限：
```json
{
  "module": {
    "requestPermissions": [
      {
        "name": "ohos.permission.INTERNET"
      },
      {
        "name": "ohos.permission.LOCATION"
      }
    ]
  }
}
```

2. 敏感权限需要用户授权：
```typescript
import abilityAccessCtrl from '@ohos.abilityAccessCtrl'

async function requestPermission() {
  let atManager = abilityAccessCtrl.createAtManager()
  let result = await atManager.requestPermissionsFromUser(
    context,
    ['ohos.permission.CAMERA']
  )
}
```

---

## 四、资源相关错误

### Resource-001: Resource not found

**错误模式：**
```
ERROR: resource \$r\('app\.(\w+)\.(\w+)'\) not found
```

**修复：**

1. 检查资源文件是否存在：
```bash
ls entry/src/main/resources/base/media/
ls entry/src/main/resources/base/element/
```

2. 创建缺失资源：

**字符串资源** (`element/string.json`)：
```json
{
  "string": [
    { "name": "app_name", "value": "My App" }
  ]
}
```

**图片资源**：
```bash
# 复制图片到资源目录
cp logo.png entry/src/main/resources/base/media/
```

3. 使用正确的资源引用：
```typescript
// 字符串
Text($r('app.string.app_name'))

// 图片
Image($r('app.media.logo'))

// 颜色
.backgroundColor($r('app.color.primary'))
```

---

### Resource-002: Invalid resource format

**错误模式：**
```
ERROR: Invalid resource format for (.+)
```

**常见问题：**
- 图片格式不支持（使用 png/jpg/webp/svg）
- 字符串 JSON 格式错误
- 颜色值格式错误

**修复：**
```json
// 正确的颜色格式
{
  "color": [
    { "name": "primary", "value": "#007DFF" }
  ]
}

// 正确的字符串格式
{
  "string": [
    { "name": "greeting", "value": "Hello" }
  ]
}
```

---

## 五、构建配置错误

### Build-001: Module not found

**错误模式：**
```
ERROR: Module '(\w+)' not found in project
```

**修复：**

1. 检查 module.json5 中的模块名：
```json
{
  "module": {
    "name": "entry"  // 模块名
  }
}
```

2. 检查编译命令：
```bash
# 模块名与配置一致
./hvigorw assembleHap --mode module -p module=entry@default
```

---

### Build-002: Signing config error

**错误模式：**
```
ERROR: Signing config not found or invalid
```

**修复步骤：**

1. 检查签名文件：
```bash
ls -la *.p12 *.cer *.p7b
```

2. 配置 build-profile.json5：
```json
{
  "app": {
    "signingConfigs": [
      {
        "name": "default",
        "type": "HarmonyOS",
        "material": {
          "certpath": "certs/release.cer",
          "storePassword": "password",
          "keyAlias": "alias",
          "keyPassword": "password",
          "profile": "certs/release.p7b",
          "signAlg": "SHA256withECDSA",
          "storeFile": "certs/release.p12"
        }
      }
    ]
  }
}
```

3. 或使用自动签名（开发阶段）：
   - DevEco Studio → File → Project Structure → Signing Configs
   - 勾选 "Automatically generate signature"

---

### Build-003: HAP size exceeds limit

**错误模式：**
```
ERROR: HAP size (\d+)MB exceeds limit (\d+)MB
```

**元服务包大小限制：**
- 单个 HAP：≤ 2MB
- 同设备所有 HAP 总和：≤ 10MB

**优化方案：**

1. **压缩图片：**
```bash
# 转 WebP
for f in *.png; do
  cwebp -q 80 "$f" -o "${f%.png}.webp"
done
```

2. **移除未使用资源：**
```bash
# 查找未使用的资源
grep -r "app.media" entry/src/main/ets/
# 对比资源目录
ls entry/src/main/resources/base/media/
```

3. **使用 HSP 共享包：**
```
# 将公共代码提取到 HSP 模块
MyApp/
├── entry/        # 主入口 HAP (≤2MB)
├── shared/       # HSP 共享包
└── features/     # 功能模块 HAP
```

4. **使用在线资源：**
```typescript
// 使用网络图片而非本地
Image('https://cdn.example.com/image.png')
```

---

## 六、依赖相关错误

### Deps-001: Dependency resolution failed

**错误模式：**
```
ERROR: Could not resolve dependency: ([^ ]+)
```

**修复：**

1. 检查 oh-package.json5：
```json
{
  "dependencies": {
    "@ohos/zxing": "^2.0.0"
  }
}
```

2. 安装依赖：
```bash
ohpm install
```

3. 检查仓库配置：
```json
{
  "dependencies": {},
  "overrides": {},
  "devDependencies": {},
  "overridesDependency": {}
}
```

---

### Deps-002: Version conflict

**错误模式：**
```
ERROR: Version conflict: ([^ ]+) requires ([^ ]+) but ([^ ]+) was found
```

**修复：**

1. 统一版本：
```json
// oh-package.json5
{
  "overrides": {
    "problematic-package": "1.2.3"
  }
}
```

2. 或使用 resolutions：
```json
{
  "resolutions": {
    "package-a/version": "1.2.3"
  }
}
```

---

## 七、运行时错误

### Runtime-001: Undefined is not a function

**原因：**
- 调用了不存在的方法
- 对象为 null/undefined

**修复：**
```typescript
// 添加空检查
if (user && user.getName) {
  user.getName()
}

// 使用可选链
user?.getName?.()
```

---

### Runtime-002: Out of memory

**原因：**
- 图片过大
- 列表数据过多
- 内存泄漏

**修复：**
```typescript
// 图片优化
Image(url)
  .objectFit(ImageFit.Cover)  // 裁剪适配
  .width(100)
  .height(100)

// 列表懒加载
List() {
  LazyForEach(this.dataSource, (item) => {
    ListItem() { ... }
  })
}

// 及时释放资源
aboutToDisappear() {
  this.httpRequest?.destroy()
}
```

---

## 八、错误自动修复映射表

| 错误类别 | 自动修复策略 | 手动干预 |
|----------|-------------|----------|
| 未定义变量 | 添加导入/声明 | 复杂类型推断 |
| 类型不匹配 | 类型转换 | 业务逻辑调整 |
| 缺少属性 | 添加属性声明 | 接口设计变更 |
| 废弃API | 替换新API | 功能差异处理 |
| 缺少权限 | 添加权限配置 | 敏感权限引导 |
| 资源缺失 | 创建占位资源 | 实际资源准备 |
| 包体超限 | 资源压缩 | 架构重构 |

---

## 参考资源

- [ArkTS错误码完整列表](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/arkts-errors-V5)
- [编译错误排查](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/ide-build-V5)
- [API兼容性指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/api-compatibility-V5)
