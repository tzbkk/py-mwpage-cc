# update_cat_refs.py - 分类引用更新工具

## 功能

批量更新多个分类的引用标签。

## 用法

```bash
python tools/update_cat_refs.py [category1] [category2] ...
```

### 参数

- `category1, category2, ...`: 要处理的分类名称列表（默认：片頭曲, 片尾曲）

## 示例

```bash
# 更新默认分类
python tools/update_cat_refs.py

# 更新指定分类
python tools/update_cat_refs.py "片頭曲" "片尾曲" "插曲"

# 更新其他分类
python tools/update_cat_refs.py "角色" "地点"
```

## 工作流程

对于每个分类：

1. 获取分类下的所有页面
2. 在页面中查找并替换分类标签
3. 保存修改

## 内置替换规则

工具会自动处理以下替换：
- `[[Category:片頭曲]]` → `[[Category:片头曲]]`
- `[[Category:片尾曲]]` → `[[Category:片尾曲]]`

## 输出示例

```
更新引用 Category:片頭曲 的页面...
  找到 10 个页面
  已更新: 雖然不會說出口。
  已更新: 愛歌

更新引用 Category:片尾曲 的页面...
  找到 8 个页面
  已更新: 小小戀歌
  已更新: 零釐米

完成!
```

## 特性

- 批量处理多个分类
- 支持自定义分类列表
- 自动查找并更新引用

## 与 fix_category.py 的区别

| 工具 | 处理方式 | 适用场景 |
|------|---------|---------|
| update_cat_refs.py | 批量多个 | 多个分类需要更新 |
| fix_category.py | 单个指定 | 单个分类替换 |

## 注意事项

- 修改页面中的分类标签
- 不移动分类页面本身
- 可以处理多个分类的批量更新
