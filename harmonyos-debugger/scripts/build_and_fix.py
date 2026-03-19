#!/usr/bin/env python3
"""
鸿蒙项目自动编译修复工具

功能：
1. 执行 hvigor 编译
2. 解析编译错误
3. 匹配错误模式并提供修复方案
4. 自动应用修复并重新编译
5. 循环直到成功或达到最大尝试次数

用法：
    python3 build_and_fix.py --project-dir /path/to/project [options]

选项：
    --project-dir     项目根目录（必需）
    --max-attempts    最大修复尝试次数（默认 5）
    --diagnose-only   仅诊断，不自动修复
    --verbose         显示详细输出
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class CompileError:
    """编译错误"""
    file: str
    line: int
    column: int
    code: str
    message: str
    category: str
    suggestion: str
    raw: str


@dataclass
class FixSuggestion:
    """修复建议"""
    error: CompileError
    fix_type: str
    fix_content: str
    confidence: float  # 0-1, 自动修复置信度


# 错误模式匹配规则
ERROR_PATTERNS = [
    # ArkTS 编译错误
    {
        'pattern': r"ArkTS:ERROR File: (?P<file>[^:]+):(?P<line>\d+):(?P<column>\d+)\s*\n(?P<message>Cannot find name '(?P<name>\w+)')",
        'category': 'undefined_variable',
        'code': 'ARKTS-1001',
        'suggestion': '变量未定义，需要添加声明或导入',
        'fix_type': 'add_declaration',
    },
    {
        'pattern': r"ArkTS:ERROR File: (?P<file>[^:]+):(?P<line>\d+):(?P<column>\d+)\s*\n(?P<message>Type '(?P<type1>[^']+)' is not assignable to type '(?P<type2>[^']+)')",
        'category': 'type_mismatch',
        'code': 'ARKTS-1002',
        'suggestion': '类型不匹配，需要类型转换',
        'fix_type': 'type_conversion',
    },
    {
        'pattern': r"ArkTS:ERROR File: (?P<file>[^:]+):(?P<line>\d+):(?P<column>\d+)\s*\n(?P<message>Property '(?P<prop>\w+)' does not exist on type '(?P<type>\w+)')",
        'category': 'missing_property',
        'code': 'ARKTS-1003',
        'suggestion': '属性不存在，需要检查类型定义',
        'fix_type': 'add_property',
    },
    {
        'pattern': r"ArkTS:ERROR File: (?P<file>[^:]+):(?P<line>\d+):(?P<column>\d+)\s*\n(?P<message>Cannot find module '(?P<module>[^']+)' or its corresponding type declarations)",
        'category': 'missing_module',
        'code': 'ARKTS-1004',
        'suggestion': '模块未找到，需要安装依赖或检查路径',
        'fix_type': 'add_import',
    },
    {
        'pattern': r"ArkTS:ERROR File: (?P<file>[^:]+):(?P<line>\d+):(?P<column>\d+)\s*\n(?P<message>Duplicate identifier '(?P<name>\w+)')",
        'category': 'duplicate_identifier',
        'code': 'ARKTS-1006',
        'suggestion': '重复标识符，需要重命名或删除重复声明',
        'fix_type': 'rename_or_remove',
    },
    # 资源错误
    {
        'pattern': r"ERROR: resource \$r\('app\.(?P<type>\w+)\.(?P<name>\w+)'\) not found",
        'category': 'resource_missing',
        'code': 'RES-001',
        'suggestion': '资源未找到，需要创建资源文件',
        'fix_type': 'create_resource',
    },
    # 包大小错误
    {
        'pattern': r"ERROR: HAP size (?P<size>[\d.]+)MB exceeds limit (?P<limit>[\d.]+)MB",
        'category': 'hap_size_exceeded',
        'code': 'BUILD-003',
        'suggestion': 'HAP包体超限，需要压缩资源',
        'fix_type': 'compress_resources',
    },
    # 签名错误
    {
        'pattern': r"ERROR: Signing config not found or invalid",
        'category': 'signing_error',
        'code': 'BUILD-002',
        'suggestion': '签名配置错误，需要检查签名文件',
        'fix_type': 'fix_signing',
    },
    # 依赖错误
    {
        'pattern': r"ERROR: Could not resolve dependency: (?P<dep>[^\s]+)",
        'category': 'dependency_error',
        'code': 'DEPS-001',
        'suggestion': '依赖解析失败，需要检查依赖配置',
        'fix_type': 'fix_dependency',
    },
]

# 废弃 API 替换表
DEPRECATED_APIS = {
    'router.push': 'router.pushUrl',
    'router.replace': 'router.replaceUrl',
    'featureAbility': '@ohos.app.ability',
}

# 常用导入映射
COMMON_IMPORTS = {
    'router': "import router from '@ohos.router'",
    'http': "import http from '@ohos.net.http'",
    'preferences': "import preferences from '@ohos.data.preferences'",
    'promptAction': "import promptAction from '@ohos.promptAction'",
    'window': "import window from '@ohos.window'",
    'common': "import common from '@ohos.app.ability.common'",
    'util': "import util from '@ohos.util'",
    'hilog': "import hilog from '@ohos.hilog'",
}


class HarmonyOSBuilder:
    """鸿蒙项目编译器"""

    def __init__(self, project_dir: str, verbose: bool = False):
        self.project_dir = os.path.abspath(project_dir)
        self.verbose = verbose
        self.build_log = ""

    def run_build(self) -> tuple[bool, str]:
        """执行编译"""
        cmd = ['./hvigorw', 'assembleHap', '--mode', 'module', '-p', 'module=entry@default']

        if self.verbose:
            print(f"执行命令: {' '.join(cmd)}")
            print(f"工作目录: {self.project_dir}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )

            self.build_log = result.stdout + result.stderr

            if self.verbose:
                print("\n--- 编译输出 ---")
                print(self.build_log[:2000])  # 截取前2000字符
                print("--- 输出结束 ---\n")

            return result.returncode == 0, self.build_log

        except subprocess.TimeoutExpired:
            return False, "编译超时（超过5分钟）"
        except FileNotFoundError:
            return False, f"找不到 hvigorw，请确认在鸿蒙项目根目录下运行"
        except Exception as e:
            return False, f"编译执行错误: {str(e)}"

    def clean(self) -> bool:
        """清理构建"""
        try:
            result = subprocess.run(
                ['./hvigorw', 'clean'],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except:
            return False


class ErrorParser:
    """错误解析器"""

    def __init__(self):
        self.patterns = ERROR_PATTERNS

    def parse(self, build_log: str) -> list[CompileError]:
        """解析编译日志中的错误"""
        errors = []

        for pattern_info in self.patterns:
            pattern = pattern_info['pattern']
            for match in re.finditer(pattern, build_log, re.MULTILINE):
                error = CompileError(
                    file=match.group('file') if 'file' in match.groupdict() else '',
                    line=int(match.group('line')) if 'line' in match.groupdict() else 0,
                    column=int(match.group('column')) if 'column' in match.groupdict() else 0,
                    code=pattern_info['code'],
                    message=match.group('message') if 'message' in match.groupdict() else match.group(0),
                    category=pattern_info['category'],
                    suggestion=pattern_info['suggestion'],
                    raw=match.group(0)
                )
                errors.append(error)

        # 去重
        seen = set()
        unique_errors = []
        for e in errors:
            key = (e.file, e.line, e.message)
            if key not in seen:
                seen.add(key)
                unique_errors.append(e)

        return unique_errors

    def categorize(self, errors: list[CompileError]) -> dict[str, list[CompileError]]:
        """按类别分组"""
        categories = {}
        for error in errors:
            if error.category not in categories:
                categories[error.category] = []
            categories[error.category].append(error)
        return categories


class FixEngine:
    """修复引擎"""

    def __init__(self, project_dir: str, verbose: bool = False):
        self.project_dir = project_dir
        self.verbose = verbose

    def analyze(self, error: CompileError) -> FixSuggestion:
        """分析错误并生成修复建议"""
        fix_type = self._get_fix_type(error)
        fix_content = self._generate_fix_content(error, fix_type)
        confidence = self._calculate_confidence(error, fix_type)

        return FixSuggestion(
            error=error,
            fix_type=fix_type,
            fix_content=fix_content,
            confidence=confidence
        )

    def _get_fix_type(self, error: CompileError) -> str:
        """获取修复类型"""
        type_map = {
            'undefined_variable': 'add_declaration',
            'type_mismatch': 'type_conversion',
            'missing_property': 'add_property',
            'missing_module': 'add_import',
            'duplicate_identifier': 'rename_or_remove',
            'resource_missing': 'create_resource',
            'hap_size_exceeded': 'compress_resources',
            'signing_error': 'fix_signing',
            'dependency_error': 'fix_dependency',
        }
        return type_map.get(error.category, 'manual_fix')

    def _generate_fix_content(self, error: CompileError, fix_type: str) -> str:
        """生成修复内容"""
        if fix_type == 'add_declaration':
            # 提取变量名
            match = re.search(r"Cannot find name '(\w+)'", error.message)
            if match:
                var_name = match.group(1)
                # 检查是否是常用模块
                if var_name in COMMON_IMPORTS:
                    return f"添加导入: {COMMON_IMPORTS[var_name]}"
                return f"添加声明: @State {var_name}: string = ''"

        elif fix_type == 'add_import':
            match = re.search(r"Cannot find module '([^']+)'", error.message)
            if match:
                module = match.group(1)
                return f"安装依赖: ohpm install {module} 或检查导入路径"

        elif fix_type == 'type_conversion':
            match = re.search(r"Type '(\w+)' is not assignable to type '(\w+)'", error.message)
            if match:
                from_type, to_type = match.groups()
                return f"类型转换: {from_type} → {to_type}，使用转换函数"

        elif fix_type == 'create_resource':
            match = re.search(r"app\.(\w+)\.(\w+)", error.message)
            if match:
                res_type, res_name = match.groups()
                return f"创建资源: resources/base/{res_type}/{res_name}"

        elif fix_type == 'compress_resources':
            return "压缩图片资源或使用 HSP 分包"

        return "请手动检查并修复"

    def _calculate_confidence(self, error: CompileError, fix_type: str) -> float:
        """计算自动修复置信度"""
        high_confidence = ['add_declaration', 'add_import', 'create_resource']
        medium_confidence = ['type_conversion', 'rename_or_remove']

        if fix_type in high_confidence:
            return 0.8
        elif fix_type in medium_confidence:
            return 0.5
        return 0.3

    def apply_fix(self, suggestion: FixSuggestion) -> bool:
        """应用修复（自动化程度取决于置信度）"""
        if suggestion.confidence < 0.7:
            return False

        # 高置信度修复
        if suggestion.fix_type == 'add_declaration':
            return self._add_declaration(suggestion)
        elif suggestion.fix_type == 'add_import':
            return self._add_import(suggestion)

        return False

    def _add_declaration(self, suggestion: FixSuggestion) -> bool:
        """添加变量声明"""
        # 这里可以读取文件并自动添加声明
        # 但建议由 AI 来做更准确
        return False

    def _add_import(self, suggestion: FixSuggestion) -> bool:
        """添加导入语句"""
        # 同上，建议由 AI 处理
        return False


def print_report(errors: list[CompileError], suggestions: list[FixSuggestion], verbose: bool = False):
    """打印诊断报告"""
    print("\n" + "=" * 60)
    print("📊 编译诊断报告")
    print("=" * 60)

    if not errors:
        print("✅ 编译成功，无错误！")
        return

    # 按类别分组
    categories = {}
    for e in errors:
        if e.category not in categories:
            categories[e.category] = []
        categories[e.category].append(e)

    print(f"\n共发现 {len(errors)} 个错误，分为 {len(categories)} 类：")

    for category, errs in categories.items():
        print(f"\n【{category}】({len(errs)} 个)")
        for e in errs[:3]:  # 每类最多显示3个
            print(f"  📄 {e.file}:{e.line}")
            print(f"     {e.message}")
            print(f"     💡 {e.suggestion}")
        if len(errs) > 3:
            print(f"  ... 还有 {len(errs) - 3} 个同类错误")

    print("\n" + "-" * 60)
    print("🔧 修复建议")
    print("-" * 60)

    for sug in suggestions[:10]:  # 最多显示10个
        confidence_icon = "🟢" if sug.confidence >= 0.7 else "🟡" if sug.confidence >= 0.4 else "🔴"
        print(f"\n{confidence_icon} {sug.fix_content}")
        print(f"   置信度: {sug.confidence:.0%}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='鸿蒙项目自动编译修复工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python3 build_and_fix.py --project-dir /path/to/project

  # 指定最大尝试次数
  python3 build_and_fix.py --project-dir /path/to/project --max-attempts 10

  # 仅诊断，不修复
  python3 build_and_fix.py --project-dir /path/to/project --diagnose-only
        """
    )

    parser.add_argument('--project-dir', required=True, help='项目根目录')
    parser.add_argument('--max-attempts', type=int, default=5, help='最大修复尝试次数（默认 5）')
    parser.add_argument('--diagnose-only', action='store_true', help='仅诊断，不自动修复')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')

    args = parser.parse_args()

    # 验证项目目录
    if not os.path.isdir(args.project_dir):
        print(f"❌ 错误: 目录不存在: {args.project_dir}")
        sys.exit(1)

    hvigorw = os.path.join(args.project_dir, 'hvigorw')
    if not os.path.exists(hvigorw):
        print(f"❌ 错误: 不是有效的鸿蒙项目（找不到 hvigorw）")
        sys.exit(1)

    # 初始化组件
    builder = HarmonyOSBuilder(args.project_dir, args.verbose)
    parser_engine = ErrorParser()
    fix_engine = FixEngine(args.project_dir, args.verbose)

    attempt = 0

    while attempt < args.max_attempts:
        attempt += 1
        print(f"\n🔄 第 {attempt}/{args.max_attempts} 次编译...")

        # 执行编译
        success, build_log = builder.run_build()

        if success:
            print("\n✅ 编译成功！")
            print_report([], [], args.verbose)
            sys.exit(0)

        # 解析错误
        errors = parser_engine.parse(build_log)

        if not errors:
            print("\n⚠️ 编译失败但未能解析出具体错误")
            print("请查看完整日志手动排查")
            if args.verbose:
                print(build_log)
            sys.exit(1)

        # 生成修复建议
        suggestions = [fix_engine.analyze(e) for e in errors]

        # 打印报告
        print_report(errors, suggestions, args.verbose)

        if args.diagnose_only:
            print("\n📋 诊断模式：不执行自动修复")
            sys.exit(1)

        # 检查是否有可自动修复的错误
        auto_fixable = [s for s in suggestions if s.confidence >= 0.7]

        if not auto_fixable:
            print("\n⚠️ 没有可自动修复的错误，需要手动处理")
            sys.exit(1)

        print(f"\n🔧 尝试自动修复 {len(auto_fixable)} 个错误...")

        # 应用修复（这里需要 AI 配合）
        for sug in auto_fixable:
            if fix_engine.apply_fix(sug):
                print(f"  ✅ 已修复: {sug.fix_content}")
            else:
                print(f"  ⏭️ 跳过自动修复（建议 AI 处理）: {sug.fix_content}")

        print("\n准备重新编译...")

    print(f"\n❌ 达到最大尝试次数 ({args.max_attempts})，仍有错误")
    sys.exit(1)


if __name__ == '__main__':
    main()
