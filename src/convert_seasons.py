#!/usr/bin/env python3
"""
批量转换季度页面及其子页面
"""
import sys
import os
import argparse
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved


def convert_page(page, bot, dry_run=False, move=False):
    """转换单个页面"""
    page_name = page.name
    original = page.text()
    new_content = bot.convert_text(original)
    
    if original == new_content:
        print(f"    ℹ️  {page_name} 无需转换")
        return True
    
    valid, errors = verify_filenames_preserved(original, new_content)
    if not valid:
        print(f"    ⚠️  {page_name} 文件名验证失败:")
        for err in errors:
            print(f"      {err}")
        return False
    
    if dry_run:
        print(f"    📝 {page_name} 将会修改（预览模式）")
    else:
        bot.edit_page(page, new_content, summary="转换为简体中文")
        print(f"    ✓ {page_name} 内容已转换")
    
    # 移动页面
    if move:
        new_name = bot.cc.convert(page_name)
        if page_name != new_name:
            if dry_run:
                print(f"    📝 将会移动到 {new_name}（预览模式）")
            else:
                try:
                    bot.move_page(page, new_name, reason="改名为简体中文")
                    print(f"    ✓ 已移动到 {new_name}")
                except Exception as e:
                    print(f"    ⚠️  移动失败: {e}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='批量转换季度页面及其子页面',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "动画第一季" "动画第二季"
  %(prog)s --from-file pages.txt
  %(prog)s "动画第一季" --dry-run
  %(prog)s "动画第一季" --no-move  # 只转换内容不移动页面
        """
    )
    
    parser.add_argument('pages', nargs='*', help='要转换的季度页面名称')
    parser.add_argument('--from-file', metavar='FILE', help='从文件读取页面列表')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--no-move', action='store_true', help='不移动页面，只转换内容')
    parser.add_argument('--no-subpages', action='store_true', help='不处理子页面')
    
    args = parser.parse_args()
    
    if not args.pages and not args.from_file:
        parser.print_help()
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 获取页面列表
    if args.from_file:
        try:
            with open(args.from_file, 'r', encoding='utf-8') as f:
                page_names = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    else:
        page_names = args.pages
    
    print(f"\n=== 批量转换季度页面 ===")
    print(f"共 {len(page_names)} 个主页面\n")
    
    converted = 0
    failed = 0
    skipped = 0
    subpage_converted = 0
    subpage_failed = 0
    
    move_pages = not args.no_move
    
    # 转换主页面
    for i, page_name in enumerate(page_names, 1):
        print(f"\n[{i}/{len(page_names)}] 主页面: {page_name}")
        
        try:
            page = bot.get_page(page_name)
            if not page.exists:
                print("  ⚠️  页面不存在，跳过")
                skipped += 1
                continue
            
            result = convert_page(page, bot, args.dry_run, move_pages)
            
            if result:
                converted += 1
            else:
                failed += 1
            
            # 处理子页面
            if not args.no_subpages:
                print(f"\n  查找子页面...")
                try:
                    subpages = bot.get_subpages(page_name)
                    print(f"  找到 {len(subpages)} 个子页面")
                    
                    for j, subpage in enumerate(subpages, 1):
                        print(f"  [{j}/{len(subpages)}] {subpage.name}")
                        result = convert_page(subpage, bot, args.dry_run, move_pages)
                        
                        if result:
                            subpage_converted += 1
                        else:
                            subpage_failed += 1
                        
                        if j < len(subpages):
                            time.sleep(0.3)
                    
                except Exception as e:
                    print(f"  ⚠️  获取子页面失败: {e}")
            
            if i < len(page_names):
                time.sleep(0.5)
                
        except Exception as e:
            print(f"  ⚠️  失败: {e}")
            failed += 1
            
            if 'ratelimited' in str(e).lower():
                print("  ⏳ 遇到速率限制，等待 60 秒...")
                time.sleep(60)
    
    print(f"\n{'📊 预览' if args.dry_run else '✅ 完成'}统计:")
    print(f"  - 主页面:")
    print(f"    总数: {len(page_names)}")
    print(f"    {'将处理' if args.dry_run else '已处理'}: {converted}")
    print(f"    跳过: {skipped}")
    print(f"    失败: {failed}")
    if not args.no_subpages:
        print(f"  - 子页面:")
        print(f"    {'将处理' if args.dry_run else '已处理'}: {subpage_converted}")
        print(f"    失败: {subpage_failed}")
    
    total_failed = failed + subpage_failed
    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
