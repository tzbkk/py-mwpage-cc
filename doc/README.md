# Fandom Wiki 自动化工具集

## 概述

本工具集用于自动化操作 Fandom Wiki，主要功能包括：
- 繁体中文转简体中文
- 批量页面转换
- 模板和分类处理
- 页面移动和重命名

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或手动安装
pip install mwclient opencc python-dotenv

# 激活虚拟环境（如果使用）
source venv/bin/activate
```

## 配置

### 方式1：使用 .env 文件（推荐）

1. 复制示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件：
```bash
# Wiki 站点配置
FANDOM_DOMAIN=your-wiki.fandom.com
FANDOM_PATH=/zh/

# 机器人账号（在 Special:BotPasswords 创建）
FANDOM_USERNAME=YourBot@BotName
FANDOM_PASSWORD=your_bot_password

# 转换模式（t2s=繁体转简体，s2t=简体转繁体）
CONVERSION_MODE=t2s
```

### 方式2：使用 config.json 文件

1. 复制示例文件：
```bash
cp config.json.example config.json
```

2. 编辑 `config.json` 文件，根据注释说明填入你的配置。

### 获取机器人密码

1. 登录你的 Fandom Wiki
2. 访问 `Special:BotPasswords`
3. 创建一个新的机器人密码
4. 记下用户名（格式：YourName@BotName）和密码

## 工具列表

### 核心库
- [fandom_bot.py](./tools/FandomBot.md) - 基础机器人类库

### 转换工具
- [batch_convert.py](./tools/batch_convert.md) - 批量转换使用模板的页面
- [convert_template.py](./tools/convert_template.md) - 转换模板及其引用页面
- [convert_category.py](./tools/convert_category.md) - 转换分类下的所有页面
- [convert_seasons.py](./tools/convert_seasons.md) - 转换季度页面及其子页面
- [convert_stars.py](./tools/convert_stars.md) - 转换单个页面（保留图片）

### 分类工具
- [convert_cat_ending.py](./tools/convert_cat_ending.md) - 转换分类页面
- [convert_cat_page.py](./tools/convert_cat_page.md) - 转换单个分类页面
- [fix_category.py](./tools/fix_category.md) - 批量替换分类标签
- [update_cat_refs.py](./tools/update_cat_refs.md) - 更新分类引用

### 辅助工具
- [move_pages.py](./tools/move_pages.md) - 批量移动/重命名页面
- [get_template_info.py](./tools/get_template_info.md) - 获取模板信息
- [test_fandom.py](./tools/test_fandom.md) - 测试连接和登录

## 快速开始

1. 测试连接：
```bash
python tools/test_fandom.py
```

2. 转换模板及其引用的页面：
```bash
python tools/convert_template.py "Template:音樂信息"
```

3. 转换分类下的所有页面：
```bash
python tools/convert_category.py "音樂"
```

## 注意事项

- 所有工具都会自动跳过图片字段（图片、圖片）
- 移动页面时默认不创建重定向
- 建议先在小范围测试后再大规模使用

## 目录结构

```
famdom-editor/
├── .env                 # 环境变量配置（私有）
├── .env.example         # 环境变量配置示例
├── config.json.example  # JSON配置示例
├── requirements.txt     # Python依赖
├── fandom_bot.py        # 核心库
├── tools/               # 工具脚本
│   ├── batch_convert.py
│   ├── convert_template.py
│   └── ...
└── doc/                 # 文档目录
    ├── README.md
    ├── QUICKSTART.md
    └── tools/
```
