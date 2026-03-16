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
                result.append(var_name + '=' + value)
            else:
                result.append(cc.convert(var_name) + '=' + cc.convert(value))
        elif line.startswith('{{'):
            result.append(line)
        else:
            result.append(cc.convert(line))
    
    return '\n'.join(result)

template_page = site.pages["Template:音樂信息"]
print("跳过模板页面（已转换）")

print("\n获取引用该模板的页面...")
pages = list(site.pages["Template:音樂信息"].embeddedin())
print(f"找到 {len(pages)} 个页面")

for i, page in enumerate(pages, 1):
    print(f"\n[{i}/{len(pages)}] 处理: {page.name}")
    original = page.text()
    new_content = convert_page(original)
    
    if original != new_content:
        page.edit(new_content, summary="转换为简体中文")
        print(f"  已保存")
    else:
        print(f"  无需修改")

print("\n全部完成!")
