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
- [fandom_bot.py](./src/FandomBot.md) - 基础机器人类库
- [batch_processor.py](./src/batch_processor.md) - 批处理工具模块

### 统一入口
- [fandom.py](./src/fandom.py) - 统一的命令行工具（推荐）

### 转换工具
- [convert_template.py](./src/convert_template.md) - 转换使用模板的页面
- [convert_category.py](./src/convert_category.md) - 转换分类下的所有页面
- [convert_page.py](./src/convert_page.py) - 转换单个或多个页面

### 季度/分类页面工具
- [convert_seasons.py](./src/convert_seasons.md) - 转换季度页面及其子页面
- [convert_cat_ending.py](./src/convert_cat_ending.md) - 批量转换分类页面并改名
- [convert_cat_page.py](./src/convert_cat_page.md) - 批量转换分类页面

### 引用更新工具
- [update_cat_refs.py](./src/update_cat_refs.md) - 更新分类引用为简体中文
- [fix_links.py](./src/fix_links.py) - 批量修复链接

### 辅助工具
- [move_pages.py](./src/move_pages.md) - 批量移动/重命名页面
- [restore_from_history.py](./src/restore_from_history.md) - 从历史版本恢复页面
- [search_and_convert.py](./src/search_and_convert.py) - 搜索并转换页面
- [get_template_info.py](./src/get_template_info.md) - 获取模板信息
- [test_fandom.py](./src/test_fandom.md) - 测试连接和登录

## 快速开始

### 1. 测试连接

```bash
python src/test_fandom.py "STARS"
```

### 2. 转换单个页面

```bash
# 使用统一入口
python src/fandom.py page "西片" --dry-run

# 或直接使用脚本
python src/convert_page.py "西片" --dry-run
```

### 3. 转换分类下的页面

```bash
# 列出页面
python src/fandom.py category "音乐" --list

# 预览转换
python src/fandom.py category "音乐" --dry-run --limit 5

# 实际转换
python src/fandom.py category "音乐"
```

### 4. 转换使用模板的页面

```bash
# 列出页面
python src/fandom.py template "Template:角色信息" --list

# 测试单个页面
python src/fandom.py template "Template:角色信息" --test "西片"

# 批量转换
python src/fandom.py template "Template:角色信息" --batch
```

## 通用功能

大多数工具都支持以下功能：

### 从文件读取

```bash
python src/move_pages.py --from-file pages.txt
```

文件格式（以 # 开头的行会被忽略）：
```
页面1
页面2
# 这是注释
页面3
```

### 预览模式

```bash
python src/convert_page.py "页面名" --dry-run
```

### 统计信息

所有批处理工具都会显示：
- 总页面数
- 已处理/将修改数量
- 跳过数量
- 失败数量

## 注意事项

**重要：[禁止删除页面](./NOTES.md)**

- 所有脚本禁止删除 Wiki 页面，最多只能移动/重命名
- 所有工具都会自动跳过图片字段（图片、圖片）
- 移动页面时默认不创建重定向
- 建议先使用 --dry-run 预览
- 建议先在小范围测试后再大规模使用

## 目录结构

```
py-mwpage-cc/
├── .env                 # 环境变量配置（私有）
├── .env.example         # 环境变量配置示例
├── config.json.example  # JSON配置示例
├── requirements.txt     # Python依赖
├── fandom_bot.py        # 核心库
├── AGENTS.md           # AI助手指南
├── src/               # 工具脚本
│   ├── batch_processor.py  # 批处理模块
│   ├── fandom.py          # 统一入口（推荐）
│   ├── convert_page.py    # 页面转换
│   ├── convert_category.py # 分类转换
│   ├── convert_template.py # 模板转换
│   └── ...
└── doc/                 # 文档目录
    ├── README.md
    ├── QUICKSTART.md
    ├── CONFIGURATION.md
    ├── REFACTORING.md
    └── tools/            # 工具文档
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
- [fandom_bot.py](./src/FandomBot.md) - 基础机器人类库

### 转换工具
- [batch_convert.py](./src/batch_convert.md) - 批量转换使用模板的页面
- [convert_template.py](./src/convert_template.md) - 转换模板及其引用页面
- [convert_category.py](./src/convert_category.md) - 转换分类下的所有页面
- [convert_seasons.py](./src/convert_seasons.md) - 转换季度页面及其子页面
- [convert_stars.py](./src/convert_stars.md) - 转换单个页面（保留图片）

### 分类工具
- [convert_cat_ending.py](./src/convert_cat_ending.md) - 转换分类页面
- [convert_cat_page.py](./src/convert_cat_page.md) - 转换单个分类页面
- [fix_category.py](./src/fix_category.md) - 批量替换分类标签
- [update_cat_refs.py](./src/update_cat_refs.md) - 更新分类引用

### 辅助工具
- [move_pages.py](./src/move_pages.md) - 批量移动/重命名页面
- [get_template_info.py](./src/get_template_info.md) - 获取模板信息
- [test_fandom.py](./src/test_fandom.md) - 测试连接和登录

## 快速开始

1. 测试连接：
```bash
python src/test_fandom.py
```

2. 转换模板及其引用的页面：
```bash
python src/convert_template.py "Template:音樂信息"
```

3. 转换分类下的所有页面：
```bash
python src/convert_category.py "音樂"
```

## 注意事项

**重要：[禁止删除页面](./NOTES.md)**

- 所有脚本禁止删除 Wiki 页面，最多只能移动/重命名
- 所有工具都会自动跳过图片字段（图片、圖片）
- 移动页面时默认不创建重定向
- 建议先在小范围测试后再大规模使用

**重要：禁止修改脚本**

- 转换页面时，脚本只修改 Wiki 页面内容
- **脚本不会也不会修改任何脚本文件或代码文件**
- 如需修改脚本，请使用代码编辑器手动编辑
- 详见 [注意事项](./NOTES.md)

## 目录结构

```
famdom-editor/
├── .env                 # 环境变量配置（私有）
├── .env.example         # 环境变量配置示例
├── config.json.example  # JSON配置示例
├── requirements.txt     # Python依赖
├── fandom_bot.py        # 核心库
├── src/               # 工具脚本
│   ├── batch_convert.py
│   ├── convert_template.py
│   └── ...
└── doc/                 # 文档目录
    ├── README.md
    ├── QUICKSTART.md
    └── src/
```
