#!/usr/bin/env python3
"""
批量移动页面（将繁体名称改为简体）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot
from batch_processor import create_batch_parser, parse_page_args, BatchProcessor


def move_page(page_name: str, bot: FandomBot, dry_run: bool = False):
    """移动单个页面"""
    new_name = bot.cc.convert(page_name)
    
    if page_name == new_name:
        return None, f"ℹ️  无需移动（名称已经是简体）"
    
    print(f"  目标名称: {new_name}")
    
    if dry_run:
        return True, f"📝 将会移动（预览模式）"
    
    page = bot.get_page(page_name)
    if page.exists:
        bot.move_page(page, new_name, reason="改名为简体中文")
        return True, "✓ 已移动"
    else:
        return False, "⚠️  页面不存在（可能已移动）"


def main():
    parser = create_batch_parser(
        '批量移动页面（将繁体名称改为简体）',
        """
示例:
  %(prog)s "雖然不會說出口。" "愛歌" "小小戀歌"
  %(prog)s --from-file pages.txt
  %(prog)s "雖然不會說出口。" --dry-run
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
    processor = lambda name, bot: move_page(name, bot, args.dry_run)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(page_names, processor, "批量移动页面")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
