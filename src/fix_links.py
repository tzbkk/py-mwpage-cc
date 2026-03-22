#!/usr/bin/env python3
"""
批量修复链接为简体版本
"""

import sys
import os
import re
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot
from batch_processor import BatchProcessor


def fix_links(old_text: str, new_text: str, bot: FandomBot, dry_run: bool = False):
    """搜索并修复链接"""
    print(f'搜索包含「{old_text}」的页面...')
    results = list(bot.site.search(old_text, what='text'))
    
    print(f'\n找到 {len(results)} 个页面\n')
    
    # 排除自己
    pages = [r['title'] for r in results if r['title'] != old_text]
    return pages


def fix_page(page_name: str, bot: FandomBot, old_text: str, new_text: str, dry_run: bool = False):
    """修复单个页面的链接"""
    page = bot.get_page(page_name)
    original = page.text()
    
    # 替换链接
    new_content = re.sub(re.escape(old_text), new_text, original)
    
    if original != new_content:
        if dry_run:
            return True, '📝 将会修改（预览模式）'
        else:
            page.edit(new_content, summary=f'修复链接：{old_text} → {new_text}')
            return True, '✓ 已修复'
    else:
        return None, 'ℹ️  无需修改'


def main():
    parser = argparse.ArgumentParser(
        description='批量修复链接为简体版本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "擅長捉弄的(原)高木同學" "擅长捉弄的(原)高木同学"
  %(prog)s "舊文本" "新文本" --limit 5
  %(prog)s "舊文本" "新文本" --dry-run
        """
    )
    
    parser.add_argument('old_text', help='要替换的旧文本')
    parser.add_argument('new_text', help='替换后的新文本')
    parser.add_argument('--limit', type=int, metavar='N', help='限制处理的页面数量')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    args = parser.parse_args()
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 搜索需要修复的页面
    pages = fix_links(args.old_text, args.new_text, bot, args.dry_run)
    
    if args.limit:
        pages = pages[:args.limit]
        print(f'限制处理数量: {args.limit} 页\n')
    
    if not pages:
        print('没有找到需要修复的页面')
        sys.exit(0)
    
    # 创建处理器并批量处理
    processor = lambda name, bot: fix_page(name, bot, args.old_text, args.new_text, args.dry_run)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(pages, processor, "批量修复链接")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
