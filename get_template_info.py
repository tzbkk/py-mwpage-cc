import mwclient
from opencc import OpenCC

cc = OpenCC('t2s')

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")
site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

template_page = site.pages["Template:音樂信息"]
print(f"模板页面: {template_page.name}")
print(f"是否存在: {template_page.exists}")
print(f"\n模板内容:\n{template_page.text()}")
