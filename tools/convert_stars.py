#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    page_name = sys.argv[1] if len(sys.argv) > 1 else "STARS"
    
    bot = FandomBot()
    
    page = bot.get_page(page_name)
    original = page.text()
    
    new_content = bot.convert_text(original, skip_images=True)
    
    bot.edit_page(page, new_content, summary="转换为简体中文")
    print("保存成功!")


if __name__ == "__main__":
    main()
