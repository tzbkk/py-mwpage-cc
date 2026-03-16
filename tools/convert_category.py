#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    category_name = sys.argv[1] if len(sys.argv) > 1 else "音樂"
    
    bot = FandomBot()
    
    print(f"获取 Category:{category_name} 的页面...")
    pages = bot.get_category_members(category_name)
    print(f"找到 {len(pages)} 个页面")
    
    for i, page in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] {page.name}")
        new_name = bot.cc.convert(page.name)
        
        original = page.text()
        new_content = bot.convert_text(original)
        
        if original != new_content:
            bot.edit_page(page, new_content, summary="转换为简体中文")
            print(f"  内容已转换")
        
        if page.name != new_name:
            print(f"  需要移动: {page.name} → {new_name}")
            bot.move_page(page, new_name, reason="改名为简体中文")
            print(f"  已移动")
        else:
            print(f"  名称无需移动")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
