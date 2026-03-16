# Fandom Wiki 自动化工具集

自动化的 Fandom Wiki 维护工具，主要用于繁体中文到简体中文的批量转换。

## 特性

- 繁体中文转简体中文
- 批量页面处理
- 模板和分类管理
- 页面移动和重命名
- 可配置的通用框架

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置
cp .env.example .env
# 编辑 .env 填入你的 Wiki 信息

# 3. 测试连接
python src/test_fandom.py

# 4. 开始使用
python src/convert_template.py "Template:音樂信息"
```

## 文档

- [快速使用指南](doc/QUICKSTART.md)
- [配置说明](doc/CONFIGURATION.md)
- [完整文档](doc/README.md)
- [工具列表](doc/README.md#工具列表)

## 目录结构

```
.
├── .env                 # 环境变量配置（私有）
├── .env.example         # 配置示例
├── config.json.example  # JSON配置示例
├── requirements.txt     # Python依赖
├── fandom_bot.py        # 核心库
├── src/               # 工具脚本
│   ├── batch_convert.py
│   ├── convert_template.py
│   ├── convert_category.py
│   └── ...
└── doc/                 # 文档
    ├── README.md
    ├── QUICKSTART.md
    └── src/
```

## 工具分类

### 核心库
- `fandom_bot.py` - 基础机器人类库

### 转换工具
- `batch_convert.py` - 批量转换使用模板的页面
- `convert_template.py` - 转换模板及其引用页面
- `convert_category.py` - 转换分类下的所有页面
- `convert_seasons.py` - 转换季度页面及其子页面
- `convert_stars.py` - 转换单个页面

### 分类工具
- `convert_cat_ending.py` - 转换分类页面
- `convert_cat_page.py` - 转换单个分类页面
- `fix_category.py` - 批量替换分类标签
- `update_cat_refs.py` - 更新分类引用

### 辅助工具
- `move_pages.py` - 批量移动/重命名页面
- `get_template_info.py` - 获取模板信息
- `test_fandom.py` - 测试连接和登录

## 配置

### 使用 .env 文件（推荐）

```bash
cp .env.example .env
```

编辑 `.env`:

```bash
FANDOM_DOMAIN=your-wiki.fandom.com
FANDOM_PATH=/zh/
FANDOM_USERNAME=YourBot@BotName
FANDOM_PASSWORD=your_bot_password
CONVERSION_MODE=t2s
```

### 使用 config.json 文件

```bash
cp config.json.example config.json
# 编辑 config.json
```

## 依赖

- Python 3.6+
- mwclient
- opencc
- python-dotenv（可选，用于读取 .env 文件）

## 许可证

MIT License
