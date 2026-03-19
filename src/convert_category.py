#!/usr/bin/env python3
"""
Fandom Wiki 分类转换工具

转换分类下的所有页面从繁体中文到简体中文。

重要：使用前请先用 --test 模式在单个页面上测试！
"""

import sys
import os
import re
import argparse
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot

def protect_filenames(text):
    """保护文件名不被转换"""
    protected = {}
    counter = [0]
    
    def get_placeholder():
        placeholder = f'__FILE_{counter[0]}__'
        counter[0] += 1
        return placeholder
    
    file_pattern1 = r'(File:[^\|\]\[\n]+?\.(?:jpg|jpeg|png|gif|svg|webp|bmp))'
    def replace_file1(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    text = re.sub(file_pattern1, replace_file1, text, flags=re.IGNORECASE)
    
    file_pattern2 = r'([^\|\[\]\n]+\.(?:jpg|jpeg|png|gif|svg|webp|bmp)(?=\|))'
    def replace_file2(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    text = re.sub(file_pattern2, replace_file2, text, flags=re.IGNORECASE)
    
    file_pattern3 = r'(\[\[File:[^\]]+?\.(?:jpg|jpeg|png|gif|svg|webp|bmp)[^\]]*?\]\])'
    def replace_file3(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    text = re.sub(file_pattern3, replace_file3, text, flags=re.IGNORECASE)
    
    return text, protected

def restore_filenames(text, protected):
    """恢复保护的文件名"""
    for placeholder, original in sorted(protected.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(placeholder, original)
    return text

def convert_page(text, bot):
    """转换单个页面的文本"""
    text, protected = protect_filenames(text)
    text = bot.cc.convert(text)
    text = restore_filenames(text, protected)
    return text

def verify_conversion(original, new_content):
    """验证转换结果"""
    files_orig = set(re.findall(r'[^\s\[\]|=]+\.(?:jpg|jpeg|png|gif)', original, re.IGNORECASE))
    files_new = set(re.findall(r'[^\s\[\]|=]+\.(?:jpg|jpeg|png|gif)', new_content, re.IGNORECASE))
    return files_orig == files_new

def list_category_pages(category_name, bot, limit=None):
    """列出分类下的所有页面"""
    print(f"📋 获取 Category:{category_name} 的页面...")
    pages = list(bot.get_category_members(category_name))
    
    if limit:
        pages = pages[:limit]
    
    print(f"找到 {len(pages)} 个页面\n")
    return pages

def convert_category(category_name, bot, dry_run=False, limit=None, test_first=True):
    """转换分类下的所有页面"""
    print(f"=== 转换分类 ===")
    print(f"分类: Category:{category_name}\n")
    
    pages = list_category_pages(category_name, bot, limit)
    
    if not pages:
        print("ℹ️  没有找到页面")
        return True
    
    # 测试第一个页面
    if test_first and not dry_run:
        print("🔍 先测试第一个页面...\n")
        first_page = pages[0]
        print(f"📄 测试: {first_page.name}")
        
        original = first_page.text()
        new_content = convert_page(original, bot)
        
        if original != new_content:
            valid = verify_conversion(original, new_content)
            
            if not valid:
                print("❌ 测试失败：文件名验证未通过")
                print("💡 使用 --no-test-first 跳过测试，或使用 --dry-run 预览")
                return False
            
            print("✓ 测试通过\n")
            print("👉 请到 Wiki 上检查这个页面，确认无误后继续")
            response = input("继续批量转换？(y/n): ")
            if response.lower() != 'y':
                print("已取消")
                return False
        else:
            print("ℹ️  第一个页面无需修改\n")
    
    # 批量转换
    print(f"\n开始批量转换...\n")
    
    converted = 0
    failed = 0
    skipped = 0
    
    for i, page in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page.name}")
        
        try:
            original = page.text()
            new_content = convert_page(original, bot)
            
            if original == new_content:
                print("  - 无需修改")
                skipped += 1
                continue
            
            if not verify_conversion(original, new_content):
                print("  ⚠️  验证失败，跳过")
                failed += 1
                continue
            
            if dry_run:
                print("  📝 将会修改（预览模式）")
                converted += 1
            else:
                bot.edit_page(page, new_content, summary="转换为简体中文")
                print("  ✓ 已转换")
                converted += 1
                
                if i < len(pages):
                    time.sleep(1)
                    
        except Exception as e:
            print(f"  ⚠️  失败: {e}")
            failed += 1
            
            if 'ratelimited' in str(e).lower():
                print("  ⏳ 遇到速率限制，等待 60 秒...")
                time.sleep(60)
    
    print(f"\n{'📊 预览' if dry_run else '✅ 完成'}统计:")
    print(f"  - 总页面数: {len(pages)}")
    print(f"  - {'将修改' if dry_run else '已修改'}: {converted}")
    print(f"  - 跳过: {skipped}")
    print(f"  - 失败: {failed}")
    
    return failed == 0

def main():
    parser = argparse.ArgumentParser(
        description='Fandom Wiki 分类转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出分类下的页面
  %(prog)s "音乐" --list
  
  # 转换分类下的所有页面
  %(prog)s "音乐"
  
  # 预览转换
  %(prog)s "音乐" --dry-run
  
  # 限制转换数量（用于测试）
  %(prog)s "音乐" --limit 5
  
  # 跳过第一个页面测试
  %(prog)s "音乐" --no-test-first
        """
    )
    
    parser.add_argument('category', help='分类名称（不需要包含 Category: 前缀）')
    parser.add_argument('--list', action='store_true', help='只列出页面，不转换')
    parser.add_argument('--dry-run', action='store_true', help='预览模式：显示将要修改但不保存')
    parser.add_argument('--limit', type=int, metavar='N', help='限制转换的页面数量')
    parser.add_argument('--no-test-first', action='store_true', help='跳过第一个页面的测试')
    
    args = parser.parse_args()
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    if args.list:
        pages = list_category_pages(args.category, bot, args.limit)
        print("页面列表:")
        for i, page in enumerate(pages, 1):
            print(f"  {i}. {page.name}")
    else:
        success = convert_category(
            args.category, 
            bot, 
            dry_run=args.dry_run,
            limit=args.limit,
            test_first=not args.no_test_first
        )
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
