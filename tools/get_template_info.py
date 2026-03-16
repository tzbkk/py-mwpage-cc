#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    template_name = sys.argv[1] if len(sys.argv) > 1 else "Template:音樂信息"
    
    bot = FandomBot()
    
    template_page = bot.get_page(template_name)
    print(f"模板页面: {template_page.name}")
    print(f"是否存在: {template_page.exists}")
    print(f"\n模板内容:\n{template_page.text()}")


if __name__ == "__main__":
    main()
