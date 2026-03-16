# 快速使用指南

## 1. 首次使用

### 1.1 安装依赖
```bash
pip install -r requirements.txt
```

### 1.2 配置

**方式1：使用 .env 文件（推荐）**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

`.env` 文件内容：
```bash
FANDOM_DOMAIN=your-wiki.fandom.com
FANDOM_PATH=/zh/
FANDOM_USERNAME=YourBot@BotName
FANDOM_PASSWORD=your_bot_password
CONVERSION_MODE=t2s
```

**方式2：使用 config.json 文件**
```bash
cp config.json.example config.json
# 编辑 config.json 文件
```

### 1.3 测试连接
```bash
python src/test_fandom.py
```

## 2. 常用场景

### 场景1: 转换模板及其引用的页面
```bash
# 完整转换（模板+引用+移动）
python src/convert_template.py "Template:音樂信息"

# 仅转换引用页面
python src/batch_convert.py "Template:音樂信息"
```

### 场景2: 转换分类
```bash
# 转换分类下的所有页面（内容+名称）
python src/convert_category.py "音樂"

# 仅转换分类页面本身
python src/convert_cat_page.py "Category:音乐"

# 批量转换多个分类
python src/convert_cat_ending.py "片頭曲" "片尾曲"
```

### 场景3: 批量移动页面
```bash
# 移动指定页面
python src/move_pages.py "頁面1" "頁面2" "頁面3"
```

### 场景4: 修复分类引用
```bash
# 替换单个分类标签
python src/fix_category.py "音樂" "音乐"

# 批量替换多个分类标签
python src/update_cat_refs.py "片頭曲" "片尾曲"
```

### 场景5: 转换系列页面
```bash
# 转换季度页面及其子页面
python src/convert_seasons.py "动画第一季" "动画第二季"
```

### 场景6: 转换单个页面
```bash
# 转换单个页面
python src/convert_stars.py "STARS"
```

## 3. 工作流程建议

### 新 Wiki 转换流程
1. 测试连接 → `test_fandom.py`
2. 转换模板 → `convert_template.py`
3. 转换分类 → `convert_category.py`
4. 转换其他页面 → `batch_convert.py` 或 `convert_seasons.py`
5. 修复引用 → `fix_category.py` 或 `update_cat_refs.py`

### 日常维护
- 单个页面修改：`convert_stars.py`
- 批量重命名：`move_pages.py`
- 查看模板：`get_template_info.py`

## 4. 注意事项

- 所有工具都会自动跳过图片字段
- 移动页面时不创建重定向
- 建议先在小范围测试
- 操作前确认配置正确
