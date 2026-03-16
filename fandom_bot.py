import mwclient
from opencc import OpenCC
import json
import re
import os
from typing import List, Optional, Callable

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


class FandomBot:
    def __init__(self, config_file: str = "config.json"):
        if HAS_DOTENV and os.path.exists('.env'):
            load_dotenv()
            self.config = self._load_from_env()
        elif os.path.exists(config_file):
            self.config = self._load_from_json(config_file)
        else:
            raise FileNotFoundError(
                "未找到配置文件！\n"
                "请创建 .env 文件或 config.json 文件。\n"
                "参考 config.json.example 示例。"
            )
        
        self.site = mwclient.Site(
            self.config['site']['domain'],
            path=self.config['site']['path']
        )
        self.site.login(
            self.config['auth']['username'],
            self.config['auth']['password']
        )
        
        self.cc = OpenCC(self.config['conversion']['mode'])
        self.skip_fields = self.config['conversion']['skip_fields']
    
    def _load_from_env(self) -> dict:
        return {
            'site': {
                'domain': os.getenv('FANDOM_DOMAIN'),
                'path': os.getenv('FANDOM_PATH', '/zh/')
            },
            'auth': {
                'username': os.getenv('FANDOM_USERNAME'),
                'password': os.getenv('FANDOM_PASSWORD')
            },
            'conversion': {
                'mode': os.getenv('CONVERSION_MODE', 't2s'),
                'skip_fields': ['图片', '圖片']
            }
        }
    
    def _load_from_json(self, config_file: str) -> dict:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config = {k: v for k, v in config.items() if not k.startswith('_')}
        
        for section in config.values():
            if isinstance(section, dict):
                keys_to_remove = [k for k in section.keys() if k.startswith('_')]
                for k in keys_to_remove:
                    del section[k]
        
        return config
    
    def convert_text(self, text: str, skip_images: bool = True) -> str:
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if line.startswith('|') and '=' in line:
                parts = line.split('=', 1)
                var_name = parts[0]
                value = parts[1] if len(parts) > 1 else ''
                
                if skip_images and any(field in var_name for field in self.skip_fields):
                    result.append(var_name + '=' + value)
                else:
                    result.append(self.cc.convert(var_name) + '=' + self.cc.convert(value))
            elif line.startswith('{{'):
                result.append(self.cc.convert(line))
            else:
                result.append(self.cc.convert(line))
        
        return '\n'.join(result)
    
    def get_page(self, page_name: str):
        return self.site.pages[page_name]
    
    def get_category_members(self, category_name: str) -> List:
        cat = self.site.categories[category_name]
        return list(cat.members())
    
    def get_template_embedded_pages(self, template_name: str) -> List:
        return list(self.site.pages[template_name].embeddedin())
    
    def edit_page(self, page, content: str, summary: str = "自动编辑"):
        page.edit(content, summary=summary)
    
    def move_page(self, page, new_name: str, reason: str = "页面移动", no_redirect: bool = True):
        page.move(new_name, reason=reason, no_redirect=no_redirect)
    
    def replace_in_page(self, page, pattern: str, replacement: str, summary: str = "文本替换"):
        content = page.text()
        new_content = re.sub(pattern, replacement, content)
        
        if content != new_content:
            page.edit(new_content, summary=summary)
            return True
        return False
    
    def batch_process_pages(self, pages: List, processor: Callable, show_progress: bool = True):
        total = len(pages)
        for i, page in enumerate(pages, 1):
            if show_progress:
                print(f"[{i}/{total}] 处理: {page.name}")
            processor(page)
    
    def get_subpages(self, prefix: str) -> List:
        return list(self.site.allpages(prefix=prefix + '/'))
