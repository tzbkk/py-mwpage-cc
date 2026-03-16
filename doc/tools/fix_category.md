# fix_category.py - 分类标签修复工具

## 功能

批量替换页面中的分类标签。

## 用法

```bash
python src/fix_category.py [old_category] [new_category]
```

### 参数

- `old_category`: 旧的分类名称（默认：音樂）
- `new_category`: 新的分类名称（默认：音乐）

## 示例

```bash
# 默认替换
python src/fix_category.py

# 指定替换
python src/fix_category.py "音樂" "音乐"

# 其他替换
python src/fix_category.py "舊分類" "新分类"
```

## 工作流程

1. 获取旧分类下的所有页面
2. 在每个页面中查找 `[[Category:旧分类]]`
3. 替换为 `[[Category:新分类]]`
4. 保存修改

## 输出示例

```
获取 Category:音樂 的所有页面...
找到 20 个页面

[1/20] 雖然不會說出口。
  已更新

[2/20] 愛歌
  已更新

[3/20] STARS
  无需修改

...

全部完成!
```

## 使用场景

- 分类页面已移动，需要更新所有引用
- 统一分类名称
- 批量修改分类标签

## 与 update_cat_refs.py 的区别

| 工具 | 功能 | 参数 |
|------|------|------|
| fix_category.py | 替换单个分类 | 旧分类, 新分类 |
| update_cat_refs.py | 批量替换多个分类 | 分类列表 |

## 注意事项

- 只修改页面中的分类标签
- 不移动分类页面本身
- 不修改页面其他内容
- 使用正则表达式精确匹配
