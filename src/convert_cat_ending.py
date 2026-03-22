#!/usr/bin/env python3
"""
批量转换分类页面并改名
"""
import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved
from batch_processor import create_batch_parser, parse_page_args, BatchProcessor


def convert_category(cat_name: str, bot: FandomBot, dry_run: bool = False):
    """转换单个分类"""
    new_name = bot.cc.convert(cat_name)
    
    cat = bot.get_page(f"Category:{cat_name}")
    if not cat.exists:
        return False, "⚠️  页面不存在，跳过"
    
    content = cat.text()
    new_content = bot.convert_text(content)
    
    # 转换内容
    if content != new_content:
        valid, errors = verify_filenames_preserved(content, new_content)
        if not valid:
            error_msg = "⚠️  文件名验证失败:\n" + "\n".join(f"    {err}" for err in errors)
            return False, error_msg
        
        if dry_run:
            print("  📝 内容将会修改（预览模式）")
        else:
            bot.edit_page(cat, new_content, summary="转换为简体中文")
            print("  ✓ 内容已转换")
    else:
        print("  ℹ️  内容无需转换")
    
    # 移动页面（如果名称不同）
    if cat_name != new_name:
        if dry_run:
            print(f"  📝 将会移动到 Category:{new_name}（预览模式）")
        else:
            try:
                bot.move_page(cat, f"Category:{new_name}", reason="改名为简体中文")
                print(f"  ✓ 已移动到 Category:{new_name}")
            except Exception as e:
                print(f"  ⚠️  移动失败: {e}")
                return False
    
    return True, "✓ 处理完成"


def main():
    parser = create_batch_parser(
        '批量转换分类页面并改名',
        """
示例:
  %(prog)s "片頭曲" "片尾曲"
  %(prog)s --from-file categories.txt
  %(prog)s "片頭曲" --dry-run
        """
    )
    
    parser.set_defaults(description='要转换的分类名称（不含 Category: 前缀）')
    args, categories, should_exit = parse_page_args(parser)
    if should_exit or categories is None:
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 创建处理器并批量处理
    processor = lambda name, bot: convert_category(name, bot, args.dry_run)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(categories, processor, "批量转换分类页面")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
