# src/ 目录说明

这是项目的主要工具目录，包含所有 Wiki 操作工具。

## 主要工具

### 统一入口（推荐）

**fandom.py** - 统一的命令行工具，提供所有转换功能

```bash
python src/fandom.py <command> [options]
```

**命令：**
- `page` - 转换单个或多个页面
- `category` - 转换分类下的所有页面
- `template` - 转换使用模板的所有页面
- `restore` - 从历史版本恢复页面

### 页面转换

**convert_page.py** - 转换单个或多个页面

```bash
python src/convert_page.py "页面名" [选项]
```

**选项：**
- `--dry-run` - 预览模式
- `--show-diff` - 显示修改详情
- `--from-file FILE` - 从文件读取页面列表

### 分类转换

**convert_category.py** - 转换分类下的所有页面

```bash
python src/convert_category.py "分类名" [选项]
```

**选项：**
- `--list` - 只列出页面
- `--dry-run` - 预览模式
- `--limit N` - 限制转换数量
- `--no-test-first` - 跳过测试

### 模板转换

**convert_template.py** - 转换使用模板的所有页面

```bash
python src/convert_template.py "Template:模板名" [选项]
```

**选项：**
- `--list` - 只列出页面
- `--test PAGE` - 测试单个页面
- `--batch` - 批量转换
- `--dry-run` - 预览模式
- `--no-doc` - 不转换 /doc

### 页面恢复

**restore_from_history.py** - 从历史版本恢复页面

```bash
python src/restore_from_history.py "页面名" [选项]
```

**选项：**
- `--show-versions` - 显示历史版本

## 辅助工具

### test_fandom.py
测试 Wiki 连接和登录。

```bash
python src/test_fandom.py [页面名]
```

### get_template_info.py
获取模板信息。

```bash
python src/get_template_info.py "Template:模板名"
```

### move_pages.py
批量移动/重命名页面。

```bash
python src/move_pages.py "页面1" "页面2" ...
```

## 特定用途工具

这些工具用于特定场景：

- `convert_cat_ending.py` - 转换分类页面后缀
- `convert_cat_page.py` - 转换单个分类页面
- `convert_seasons.py` - 转换季度页面
- `update_cat_refs.py` - 更新分类引用

## 使用建议

### 日常使用

对于日常的繁简转换任务，推荐使用：

```bash
# 使用统一入口
python src/fandom.py page "页面名"
python src/fandom.py category "分类名"
python src/fandom.py template "Template:模板名" --batch
```

### 快速测试

```bash
# 测试连接
python src/test_fandom.py

# 预览转换
python src/fandom.py page "页面名" --dry-run
```

### 批量操作

```bash
# 从文件批量转换
python src/convert_page.py --from-file pages.txt

# 转换分类（限制数量）
python src/convert_category.py "分类名" --limit 10
```

## 核心特性

所有主要工具都支持：

- ✅ **文件名保护** - 自动保护 .jpg, .png 等文件名
- ✅ **转换验证** - 验证文件名未被修改
- ✅ **测试模式** - 先测试单个页面
- ✅ **预览模式** - 使用 --dry-run 预览
- ✅ **安全恢复** - 可从历史版本恢复
- ✅ **速率限制处理** - 自动处理 API 限制

## 重要原则

**⚠️ 永远先测试单个页面，再批量应用！**

1. 使用 `--dry-run` 预览修改
2. 在单个页面上测试
3. 到 Wiki 上检查结果
4. 确认无误后再批量转换

## 文件清单

```
src/
├── fandom.py                      # 统一入口
├── convert_page.py                # 页面转换
├── convert_category.py            # 分类转换
├── convert_template.py            # 模板转换
├── restore_from_history.py        # 恢复页面
├── test_fandom.py                 # 测试连接
├── get_template_info.py           # 获取模板信息
├── move_pages.py                  # 移动页面
├── convert_cat_ending.py         # 特定用途
├── convert_cat_page.py           # 特定用途
├── convert_seasons.py            # 特定用途
├── update_cat_refs.py            # 更新分类引用
└── README.md                      # 本文档
```

## 更多信息

- [主文档](../README.md)
- [项目概览](../PROJECT.md)
