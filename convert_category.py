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

print("检查 Category:音樂...")
cat = site.categories["音樂"]
pages = list(cat.members())
print(f"找到 {len(pages)} 个页面")

for i, page in enumerate(pages, 1):
    print(f"\n[{i}/{len(pages)}] {page.name}")
    new_name = cc.convert(page.name)
    
    original = page.text()
    new_content = convert_page(original)
    
    if original != new_content:
        page.edit(new_content, summary="转换为简体中文")
        print(f"  内容已转换")
    
    if page.name != new_name:
        print(f"  需要移动: {page.name} → {new_name}")
        page.move(new_name, reason="改名为简体中文", no_redirect=True)
        print(f"  已移动")
    else:
        print(f"  名称无需移动")

print("\n全部完成!")
