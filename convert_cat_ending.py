import mwclient
from opencc import OpenCC

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

categories = ["片頭曲", "片尾曲"]

for cat_name in categories:
    print(f"\n处理 Category:{cat_name}")
    new_name = cc.convert(cat_name)
    print(f"  目标名称: {new_name}")
    
    cat = site.pages[f"Category:{cat_name}"]
    if cat.exists:
        content = cat.text()
        new_content = cc.convert(content)
        
        cat.edit(new_content, summary="转换为简体中文")
        print(f"  内容已转换")
        
        if cat_name != new_name:
            cat.move(f"Category:{new_name}", reason="改名为简体中文", no_redirect=True)
            print(f"  页面已移动")
    else:
        print(f"  页面不存在")

print("\n完成!")
