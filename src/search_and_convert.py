#!/usr/bin/env python3
"""
搜索页面，转换内容为简体并移动（如果名称改变）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved
import argparse


def search_pages(bot: FandomBot, keyword: str, filter_pattern: str = None):
    """搜索包含关键词的页面"""
    print(f"正在搜索: {keyword}")
    
    pages = []
    
    for result in bot.site.search(keyword, namespace=0):
        page_name = result.get('title', '')
        if filter_pattern:
            if filter_pattern in page_name:
                pages.append(page_name)
                print(f"  找到: {page_name}")
        else:
            pages.append(page_name)
            print(f"  找到: {page_name}")
    
    print(f"\n共找到 {len(pages)} 个页面")
    return pages


def process_pages(bot: FandomBot, pages: list, dry_run: bool = False, convert_only: bool = False, move_only: bool = False):
    """处理页面：转换内容 + 移动页面"""
    
    for i, page_name in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] 处理: {page_name}")
        
        page = bot.get_page(page_name)
        if not page.exists:
            print(f"  页面不存在，跳过")
            continue
        
        new_name = bot.cc.convert(page_name)
        needs_move = page_name != new_name
        
        # 转换内容
        if not move_only:
            if dry_run:
                print(f"  [预览] 将转换页面内容为简体中文")
            else:
                content = page.text()
                new_content = bot.convert_text(content)
                if content != new_content:
                    valid, errors = verify_filenames_preserved(content, new_content)
                    if not valid:
                        print(f"  文件名验证失败，跳过:")
                        for err in errors:
                            print(f"    {err}")
                        continue
                    bot.edit_page(page, new_content, summary="转换为简体中文")
                    print(f"  已转换内容")
                else:
                    print(f"  内容无需转换")
        
        # 移动页面
        if not convert_only and needs_move:
            if dry_run:
                print(f"  [预览] 将移动: {page_name} → {new_name}")
            else:
                try:
                    bot.move_page(page, new_name, reason="改名为简体中文")
                    print(f"  已移动: {page_name} → {new_name}")
                except Exception as e:
                    print(f"  移动失败: {e}")


def main():
    parser = argparse.ArgumentParser(description='搜索页面并转换/移动')
    parser.add_argument('keyword', nargs='?', help='搜索关键词')
    parser.add_argument('--filter', '-f', help='额外过滤模式（只保留包含此字符串的页面）')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际执行')
    parser.add_argument('--list', action='store_true', help='只列出页面，不处理')
    parser.add_argument('--convert-only', action='store_true', help='只转换内容，不移动页面')
    parser.add_argument('--move-only', action='store_true', help='只移动页面，不转换内容')
    parser.add_argument('--pages', nargs='+', help='直接指定页面列表（跳过搜索）')
    
    args = parser.parse_args()
    
    bot = FandomBot()
    
    # 获取页面列表
    if args.pages:
        pages = args.pages
    elif args.keyword:
        pages = search_pages(bot, args.keyword, args.filter)
    else:
        print("错误: 请提供搜索关键词或使用 --pages 指定页面")
        parser.print_help()
        return
    
    if args.list:
        print("\n页面列表:")
        for p in pages:
            new_name = bot.cc.convert(p)
            if p != new_name:
                print(f"  {p} → {new_name}")
            else:
                print(f"  {p}")
        return
    
    if not pages:
        print("没有找到需要处理的页面")
        return
    
    # 处理页面
    process_pages(bot, pages, args.dry_run, args.convert_only, args.move_only)
    
    print("\n处理完成!")


if __name__ == '__main__':
    main()
