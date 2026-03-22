# update_cat_refs.py - 分类引用更新工具

## 功能

批量更新多个分类的引用标签为简体中文。

## 用法

```bash
python src/update_cat_refs.py [category1] [category2] ...
python src/update_cat_refs.py --from-file categories.txt
```

### 参数

- `category1, category2, ...`: 要处理的分类名称列表（不含 Category: 前缀）
- `--from-file FILE`: 从文件读取分类列表
- `--dry-run`: 预览模式，不实际保存

## 示例

```bash
# 更新指定分类
python src/update_cat_refs.py "片頭曲" "片尾曲"

# 更新其他分类
python src/update_cat_refs.py "角色" "地点"

# 从文件读取
python src/update_cat_refs.py --from-file categories.txt

# 预览模式
python src/update_cat_refs.py "片頭曲" --dry-run
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

对于每个分类：

1. 获取分类下的所有页面
2. 在页面中查找并替换分类标签
3. 保存修改

## 替换规则

工具会自动将分类标签中的繁体名称转换为简体：
- `[[Category:片頭曲]]` → `[[Category:片头曲]]`
- `[[Category:片尾曲]]` → `[[Category:片尾曲]]`
- 其他分类也会自动转换为简体

## 输出示例

```
✓ 已登录: bot_username

=== 批量更新分类引用 ===
共 2 个分类

[1/2] 片頭曲
  找到 10 个引用 Category:片頭曲 的页面
    ✓ 雖然不會說出口。 已更新
    ✓ 愛歌 已更新
    ...

[2/2] 片尾曲
  找到 8 个引用 Category:片尾曲 的页面
    ✓ 小小戀歌 已更新
    ✓ 零釐米 已更新
    ...

✅ 完成统计:
  - 总分类数: 2
  - 已更新: 18
  - 跳过: 0
  - 失败: 0
```

## 特性

- 支持批量处理多个分类
- 从命令行参数或文件读取分类列表
- 自动查找并更新引用
- 预览模式 (--dry-run) 查看将要执行的操作
- 统计信息显示成功/失败/跳过数量
- 速率限制自动处理

## 与 fix_category.py 的区别

| 工具 | 处理方式 | 适用场景 |
|------|---------|---------|
| update_cat_refs.py | 批量多个 | 多个分类需要更新 |
| fix_category.py | 单个指定 | 单个分类替换 |

## 注意事项

- 修改页面中的分类标签
- 不移动分类页面本身
- 可以处理多个分类的批量更新
- 建议先使用 --dry-run 预览
- 建议先在小范围测试
- **脚本只修改 Wiki 页面内容，不会修改任何脚本文件**
