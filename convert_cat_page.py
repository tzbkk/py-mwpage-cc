import mwclient
from opencc import OpenCC
import re

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

page = site.pages["Category:音乐"]
original = page.text()

new_content = cc.convert(original)

page.edit(new_content, summary="转换为简体中文")
print("Category:音乐 内容已转换为简体中文")
