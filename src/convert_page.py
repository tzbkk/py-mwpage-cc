#!/usr/bin/env python3
"""
Fandom Wiki 通用转换工具

将任意页面从繁体中文转换为简体中文。

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
    
    # 保护 File:xxx.jpg 格式
    file_pattern1 = r'(File:[^\|\]\[\n]+?\.(?:jpg|jpeg|png|gif|svg|webp|bmp))'
    def replace_file1(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    text = re.sub(file_pattern1, replace_file1, text, flags=re.IGNORECASE)
    
    # 保护独立的文件名（在 gallery 标签中或其他地方）
    file_pattern2 = r'([^\|\[\]\n]+\.(?:jpg|jpeg|png|gif|svg|webp|bmp)(?=\|))'
    def replace_file2(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    text = re.sub(file_pattern2, replace_file2, text, flags=re.IGNORECASE)
    
    # 保护 [[File:xxx.jpg]] 格式
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

def verify_conversion(original, new_content, page_name):
    """验证转换结果"""
    import re
    
    print(f"\n📊 转换统计 - {page_name}")
    
    # 行数统计
    lines_orig = original.split('\n')
    lines_new = new_content.split('\n')
    changed_lines = sum(1 for o, n in zip(lines_orig, lines_new) if o != n)
    print(f"  - 总行数: {len(lines_orig)}")
    print(f"  - 修改行数: {changed_lines}")
    
    # 文件名检查
    files_orig = set(re.findall(r'[^\s\[\]|=]+\.(?:jpg|jpeg|png|gif)', original, re.IGNORECASE))
    files_new = set(re.findall(r'[^\s\[\]|=]+\.(?:jpg|jpeg|png|gif)', new_content, re.IGNORECASE))
    
    if files_orig == files_new:
        print(f"  ✓ 文件名保护正常 ({len(files_orig)} 个文件)")
        return True
    else:
        print(f"  ⚠️  文件名可能有问题:")
        if files_orig - files_new:
            print(f"    丢失: {files_orig - files_new}")
        if files_new - files_orig:
            print(f"    新增: {files_new - files_orig}")
        return False

def convert_single_page(page_name, bot, dry_run=False, show_diff=False):
    """转换单个页面"""
    print(f"📄 转换页面: {page_name}")
    
    page = bot.get_page(page_name)
    if not page.exists:
        print(f"❌ 页面不存在: {page_name}")
        return False
    
    original = page.text()
    new_content = convert_page(original, bot)
    
    if original == new_content:
        print("ℹ️  页面无需修改")
        return True
    
    # 验证转换
    valid = verify_conversion(original, new_content, page_name)
    
    if not valid:
        print("\n❌ 转换验证失败，不会保存")
        return False
    
    if show_diff:
        print("\n📝 修改预览:")
        lines_orig = original.split('\n')
        lines_new = new_content.split('\n')
        for i, (orig, new) in enumerate(zip(lines_orig[:30], lines_new[:30])):
            if orig != new:
                print(f"  行 {i}:")
                print(f"    原: {orig[:80]}")
                print(f"    新: {new[:80]}")
    
    if dry_run:
        print("\n🔍 预览模式 - 不会保存更改")
        return True
    
    try:
        bot.edit_page(page, new_content, summary="转换为简体中文")
        print(f"✅ 页面已保存")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False

def convert_multiple_pages(page_names, bot, dry_run=False):
    """批量转换多个页面"""
    print(f"=== 批量转换 ===")
    print(f"共 {len(page_names)} 个页面\n")
    
    converted = 0
    failed = 0
    skipped = 0
    
    for i, page_name in enumerate(page_names, 1):
        print(f"\n[{i}/{len(page_names)}] {page_name}")
        
        try:
            page = bot.get_page(page_name)
            if not page.exists:
                print("  ⚠️  页面不存在，跳过")
                skipped += 1
                continue
            
            original = page.text()
            new_content = convert_page(original, bot)
            
            if original == new_content:
                print("  - 无需修改")
                skipped += 1
                continue
            
            # 验证转换
            valid = verify_conversion(original, new_content, page_name)
            
            if not valid:
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
                
                if i < len(page_names):
                    time.sleep(1)
                    
        except Exception as e:
            print(f"  ⚠️  失败: {e}")
            failed += 1
            
            if 'ratelimited' in str(e).lower():
                print("  ⏳ 遇到速率限制，等待 60 秒...")
                time.sleep(60)
    
    print(f"\n{'📊 预览' if dry_run else '✅ 完成'}统计:")
    print(f"  - 总页面数: {len(page_names)}")
    print(f"  - {'将修改' if dry_run else '已修改'}: {converted}")
    print(f"  - 跳过: {skipped}")
    print(f"  - 失败: {failed}")
    
    return failed == 0

def convert_from_file(file_path, bot, dry_run=False):
    """从文件读取页面列表并转换"""
    print(f"=== 从文件转换 ===")
    print(f"文件: {file_path}\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            page_names = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False
    
    return convert_multiple_pages(page_names, bot, dry_run)

def main():
    parser = argparse.ArgumentParser(
        description='Fandom Wiki 通用转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个页面
  %(prog)s "西片"
  
  # 预览单个页面的修改
  %(prog)s "西片" --dry-run
  
  # 显示修改详情
  %(prog)s "西片" --show-diff
  
  # 转换多个页面
  %(prog)s "西片" "真野" "月本早苗"
  
  # 从文件读取页面列表
  %(prog)s --from-file pages.txt
  
  # 预览批量转换
  %(prog)s "西片" "真野" --dry-run

页面列表文件格式 (pages.txt):
  西片
  真野
  月本早苗
  # 以 # 开头的行会被忽略
        """
    )
    
    parser.add_argument('pages', nargs='*', help='要转换的页面名称')
    parser.add_argument('--from-file', metavar='FILE', help='从文件读取页面列表')
    parser.add_argument('--dry-run', action='store_true', help='预览模式：显示将要修改但不保存')
    parser.add_argument('--show-diff', action='store_true', help='显示修改详情')
    
    args = parser.parse_args()
    
    if not args.pages and not args.from_file:
        parser.print_help()
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    if args.from_file:
        success = convert_from_file(args.from_file, bot, args.dry_run)
    elif len(args.pages) == 1:
        success = convert_single_page(args.pages[0], bot, args.dry_run, args.show_diff)
    else:
        success = convert_multiple_pages(args.pages, bot, args.dry_run)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
