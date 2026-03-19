import mwclient
from opencc import OpenCC
import json
import re
import os
from typing import List, Optional, Callable, Tuple, Dict

try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


FILE_EXTENSIONS = r'(?:jpg|jpeg|png|gif|svg|webp|bmp|ico|tiff?|pdf|ogg|mp3|mp4|webm|ogv)'


def protect_filenames(text: str) -> Tuple[str, Dict[str, str]]:
    """保护所有文件名不被转换，支持带空格的文件名"""
    protected = {}
    counter = [0]
    
    def get_placeholder():
        placeholder = f'__PROTECTED_FILE_{counter[0]}__'
        counter[0] += 1
        return placeholder
    
    # [[File:xxx.jpg|...]] 或 [[Image:xxx.jpg|...]] - 只保护文件名部分
    def replace_wiki_file_link(match):
        placeholder = get_placeholder()
        prefix = match.group(1)
        filename = match.group(2)
        params = match.group(3) if match.lastindex >= 3 else ''
        protected[placeholder] = f'{prefix}:{filename}'
        return f'[[{placeholder}{params}]]'
    
    text = re.sub(
        rf'\[\[(File|Image|文件|檔案):([^\|\]]+?\.{FILE_EXTENSIONS})([^\]]*?)\]\]',
        replace_wiki_file_link,
        text,
        flags=re.IGNORECASE
    )
    
    # File:xxx.jpg 或 Image:xxx.jpg（不含方括号，支持带空格）
    def replace_file_prefix(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(0)
        return placeholder
    
    text = re.sub(
        rf'(File|Image|文件|檔案):[^\|\]\[\n]+?\.{FILE_EXTENSIONS}',
        replace_file_prefix,
        text,
        flags=re.IGNORECASE
    )
    
    # gallery 标签中的纯文件名（行首开始，支持带空格）
    def replace_gallery_file(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return placeholder
    
    text = re.sub(
        rf'^([^\|\]\[=\n]+?\.{FILE_EXTENSIONS})(?=\s*$|\s*\|)',
        replace_gallery_file,
        text,
        flags=re.MULTILINE | re.IGNORECASE
    )
    
    # =xxx.jpg 形式的文件名值（= 后面直接是文件名，支持带空格）
    def replace_value_file(match):
        placeholder = get_placeholder()
        protected[placeholder] = match.group(1)
        return '=' + placeholder
    
    text = re.sub(
        rf'=([^\|\]\[\n=]+?\.{FILE_EXTENSIONS})(?=\s*$|\s*[\|\]])',
        replace_value_file,
        text,
        flags=re.IGNORECASE
    )
    
    return text, protected


def restore_filenames(text: str, protected: Dict[str, str]) -> str:
    """恢复保护的文件名"""
    for placeholder, original in sorted(protected.items(), key=lambda x: len(x[0]), reverse=True):
        text = text.replace(placeholder, original)
    return text


def verify_filenames_preserved(original: str, converted: str) -> Tuple[bool, List[str]]:
    """验证文件名是否被正确保护"""
    pattern = rf'[^\s\[\]|=]*?\.{FILE_EXTENSIONS}'
    
    files_orig = set(re.findall(pattern, original, re.IGNORECASE))
    files_new = set(re.findall(pattern, converted, re.IGNORECASE))
    
    if files_orig == files_new:
        return True, []
    
    errors = []
    if files_orig - files_new:
        errors.append(f"丢失: {files_orig - files_new}")
    if files_new - files_orig:
        errors.append(f"新增: {files_new - files_orig}")
    
    return False, errors


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
        text, protected = protect_filenames(text)
        text = self.cc.convert(text)
        text = restore_filenames(text, protected)
        return text
    
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
