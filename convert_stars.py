import mwclient
from opencc import OpenCC

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

page = site.pages["STARS"]
original = page.text()

lines = original.split('\n')
result = []

for line in lines:
    if line.startswith('|') and '=' in line:
        parts = line.split('=', 1)
        var_name = parts[0]
        value = parts[1] if len(parts) > 1 else ''
        
        if '圖片' in var_name or '图片' in var_name:
            result.append(line)
        else:
            result.append(var_name + '=' + cc.convert(value))
    elif line.startswith('{{'):
        result.append(line)
    else:
        result.append(cc.convert(line))

new_content = '\n'.join(result)

page.edit(new_content, summary="转换为简体中文")

print("保存成功!")
