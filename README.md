# 鸿蒙元服务 Skill Packages (OpenCode)

简介
- 本仓库的顶层文件夹全部作为 OpenCode 的 Skill 包，用于 OpenCode 的技能加载与执行。每个文件夹都包含一个可运行的技能实现，以及该技能的元数据和文档。

当前技能包
- harmonyos-api-snippets — HarmonyOS API 使用示例片段
- harmonyos-atomic-service — HarmonyOS 原子服务示例
- harmonyos-code-translator — 鸿蒙代码迁移/转换工具
- harmonyos-debugger — 调试相关工具与用例
- harmonyos-widget-gallery — 鸿蒙小部件示例画廊
- website-to-harmonyos — 网站迁移到鸿蒙的示例与工具
- website2uniapp — 从网站迁移到 uni-app 的工具
- miniprogram2uniapp — 小程序到 uni-app 的转换工具

使用方式
- OpenCode 将在运行时从根目录的子文件夹中发现并加载技能包。要添加新的技能包，在根目录创建一个新的文件夹，并实现一个标准的 skill.json（元数据）和入口脚本（如 index.js / main.js），以及可选的 README.md。
- skill.json 示例字段（推荐）：
  {
    "name": "skill-name",
    "version": "0.1.0",
    "description": "简要描述技能",
    "entry": "index.js"
  }
- 具体技能的实现与使用方式，请查看各自的 README.md。

- 技能描述
- - harmonyos-api-snippets — HarmonyOS API 使用示例片段，便于快速了解常用 API 的用法与行为。
- - harmonyos-atomic-service — HarmonyOS 原子服务示例，展示服务之间的通信与任务调度模式。
- - harmonyos-code-translator — 鸿蒙代码迁移/转换工具，辅助跨生态迁移场景。
- - harmonyos-debugger — 调试工具与用例，帮助定位并解决鸿蒙应用中的问题。
- - harmonyos-widget-gallery — 鸿蒙小部件（Widget）示例画廊，展示 UI 构建与交互模式。
- - website-to-harmonyos — 网站迁移到鸿蒙的示例与工具，包含结构与兼容性要点。
- - website2uniapp — 将网站应用迁移到 uni-app 的工具集合。
- - miniprogram2uniapp — 小程序到 uni-app 的转换工具与示例。

贡献
- 新增技能包：在根目录创建新文件夹，提供 skill.json、入口脚本和 README。
- 确保文档清晰、描述准确，方便他人理解与使用。

许可证
- MIT

联系
- 如有问题，请在本仓库中提出 Issue，或联系维护者。
