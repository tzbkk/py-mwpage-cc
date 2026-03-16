import mwclient
from opencc import OpenCC
import re

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

print("获取 Category:音樂 的所有页面...")
cat = site.categories["音樂"]
pages = list(cat.members())
print(f"找到 {len(pages)} 个页面")

for i, page in enumerate(pages, 1):
    print(f"[{i}/{len(pages)}] {page.name}")
    content = page.text()
    new_content = re.sub(r'\[\[Category:音樂\]\]', '[[Category:音乐]]', content)
    
    if content != new_content:
        page.edit(new_content, summary="将Category:音樂改为Category:音乐")
        print(f"  已更新")
    else:
        print(f"  无需修改")

print("\n全部完成!")
