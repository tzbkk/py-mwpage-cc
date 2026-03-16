import mwclient
import re

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

replacements = [
    (r'\[\[Category:片頭曲\]\]', '[[Category:片头曲]]'),
    (r'\[\[Category:片尾曲\]\]', '[[Category:片尾曲]]'),
]

categories = ["片頭曲", "片尾曲"]

for cat_name in categories:
    print(f"\n更新引用 Category:{cat_name} 的页面...")
    cat = site.categories[cat_name]
    pages = list(cat.members())
    print(f"  找到 {len(pages)} 个页面")
    
    for page in pages:
        content = page.text()
        new_content = content
        new_content = re.sub(r'\[\[Category:片頭曲\]\]', '[[Category:片头曲]]', new_content)
        
        if content != new_content:
            page.edit(new_content, summary="更新分类名称为简体中文")
            print(f"  已更新: {page.name}")

print("\n完成!")
