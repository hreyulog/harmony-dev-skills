---
name: harmonyos-debugger
description: 鸿蒙项目编译错误诊断与自动修复。当用户遇到：(1) hvigor编译错误 (2) ArkTS语法错误 (3) 模块依赖问题 (4) 签名/打包失败 (5) 需要自动编译并修复错误时触发。支持错误解析、智能诊断、自动修复迭代。
---

# 鸿蒙项目调试器

自动编译鸿蒙项目，诊断错误，并提供修复方案或自动修复。

## 核心工作流

```
┌─────────────────────────────────────────────────────────────┐
│                     编译修复循环                              │
├─────────────────────────────────────────────────────────────┤
│  1. 执行编译 (hvigorw assembleHap)                          │
│         ↓                                                   │
│  2. 解析错误输出                                             │
│         ↓                                                   │
│  3. 匹配错误模式 → 查找修复方案                               │
│         ↓                                                   │
│  4. 应用修复                                                 │
│         ↓                                                   │
│  5. 重新编译验证                                             │
│         ↓                                                   │
│  [循环直到成功或达到最大尝试次数]                              │
└─────────────────────────────────────────────────────────────┘
```

## 快速使用

### 一键编译修复

```bash
# 在项目根目录执行
python3 scripts/build_and_fix.py --project-dir /path/to/project --max-attempts 5
```

### 仅诊断（不自动修复）

```bash
python3 scripts/build_and_fix.py --project-dir /path/to/project --diagnose-only
```

---

## 一、编译命令

### 基础编译

```bash
# 编译 HAP
./hvigorw assembleHap --mode module -p module=entry@default

# 编译 APP（用于上架）
./hvigorw assembleApp --mode module -p module=entry@default

# 清理
./hvigorw clean

# 完整重新编译
./hvigorw clean && ./hvigorw assembleHap --mode module -p module=entry@default
```

### 编译参数

| 参数 | 说明 |
|------|------|
| `--mode module` | 模块模式编译 |
| `-p module=entry@default` | 指定编译入口模块 |
| `--no-daemon` | 禁用守护进程（CI环境） |
| `-p product=default` | 指定产品配置 |

---

## 二、错误模式库

### 错误类型分类

| 类型 | 前缀 | 示例 |
|------|------|------|
| ArkTS编译错误 | `ArkTS:ERROR` | 语法、类型错误 |
| 链接错误 | `ERROR: failed to link` | 依赖问题 |
| 资源错误 | `ERROR: resource` | 资源未找到 |
| 配置错误 | `ERROR: config` | 配置文件问题 |
| 签名错误 | `ERROR: signing` | 签名配置问题 |

### 常见错误速查

详细错误模式和修复方案见 [references/error-patterns.md](references/error-patterns.md)

#### 高频错误 TOP 10

| 错误关键字 | 原因 | 快速修复 |
|------------|------|----------|
| `Cannot find name` | 变量/函数未定义 | 添加导入或声明 |
| `Type 'X' is not assignable` | 类型不匹配 | 类型转换或修正类型 |
| `Property 'X' does not exist` | 属性不存在 | 检查对象类型或添加属性 |
| `Module 'X' has no exported member` | 导入错误 | 检查导出或导入路径 |
| `Cannot find module` | 模块未找到 | 安装依赖或检查路径 |
| `Resource not found` | 资源缺失 | 添加资源文件 |
| `Attribute 'X' is deprecated` | 使用废弃API | 替换为新API |
| `Build profile not found` | 配置缺失 | 创建或修复配置文件 |
| `Signing config error` | 签名配置错误 | 检查签名文件和配置 |
| `HAP size exceeds limit` | 包体超限 | 压缩资源或分包 |

---

## 三、自动修复流程

### Step 1: 执行编译并捕获输出

```bash
./hvigorw assembleHap --mode module -p module=entry@default 2>&1 | tee build.log
```

### Step 2: 解析错误

使用脚本解析：

```bash
python3 scripts/parse_errors.py build.log
```

输出格式：
```json
{
  "errors": [
    {
      "file": "entry/src/main/ets/pages/Index.ets",
      "line": 25,
      "column": 10,
      "code": "ARKTS-1001",
      "message": "Cannot find name 'message'",
      "category": "undefined_variable",
      "suggestion": "添加变量声明或导入"
    }
  ],
  "warnings": [...],
  "summary": {
    "totalErrors": 3,
    "totalWarnings": 5,
    "byCategory": {
      "undefined_variable": 2,
      "type_mismatch": 1
    }
  }
}
```

### Step 3: 匹配修复方案

每个错误类别对应修复策略：

| 类别 | 修复策略 |
|------|----------|
| `undefined_variable` | 添加声明/导入 |
| `type_mismatch` | 类型转换 |
| `missing_property` | 添加属性 |
| `missing_import` | 添加import语句 |
| `deprecated_api` | 替换API |
| `resource_missing` | 创建资源文件 |

### Step 4: 应用修复

修复优先级：
1. **高优先级**：语法错误、类型错误（会阻止编译）
2. **中优先级**：废弃API警告、缺失属性
3. **低优先级**：代码风格警告

### Step 5: 验证修复

```bash
# 重新编译验证
./hvigorw assembleHap --mode module -p module=entry@default
```

---

## 四、常见问题修复示例

### 1. 变量未定义

**错误：**
```
ArkTS:ERROR File: entry/src/main/ets/pages/Index.ets:25:10
Cannot find name 'message'.
```

**修复：**
```typescript
// 修复前
Text(message)

// 修复后
@State message: string = 'Hello'  // 添加状态变量
Text(this.message)  // 使用 this
```

### 2. 类型不匹配

**错误：**
```
ArkTS:ERROR File: entry/src/main/ets/pages/Index.ets:30:5
Type 'string' is not assignable to type 'number'.
```

**修复：**
```typescript
// 修复前
let count: number = '10'

// 修复后
let count: number = 10
// 或
let count: number = parseInt('10')
```

### 3. 缺少导入

**错误：**
```
ArkTS:ERROR File: entry/src/main/ets/pages/Index.ets:5:1
Cannot find module '@ohos/router' or its corresponding type declarations.
```

**修复：**
```typescript
// 添加导入
import router from '@ohos.router'
```

### 4. 属性不存在

**错误：**
```
ArkTS:ERROR File: entry/src/main/ets/pages/Index.ets:40:5
Property 'pushUrl' does not exist on type 'Router'.
```

**修复：**
```typescript
// 修复前（旧API）
router.push({ url: 'pages/Detail' })

// 修复后（新API）
router.pushUrl({ url: 'pages/Detail' })
```

### 5. 资源未找到

**错误：**
```
ERROR: resource $r('app.media.logo') not found
```

**修复：**
```bash
# 检查资源文件是否存在
ls entry/src/main/resources/base/media/

# 如果不存在，添加图片
cp logo.png entry/src/main/resources/base/media/
```

### 6. 包体超限

**错误：**
```
ERROR: HAP size 2.5MB exceeds limit 2MB for atomic service
```

**修复方案：**
1. 压缩图片资源
```bash
# 转换为 WebP
for f in *.png; do
  cwebp -q 80 "$f" -o "${f%.png}.webp"
done
```
2. 移除未使用资源
3. 使用 HSP 共享包

---

## 五、调试技巧

### 查看详细编译日志

```bash
# 详细模式
./hvigorw assembleHap --mode module -p module=entry@default --stacktrace

# 调试模式
./hvigorw assembleHap --mode module -p module=entry@default --debug
```

### 检查依赖树

```bash
./hvigorw dependencies --configuration implementation
```

### 验证配置文件

```bash
# 检查 app.json5
cat AppScope/app.json5

# 检查 module.json5
cat entry/src/main/module.json5

# 验证 JSON 格式
python3 -m json.tool AppScope/app.json5
```

### 清理缓存

```bash
# 清理构建缓存
./hvigorw clean

# 清理 IDE 缓存
rm -rf .idea/
rm -rf .hvigor/
rm -rf build/
```

---

## 六、配置文件常见错误

### app.json5 常见问题

```json
{
  "app": {
    "bundleName": "com.example.app",  // 必须唯一
    "vendor": "example",
    "versionCode": 1000000,  // 必须是整数
    "versionName": "1.0.0",
    "bundleType": "atomicService"  // 元服务必须是这个值
  }
}
```

### module.json5 常见问题

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "deliveryWithInstall": true,
    "installationFree": true,  // 元服务必须为 true
    "abilities": [...],
    "extensionAbilities": [...]  // 卡片能力配置
  }
}
```

---

## 七、自动化脚本

### 完整编译修复脚本

见 `scripts/build_and_fix.py`

使用方法：
```bash
# 基本用法
python3 scripts/build_and_fix.py --project-dir /path/to/project

# 指定最大尝试次数
python3 scripts/build_and_fix.py --project-dir /path/to/project --max-attempts 10

# 仅诊断
python3 scripts/build_and_fix.py --project-dir /path/to/project --diagnose-only

# 显示详细输出
python3 scripts/build_and_fix.py --project-dir /path/to/project --verbose
```

---

## 八、最佳实践

### 预防措施

1. **启用严格模式**
```typescript
// 在 tsconfig.json 中
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true
  }
}
```

2. **使用 Lint 工具**
```bash
# 安装 ArkTS Lint
npm install -g @arkts/lint

# 运行检查
arkts-lint check entry/src/main/ets/
```

3. **增量编译**
```bash
# 开发时使用增量编译，更快发现问题
./hvigorw assembleHap --mode module -p module=entry@default -p incremental=true
```

### CI/CD 集成

```yaml
# .gitlab-ci.yml
build:
  script:
    - ./hvigorw clean
    - python3 scripts/build_and_fix.py --project-dir . --max-attempts 3
  artifacts:
    paths:
      - build/outputs/
```

---

## 参考资源

- [ArkTS错误码参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/arkts-errors-V5)
- [编译构建指南](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V5/ide-build-V5)
- [API参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references-V5/)
