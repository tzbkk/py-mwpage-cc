#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    replacements = [
        ("片頭曲", "片头曲"),
        ("片尾曲", "片尾曲"),
    ]
    
    if len(sys.argv) > 1:
        categories = sys.argv[1:]
    else:
        categories = ["片頭曲", "片尾曲"]
    
    bot = FandomBot()
    
    for cat_name in categories:
        print(f"\n更新引用 Category:{cat_name} 的页面...")
        pages = bot.get_category_members(cat_name)
        print(f"  找到 {len(pages)} 个页面")
        
        for page in pages:
            content = page.text()
            new_content = content
            
            for old, new in replacements:
                pattern = f'\\[\\[Category:{old}\\]\\]'
                replacement = f'[[Category:{new}]]'
                new_content = bot.replace_in_page(page, pattern, replacement, summary="更新分类名称为简体中文")
                if new_content:
                    print(f"  已更新: {page.name}")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
