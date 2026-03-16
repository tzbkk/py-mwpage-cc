import mwclient

site = mwclient.Site("karakai-jouzu-no-takagi-san.fandom.com", path="/zh/")

site.login("Lunisha Kumina@lunishabot", "1q0n36m4hc6dohp0k90krm8nhpa0jb5p")

print(f"登录成功! 用户: {site.username}")

page = site.pages["STARS"]
print(f"\n页面标题: {page.name}")
print(f"是否存在: {page.exists}")
print(f"\n页面内容:\n{page.text()}")
