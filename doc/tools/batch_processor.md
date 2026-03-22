# batch_processor.py - 批处理工具模块

## 功能

提供通用的批处理功能，简化批量页面操作的实现。

## 主要组件

### BatchProcessor 类

批处理器类，提供统一的批量处理功能。

#### 初始化

```python
from batch_processor import BatchProcessor
from fandom_bot import FandomBot

bot = FandomBot()
batch = BatchProcessor(bot, dry_run=False, delay=0.5)
```

**参数**:
- `bot`: FandomBot 实例
- `dry_run`: 是否为预览模式
- `delay`: 每个操作之间的延迟（秒）

#### 方法

**process_pages()**

批量处理页面。

```python
def process_pages(pages: List[str], processor: Callable,
                  title: str = "批量处理", show_progress: bool = True)
```

**参数**:
- `pages`: 页面名称列表
- `processor`: 处理函数，签名为 `processor(page_name, bot) -> (result, message)`
  - `result`: True (成功) / False (失败) / None (跳过)
  - `message`: str (处理结果描述)
- `title`: 处理标题
- `show_progress`: 是否显示进度

**返回值**:
- `bool`: 是否全部成功

**示例**:

```python
def convert_page(page_name: str, bot: FandomBot):
    page = bot.get_page(page_name)
    original = page.text()
    new_content = bot.convert_text(original)
    
    if original == new_content:
        return None, "ℹ️  无需转换"
    
    bot.edit_page(page, new_content, summary="转换为简体中文")
    return True, "✓ 已转换"

pages = ["页面1", "页面2", "页面3"]
batch.process_pages(pages, convert_page, "批量转换")
```

**输出示例**:

```
=== 批量转换 ===
共 3 个页面

[1/3] 页面1
  ✓ 已转换

[2/3] 页面2
  ℹ️  无需转换

[3/3] 页面3
  ✓ 已转换

✅ 完成统计:
  - 已处理: 2
  - 跳过: 1
  - 失败: 0
```

**print_statistics()**

打印统计信息。

```python
def print_statistics(extra_stats: Dict[str, int] = None)
```

**参数**:
- `extra_stats`: 额外的统计信息字典

**示例**:

```python
batch.print_statistics({
    "子页面": 10,
    "移动": 5
})
```

### read_page_list() 函数

从文件读取页面列表。

```python
from batch_processor import read_page_list

pages = read_page_list("pages.txt")
```

**参数**:
- `file_path`: 文件路径

**返回值**:
- `List[str]`: 页面名称列表

**文件格式**:
```
页面1
页面2
# 这是注释，会被忽略
页面3
```

### create_batch_parser() 函数

创建标准的批处理命令行解析器。

```python
from batch_processor import create_batch_parser

parser = create_batch_parser(
    '工具描述',
    '''
示例:
  %(prog)s "页面1" "页面2"
  %(prog)s --from-file pages.txt
  %(prog)s "页面1" --dry-run
    '''
)
```

**参数**:
- `description`: 工具描述
- `epilog`: 帮助信息尾部

**返回值**:
- `argparse.ArgumentParser`

**默认参数**:
- `pages *`: 要处理的页面名称
- `--from-file FILE`: 从文件读取页面列表
- `--dry-run`: 预览模式

### parse_page_args() 函数

解析页面参数（命令行或文件）。

```python
from batch_processor import parse_page_args

args, page_names, should_exit = parse_page_args(parser)

if should_exit or page_names is None:
    sys.exit(1)
```

**参数**:
- `parser`: argparse.ArgumentParser

**返回值**:
- `args`: 解析后的参数
- `page_names`: 页面名称列表
- `should_exit`: 是否应该退出程序

## 使用示例

### 完整示例

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot
from batch_processor import create_batch_parser, parse_page_args, BatchProcessor


def process_page(page_name: str, bot: FandomBot):
    """处理单个页面"""
    page = bot.get_page(page_name)
    original = page.text()
    new_content = bot.convert_text(original)
    
    if original == new_content:
        return None, "ℹ️  无需转换"
    
    bot.edit_page(page, new_content, summary="转换为简体中文")
    return True, "✓ 已转换"


def main():
    parser = create_batch_parser(
        '批量转换页面',
        '''
示例:
  %(prog)s "页面1" "页面2"
  %(prog)s --from-file pages.txt
  %(prog)s "页面1" --dry-run
        '''
    )
    
    args, page_names, should_exit = parse_page_args(parser)
    if should_exit or page_names is None:
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 创建处理器并批量处理
    processor = lambda name, bot: process_page(name, bot)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(page_names, processor, "批量转换")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

## 特性

- 统一的批处理逻辑
- 自动错误处理和速率限制
- 统一的进度显示
- 统一的统计信息
- 支持 dry-run 模式
- 支持从文件读取页面列表
- 简化新工具的开发

## 使用场景

- 需要批量处理页面的新工具
- 需要统一用户反馈的工具
- 需要错误处理和速率限制的工具

## 注意事项

- processor 函数必须返回 (result, message) 元组
- result 必须是 True/False/None
- message 会直接显示给用户
- 自动处理速率限制（60秒等待）
