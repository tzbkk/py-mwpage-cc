#!/usr/bin/env python3
"""
批量转换分类页面
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved
from batch_processor import create_batch_parser, parse_page_args, BatchProcessor


def convert_page(page_name: str, bot: FandomBot, dry_run: bool = False):
    """转换单个页面"""
    page = bot.get_page(page_name)
    if not page.exists:
        return False, "⚠️  页面不存在，跳过"
    
    original = page.text()
    new_content = bot.convert_text(original)
    
    if original == new_content:
        return None, "ℹ️  无需转换"
    
    valid, errors = verify_filenames_preserved(original, new_content)
    if not valid:
        error_msg = "⚠️  文件名验证失败:\n" + "\n".join(f"    {err}" for err in errors)
        return False, error_msg
    
    if dry_run:
        return True, "📝 将会修改（预览模式）"
    
    bot.edit_page(page, new_content, summary="转换为简体中文")
    return True, "✓ 已转换"


def main():
    parser = create_batch_parser(
        '批量转换分类页面',
        """
示例:
  %(prog)s "Category:音乐"
  %(prog)s "Category:音乐" "Category:动画"
  %(prog)s --from-file categories.txt
  %(prog)s "Category:音乐" --dry-run
        """
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
    processor = lambda name, bot: convert_page(name, bot, args.dry_run)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(page_names, processor, "批量转换分类页面")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
