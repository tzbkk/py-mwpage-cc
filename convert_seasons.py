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

pages = ['动画第一季', '动画第二季', '动画第三季']

for page_name in pages:
    print(f"\n处理 {page_name}...")
    page = site.pages[page_name]
    original = page.text()
    new_content = convert_page(original)
    page.edit(new_content, summary="转换为简体中文")
    print(f"  内容已转换")

print("\n查找剧集列表子页面...")
for prefix in ['动画第一季', '动画第二季', '动画第三季']:
    for page in site.allpages(prefix=prefix + '/'):
        print(f"\n  {page.name}")
        original = page.text()
        new_content = convert_page(original)
        if original != new_content:
            new_name = cc.convert(page.name)
            page.edit(new_content, summary="转换为简体中文")
            print(f"    内容已转换")
            if page.name != new_name:
                page.move(new_name, reason="改名为简体中文", no_redirect=True)
                print(f"    已移动到 {new_name}")

print("\n全部完成!")
