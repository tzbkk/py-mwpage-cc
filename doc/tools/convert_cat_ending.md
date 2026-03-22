# convert_cat_ending.py - 分类页面批量转换工具

## 功能

批量转换多个分类页面的内容和名称（如果需要）。

## 用法

```bash
python src/convert_cat_ending.py [category1] [category2] ...
python src/convert_cat_ending.py --from-file categories.txt
```

### 参数

- `category1, category2, ...`: 分类名称列表（不含 Category: 前缀）
- `--from-file FILE`: 从文件读取分类列表
- `--dry-run`: 预览模式，不实际保存和移动

## 示例

```bash
# 转换指定分类
python src/convert_cat_ending.py "片頭曲" "片尾曲"

# 转换其他分类
python src/convert_cat_ending.py "角色" "地点" "物品"

# 从文件读取
python src/convert_cat_ending.py --from-file categories.txt

# 预览模式
python src/convert_cat_ending.py "片頭曲" --dry-run
```

### 文件格式

categories.txt 文件格式（以 # 开头的行会被忽略）：
```
片頭曲
片尾曲
# 这是注释
插曲
```

## 工作流程

对于每个指定的分类：

1. 检查分类页面是否存在
2. 转换分类页面内容为简体中文
3. 验证文件名保护
4. 如果分类名称是繁体，移动到简体名称
5. 保存页面

## 输出示例

```
✓ 已登录: bot_username

=== 批量转换分类页面 ===
共 2 个分类

[1/2] 片頭曲
  目标名称: 片头曲
  ✓ 内容已转换
  ✓ 已移动到 Category:片头曲

[2/2] 片尾曲
  目标名称: 片尾曲
  ℹ️  内容无需转换
  ℹ️  无需移动（名称已经是简体）

✅ 完成统计:
  - 总分类数: 2
  - 已处理: 2
  - 失败: 0
```

## 特性

- 支持批量处理多个分类页面
- 从命令行参数或文件读取分类列表
- 同时转换内容和移动页面
- 预览模式 (--dry-run) 查看将要执行的操作
- 自动文件名保护验证
- 统计信息显示成功/失败数量
- 速率限制自动处理

## 与其他分类工具的区别

| 功能 | convert_cat_ending.py | convert_cat_page.py |
|------|----------------------|---------------------|
| 处理数量 | 多个分类 | 多个分类 |
| 移动页面 | ✅ | ❌ |
| 分类名称格式 | 不含 Category: | 完整名称 |

## 使用场景

- 批量转换并移动多个分类页面
- 分类名称需要从繁体改为简体时
- 统一分类命名规范

## 注意事项

- 会移动分类页面（如果名称需要转换）
- 移动时不创建重定向
- 不影响分类下的页面，只处理分类页本身
- 建议先使用 --dry-run 预览
- 建议先在小范围测试
- **脚本只修改 Wiki 页面内容，不会修改任何脚本文件**
