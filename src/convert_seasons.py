#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot, verify_filenames_preserved


def main():
    pages = sys.argv[1:] if len(sys.argv) > 1 else ['动画第一季', '动画第二季', '动画第三季']
    
    bot = FandomBot()
    
    for page_name in pages:
        print(f"\n处理 {page_name}...")
        page = bot.get_page(page_name)
        original = page.text()
        new_content = bot.convert_text(original)
        
        if original != new_content:
            valid, errors = verify_filenames_preserved(original, new_content)
            if not valid:
                print(f"  文件名验证失败，跳过:")
                for err in errors:
                    print(f"    {err}")
                continue
            bot.edit_page(page, new_content, summary="转换为简体中文")
            print(f"  内容已转换")
        else:
            print(f"  无需转换")
    
    print("\n查找子页面...")
    for prefix in pages:
        subpages = bot.get_subpages(prefix)
        for page in subpages:
            print(f"\n  {page.name}")
            original = page.text()
            new_content = bot.convert_text(original)
            if original != new_content:
                valid, errors = verify_filenames_preserved(original, new_content)
                if not valid:
                    print(f"    文件名验证失败，跳过:")
                    for err in errors:
                        print(f"      {err}")
                    continue
                new_name = bot.cc.convert(page.name)
                bot.edit_page(page, new_content, summary="转换为简体中文")
                print(f"    内容已转换")
                if page.name != new_name:
                    bot.move_page(page, new_name, reason="改名为简体中文")
                    print(f"    已移动到 {new_name}")
            else:
                print(f"    无需转换")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
