#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved


def main():
    page_name = sys.argv[1] if len(sys.argv) > 1 else "Category:音乐"
    
    bot = FandomBot()
    
    page = bot.get_page(page_name)
    original = page.text()
    
    new_content = bot.convert_text(original)
    
    if original != new_content:
        valid, errors = verify_filenames_preserved(original, new_content)
        if not valid:
            print(f"文件名验证失败:")
            for err in errors:
                print(f"  {err}")
            return
        bot.edit_page(page, new_content, summary="转换为简体中文")
        print(f"{page_name} 内容已转换为简体中文")
    else:
        print(f"{page_name} 无需转换")


if __name__ == "__main__":
    main()
