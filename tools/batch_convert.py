#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    if len(sys.argv) < 2:
        print("用法: python batch_convert.py <template_name>")
        print("示例: python batch_convert.py 'Template:音樂信息'")
        sys.exit(1)
    
    template_name = sys.argv[1]
    
    bot = FandomBot()
    
    print(f"获取引用 {template_name} 的页面...")
    pages = bot.get_template_embedded_pages(template_name)
    print(f"找到 {len(pages)} 个页面")
    
    for i, page in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] 处理: {page.name}")
        original = page.text()
        new_content = bot.convert_text(original)
        
        if original != new_content:
            bot.edit_page(page, new_content, summary="转换为简体中文")
            print(f"  已保存")
        else:
            print(f"  无需修改")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
