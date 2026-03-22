#!/usr/bin/env python3
"""
批量更新分类引用为简体中文
"""
import sys
import os
import re
import argparse
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def update_category_ref(cat_name: str, bot: FandomBot, dry_run: bool = False):
    """更新单个分类的引用"""
    try:
        pages = bot.get_category_members(cat_name)
        print(f"\n更新引用 Category:{cat_name} 的页面...")
        print(f"  找到 {len(pages)} 个页面")
        
        updated = 0
        skipped = 0
        failed = 0
        
        for page in pages:
            try:
                original = page.text()
                new_content = original
                
                # 替换分类链接
                pattern = rf'\[\[Category:{re.escape(cat_name)}\]\]'
                replacement = f'[[Category:{bot.cc.convert(cat_name)}]]'
                new_content = re.sub(pattern, replacement, new_content)
                
                if original != new_content:
                    if dry_run:
                        print(f"    📝 {page.name} 将会修改（预览模式）")
                    else:
                        page.edit(new_content, summary="更新分类名称为简体中文")
                        print(f"    ✓ {page.name} 已更新")
                    updated += 1
                else:
                    print(f"    ℹ️  {page.name} 无需修改")
                    skipped += 1
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"    ⚠️  {page.name} 失败: {e}")
                failed += 1
        
        return updated, failed, skipped
    except Exception as e:
        print(f"  ⚠️  获取分类成员失败: {e}")
        return 0, 1, 0


def main():
    parser = argparse.ArgumentParser(
        description='批量更新分类引用为简体中文',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "片頭曲" "片尾曲"
  %(prog)s --from-file categories.txt
  %(prog)s "片頭曲" --dry-run
        """
    )
    
    parser.add_argument('categories', nargs='*', help='要更新的分类名称（不含 Category: 前缀）')
    parser.add_argument('--from-file', metavar='FILE', help='从文件读取分类列表')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    args = parser.parse_args()
    
    if not args.categories and not args.from_file:
        parser.print_help()
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 获取分类列表
    if args.from_file:
        try:
            with open(args.from_file, 'r', encoding='utf-8') as f:
                categories = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    else:
        categories = args.categories
    
    print(f"\n=== 批量更新分类引用 ===")
    print(f"共 {len(categories)} 个分类\n")
    
    total_updated = 0
    total_failed = 0
    total_skipped = 0
    
    for i, cat_name in enumerate(categories, 1):
        print(f"[{i}/{len(categories)}] {cat_name}")
        updated, failed, skipped = update_category_ref(cat_name, bot, args.dry_run)
        total_updated += updated
        total_failed += failed
        total_skipped += skipped
    
    print(f"\n{'📊 预览' if args.dry_run else '✅ 完成'}统计:")
    print(f"  - 总分类数: {len(categories)}")
    print(f"  - {'将更新' if args.dry_run else '已更新'}: {total_updated}")
    print(f"  - 跳过: {total_skipped}")
    print(f"  - 失败: {total_failed}")
    
    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
