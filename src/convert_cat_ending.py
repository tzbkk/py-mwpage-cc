#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved


def main():
    categories = sys.argv[1:] if len(sys.argv) > 1 else ["片頭曲", "片尾曲"]
    
    bot = FandomBot()
    
    for cat_name in categories:
        print(f"\n处理 Category:{cat_name}")
        new_name = bot.cc.convert(cat_name)
        print(f"  目标名称: {new_name}")
        
        cat = bot.get_page(f"Category:{cat_name}")
        if cat.exists:
            content = cat.text()
            new_content = bot.convert_text(content)
            
            if content != new_content:
                valid, errors = verify_filenames_preserved(content, new_content)
                if not valid:
                    print(f"  文件名验证失败:")
                    for err in errors:
                        print(f"    {err}")
                    continue
                bot.edit_page(cat, new_content, summary="转换为简体中文")
                print(f"  内容已转换")
            else:
                print(f"  内容无需转换")
            
            if cat_name != new_name:
                bot.move_page(cat, f"Category:{new_name}", reason="改名为简体中文")
                print(f"  页面已移动")
        else:
            print(f"  页面不存在")
    
    print("\n完成!")


if __name__ == "__main__":
    main()
