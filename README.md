# Fandom Wiki 自动化转换工具

自动化的 Fandom Wiki 维护工具，主要用于繁体中文到简体中文的批量转换。

## ⚠️ 重要原则

**永远先测试单个页面，再批量应用！**

使用任何工具前，必须先用 `--dry-run` 或在单个页面上测试，确认无误后再批量应用。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置

```bash
cp .env.example .env
# 编辑 .env 填入你的 Wiki 信息
```

### 3. 测试连接

```bash
python src/fandom.py page "STARS" --dry-run
```

### 4. 开始使用

```bash
# 转换单个页面（推荐第一步）
python src/fandom.py page "西片" --dry-run  # 预览
python src/fandom.py page "西片"            # 实际转换

# 检查 Wiki 上的结果，确认无误后...

# 转换分类
python src/fandom.py category "音乐" --list        # 列出页面
python src/fandom.py category "音乐" --dry-run     # 预览
python src/fandom.py category "音乐"               # 转换

# 转换模板
python src/fandom.py template "Template:角色信息" --list          # 列出页面
python src/fandom.py template "Template:角色信息" --test "西片"   # 测试
python src/fandom.py template "Template:角色信息" --batch         # 批量转换
```

## 工具集

### 统一入口（推荐）

```bash
python src/fandom.py <command> [options]
```

**命令：**
- `page` - 转换单个或多个页面
- `category` - 转换分类下的所有页面
- `template` - 转换使用模板的所有页面
- `restore` - 从历史版本恢复页面

### 独立工具

也可以直接使用独立的工具脚本：

```bash
# 页面转换
python src/convert_page.py "页面名" [选项]

# 分类转换
python src/convert_category.py "分类名" [选项]

# 模板转换
python src/convert_template.py "Template:模板名" [选项]

# 恢复页面
python src/restore_from_history.py "页面名" [选项]
```

## 常用选项

所有转换工具都支持：

- `--dry-run` - 预览模式，显示将要修改但不保存
- `--list` - 只列出页面，不转换
- `--help` - 显示帮助信息

## 功能特性

✅ **文件名保护** - 自动保护 .jpg, .png 等文件名不被修改  
✅ **智能转换** - 使用 OpenCC 进行高质量繁简转换  
✅ **变量名映射** - 自动转换模板变量名  
✅ **测试优先** - 支持先测试单个页面，再批量应用  
✅ **预览模式** - 使用 --dry-run 预览修改  
✅ **安全恢复** - 出错时可从历史版本恢复  
✅ **速率限制处理** - 自动处理 API 速率限制  
✅ **转换验证** - 自动验证文件名保护是否正确  

## 使用场景

### 场景 1：转换单个页面

```bash
# 1. 预览修改
python src/fandom.py page "西片" --dry-run

# 2. 实际转换
python src/fandom.py page "西片"
```

### 场景 2：转换多个页面

```bash
# 直接指定多个页面
python src/fandom.py page "西片" "真野" "月本早苗"

# 或从文件读取
echo -e "西片\n真野\n月本早苗" > pages.txt
python src/fandom.py page --from-file pages.txt
```

### 场景 3：转换分类下的所有页面

```bash
# 1. 列出页面
python src/fandom.py category "音乐" --list

# 2. 测试前 5 个页面
python src/fandom.py category "音乐" --limit 5

# 3. 转换所有页面
python src/fandom.py category "音乐"
```

### 场景 4：转换使用模板的所有页面

```bash
# 1. 列出使用模板的页面
python src/fandom.py template "Template:角色信息" --list

# 2. 测试单个页面
python src/fandom.py template "Template:角色信息" --test "西片"

# 3. 批量转换
python src/fandom.py template "Template:角色信息" --batch
```

### 场景 5：恢复出错的页面

```bash
# 1. 查看历史版本
python src/fandom.py restore "西片" --show-versions

# 2. 恢复到最近的非转换版本
python src/fandom.py restore "西片"
```

## 工作流程建议

### 推荐的安全工作流程

1. **预览** - 使用 `--dry-run` 查看将要修改的内容
2. **测试** - 在单个页面上测试转换
3. **检查** - 到 Wiki 上检查测试结果
4. **批量** - 确认无误后再批量转换
5. **验证** - 抽查几个页面确认转换正确

### 示例：转换模板

```bash
# 步骤 1: 列出页面
python src/fandom.py template "Template:角色信息" --list

# 步骤 2: 测试单个页面
python src/fandom.py template "Template:角色信息" --test "西片" --dry-run
python src/fandom.py template "Template:角色信息" --test "西片"

# 步骤 3: 到 Wiki 上检查西片页面
# 确认：
# - 变量名已转换（名称、图片、别称等）
# - 内容已转换为简体
# - 文件名未被修改（.jpg, .png 等）

# 步骤 4: 批量转换
python src/fandom.py template "Template:角色信息" --batch --dry-run
python src/fandom.py template "Template:角色信息" --batch
```

## 目录结构

```
.
├── .env                  # 环境变量配置（私有）
├── .env.example          # 配置示例
├── requirements.txt      # Python 依赖
├── fandom_bot.py        # 核心库
├── src/                 # 工具脚本
│   ├── fandom.py               # 统一入口（推荐）
│   ├── convert_page.py         # 页面转换
│   ├── convert_category.py     # 分类转换
│   ├── convert_template.py     # 模板转换
│   ├── restore_from_history.py # 恢复页面
│   ├── README.md               # 详细文档
│   ├── test_fandom.py          # 测试连接
│   ├── get_template_info.py    # 获取模板信息
│   └── move_pages.py           # 移动页面
└── doc/                 # 文档
```

## 配置说明

### .env 文件

```bash
FANDOM_DOMAIN=your-wiki.fandom.com
FANDOM_PATH=/zh/
FANDOM_USERNAME=YourBot@BotName
FANDOM_PASSWORD=your_bot_password
CONVERSION_MODE=t2s
```

### 获取 Bot 密码

1. 登录 Fandom Wiki
2. 访问 Special:BotPasswords
3. 创建一个新的 Bot 密码
4. 将用户名和密码填入 .env 文件

## 依赖

- Python 3.6+
- mwclient - MediaWiki API 客户端
- opencc - 繁简转换库
- python-dotenv - 读取 .env 文件（可选）

## 常见问题

### Q: 为什么要先测试？
A: 避免批量修改出错。测试可以让你先在一个页面上验证脚本是否正确工作。

### Q: 文件名会被修改吗？
A: 不会。所有工具都会自动保护文件名（.jpg, .png 等）不被修改，并有验证机制确保保护生效。

### Q: 如果转换出错怎么办？
A: 使用恢复工具可以从历史版本恢复页面：
```bash
python src/fandom.py restore "页面名"
```

### Q: 遇到速率限制怎么办？
A: 脚本会自动检测速率限制并等待 60 秒。如果多次遇到，可以稍后再试。

### Q: 可以转换其他语言吗？
A: 可以修改 .env 中的 CONVERSION_MODE。OpenCC 支持多种转换模式：
- t2s - 繁体到简体
- s2t - 简体到繁体
- 等等

## 安全检查清单

在批量转换前，确认以下事项：

- [ ] 已在单个页面上测试
- [ ] 已到 Wiki 上检查测试结果
- [ ] 变量名转换正确
- [ ] 内容转换为简体中文
- [ ] 文件名未被修改
- [ ] 预览了批量转换的页面列表

全部确认后，再执行批量转换。

## 许可证

MIT License

## 更多信息

- [详细文档](src/README.md)
- [项目概览](PROJECT.md)
- [配置说明](doc/CONFIGURATION.md)
