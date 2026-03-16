#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    pages = sys.argv[1:] if len(sys.argv) > 1 else [
        "雖然不會說出口。",
        "愛歌",
        "小小戀歌",
        "心血來潮的浪漫",
        "零釐米",
        "奏",
        "粉雪",
        "奇迹",
        "感谢",
        "STARS",
        "献给你",
        "你和光",
        "溫柔的心情",
        "上午11點",
        "自行車",
        "起風之戀",
        "彷如相逢時",
    ]
    
    bot = FandomBot()
    
    for page_name in pages:
        new_name = bot.cc.convert(page_name)
        if page_name != new_name:
            print(f"移动: {page_name} → {new_name}")
            page = bot.get_page(page_name)
            if page.exists:
                bot.move_page(page, new_name, reason="改名为简体中文")
                print(f"  完成")
            else:
                print(f"  页面不存在（可能已移动）")
        else:
            print(f"无需移动: {page_name}")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
