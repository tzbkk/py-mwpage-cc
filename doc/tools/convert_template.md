# convert_template.py - 模板转换工具

## 功能

转换使用指定模板的所有页面内容。

## 用法

```bash
python src/convert_template.py <template_name> [选项]
```

### 参数

- `template_name`: 模板名称（包含 Template: 前缀）
- `--list`: 只列出使用该模板的页面
- `--test PAGE`: 测试模式，转换单个页面
- `--batch`: 批量模式，转换所有使用该模板的页面
- `--dry-run`: 预览模式，不实际保存
- `--no-test-first`: 跳过第一个页面的测试
- `--no-doc`: 不转换 /doc 页面

## 示例

```bash
# 列出使用模板的页面
python src/convert_template.py "Template:角色信息" --list

# 测试单个页面（推荐第一步）
python src/convert_template.py "Template:角色信息" --test "西片"

# 预览单个页面的修改
python src/convert_template.py "Template:角色信息" --test "西片" --dry-run

# 批量转换所有页面（测试成功后）
python src/convert_template.py "Template:角色信息" --batch

# 预览批量转换
python src/convert_template.py "Template:角色信息" --batch --dry-run

# 跳过第一个页面测试
python src/convert_template.py "Template:角色信息" --batch --no-test-first

# 不包含 /doc 页面
python src/convert_template.py "Template:角色信息" --batch --no-doc
```

## 工作流程

### 列出模式 (--list)
1. 获取所有使用该模板的页面
2. 显示页面列表

### 测试模式 (--test)
1. 转换单个页面
2. 显示转换统计
3. 验证文件名保护
4. 可选保存修改

### 批量模式 (--batch)
1. 获取所有使用该模板的页面
2. 如果需要，先测试第一个页面
3. 批量转换所有页面
4. 显示统计信息

## 输出示例

### 列出模式
```
📋 获取使用 Template:角色信息 的页面...
找到 15 个页面

文档页面: Template:角色信息/doc

页面列表:
  1. 西片
  2. 真野
  3. 月本早苗
  ...
```

### 测试模式
```
=== 测试模式 ===
页面: 西片
模板: Template:角色信息

📊 转换统计 - 西片
  - 总行数: 50
  - 修改行数: 12
  ✓ 文件名保护正常

📝 变量名转换检查:
  ✓ 名稱 → 名称
  ✓ 圖片 → 图片
  ✓ 別稱 → 别称

💾 保存更改...
✅ 测试成功！页面已保存

👉 请到 Wiki 上检查页面确认无误后，再使用 --batch 模式
```

### 批量模式
```
=== 批量转换模式 ===
模板: Template:角色信息

🔍 先测试第一个页面...

📊 转换统计 - 西片
  - 总行数: 50
  - 修改行数: 12
  ✓ 文件名保护正常

✓ 测试通过

👉 请到 Wiki 上检查这个页面，确认无误后继续
继续批量转换？(y/n): y

开始批量转换...

[1/15] 西片
  ✓ 已转换

[2/15] 真野
  - 无需修改

...

✅ 完成统计:
  - 总页面数: 15
  - 已修改: 12
  - 跳过: 3
  - 失败: 0
```

## 特性

- 三种工作模式：列出、测试、批量
- 测试单个页面后再批量转换
- 自动文件名保护验证
- 可选包含/排除 /doc 页面
- 预览模式查看将要执行的修改
- 统计信息显示成功/失败/跳过数量
- 速率限制自动处理

## 推荐工作流程

1. **列出页面** - 查看所有使用该模板的页面
2. **测试单个** - 在单个页面上测试转换
3. **检查结果** - 到 Wiki 上确认转换正确
4. **批量转换** - 使用批量模式转换所有页面

## 注意事项

- 建议先使用 --test 模式测试单个页面
- 建议先使用 --dry-run 预览批量转换
- 测试成功后再进行批量转换
- 操作不可逆，建议先备份
- 不会移动模板或页面，只转换内容
- **脚本只修改 Wiki 页面内容，不会修改任何脚本文件**
