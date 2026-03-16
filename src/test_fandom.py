#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    page_name = sys.argv[1] if len(sys.argv) > 1 else "STARS"
    
    bot = FandomBot()
    
    print(f"登录成功! 用户: {bot.site.username}")
    
    page = bot.get_page(page_name)
    print(f"\n页面标题: {page.name}")
    print(f"是否存在: {page.exists}")
    print(f"\n页面内容:\n{page.text()}")


if __name__ == "__main__":
    main()
