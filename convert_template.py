import mwclient
from opencc import OpenCC

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

def convert_page(content):
    lines = content.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('|') and '=' in line:
            parts = line.split('=', 1)
            var_name = parts[0]
            value = parts[1] if len(parts) > 1 else ''
            
            if '圖片' in var_name or '图片' in var_name:
                result.append('|图片 =' + value)
            else:
                result.append(cc.convert(var_name) + '=' + cc.convert(value))
        elif line.startswith('{{'):
            result.append(cc.convert(line))
        else:
            result.append(cc.convert(line))
    
    return '\n'.join(result)

print("1. 转换模板内容...")
old_template = site.pages["Template:音樂信息"]
original_template = old_template.text()
new_template = convert_page(original_template)
old_template.edit(new_template, summary="转换为简体中文")
print("   模板内容已转换")

print("\n2. 获取引用模板的页面...")
pages = list(site.pages["Template:音樂信息"].embeddedin())
print(f"   找到 {len(pages)} 个页面")

print("\n3. 更新页面内容（模板名和变量名改简体）...")
for i, page in enumerate(pages, 1):
    print(f"   [{i}/{len(pages)}] {page.name}")
    original = page.text()
    new_content = convert_page(original)
    page.edit(new_content, summary="转换为简体中文")

print("\n4. 移动模板页面...")
old_template = site.pages["Template:音樂信息"]
new_template_page = site.pages["Template:音乐信息"]

old_template.move("Template:音乐信息", reason="改名为简体中文", no_redirect=True)
print("   模板已移动到 Template:音乐信息，无重定向")

print("\n全部完成!")
