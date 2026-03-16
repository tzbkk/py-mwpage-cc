#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot


def main():
    template_name = sys.argv[1] if len(sys.argv) > 1 else "Template:音樂信息"
    
    bot = FandomBot()
    
    print(f"转换模板: {template_name}")
    template = bot.get_page(template_name)
    original = template.text()
    new_content = bot.convert_text(original)
    bot.edit_page(template, new_content, summary="转换为简体中文")
    print("模板内容已转换")
    
    print(f"\n获取引用 {template_name} 的页面...")
    pages = bot.get_template_embedded_pages(template_name)
    print(f"找到 {len(pages)} 个页面")
    
    for i, page in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {page.name}")
        original = page.text()
        new_content = bot.convert_text(original)
        
        if original != new_content:
            bot.edit_page(page, new_content, summary="转换为简体中文")
            print(f"  内容已转换")
        else:
            print(f"  无需修改")
    
    new_template_name = bot.cc.convert(template_name)
    if template_name != new_template_name:
        print(f"\n移动模板: {template_name} → {new_template_name}")
        bot.move_page(template, new_template_name, reason="改名为简体中文")
        print("模板已移动")
    
    print("\n全部完成!")


if __name__ == "__main__":
    main()
