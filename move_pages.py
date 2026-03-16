import mwclient
from opencc import OpenCC

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

pages_to_check = [
    "雖然不會說出口。",
    "愛歌",
    "小小戀歌",
    "心血來潮的浪漫",
    "零釐米",
    "奏",
    "粉雪",
    "奇迹",
    "感谢",
    "STARS",
    "献给你",
    "你和光",
    "溫柔的心情",
    "上午11點",
    "自行車",
    "起風之戀",
    "彷如相逢時",
]

for page_name in pages_to_check:
    new_name = cc.convert(page_name)
    if page_name != new_name:
        print(f"移动: {page_name} → {new_name}")
        page = site.pages[page_name]
        if page.exists:
            page.move(new_name, reason="改名为简体中文", no_redirect=True)
            print(f"  完成")
        else:
            print(f"  页面不存在（可能已移动）")
    else:
        print(f"无需移动: {page_name}")

print("\n全部完成!")
