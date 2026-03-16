#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    old_cat = sys.argv[1] if len(sys.argv) > 1 else "音樂"
    new_cat = sys.argv[2] if len(sys.argv) > 2 else "音乐"
    
    bot = FandomBot()
    
    print(f"获取 Category:{old_cat} 的所有页面...")
    pages = bot.get_category_members(old_cat)
    print(f"找到 {len(pages)} 个页面")
    
    pattern = f'\\[\\[Category:{old_cat}\\]\\]'
    replacement = f'[[Category:{new_cat}]]'
    
    for i, page in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page.name}")
        if bot.replace_in_page(page, pattern, replacement, summary=f"将Category:{old_cat}改为Category:{new_cat}"):
            print(f"  已更新")
        else:
            print(f"  无需修改")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
