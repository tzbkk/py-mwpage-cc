# convert_cat_page.py - 单个分类页面转换工具

## 功能

转换单个分类页面的内容。

## 用法

```bash
python tools/convert_cat_page.py [page_name]
```

### 参数

- `page_name`: 分类页面名称（默认：Category:音乐）

## 示例

```bash
# 转换默认分类
python tools/convert_cat_page.py

# 转换指定分类
python tools/convert_cat_page.py "Category:角色"

# 转换其他分类
python tools/convert_cat_page.py "Category:音乐"
```

## 工作流程

1. 获取分类页面
2. 转换页面内容为简体中文
3. 保存页面

## 输出示例

```
Category:音乐 内容已转换为简体中文
```

## 特性

- 只转换内容，不移动页面
- 简单快速
- 适合单个分类的快速转换

## 与其他分类工具的区别

| 工具 | 功能 | 是否移动 |
|------|------|---------|
| convert_cat_page.py | 转换单个分类内容 | ❌ |
| convert_cat_ending.py | 批量转换并移动 | ✅ |
| convert_category.py | 转换分类下的页面 | ✅ |

## 使用场景

- 快速转换单个分类页面
- 分类页面不需要改名时
- 测试分类转换效果

## 注意事项

- 只转换分类页面本身，不影响分类下的页面
- 不会移动/重命名分类
- 适合不需要改名的分类页面
