# convert_cat_ending.py - 分类页面转换工具

## 功能

批量转换多个分类页面的内容和名称。

## 用法

```bash
python src/convert_cat_ending.py [category1] [category2] ...
```

### 参数

- `category1, category2, ...`: 分类名称列表（默认：片頭曲, 片尾曲）

## 示例

```bash
# 转换默认分类
python src/convert_cat_ending.py

# 转换指定分类
python src/convert_cat_ending.py "片頭曲" "片尾曲" "插曲"

# 转换其他分类
python src/convert_cat_ending.py "角色" "地点" "物品"
```

## 工作流程

对于每个指定的分类：

1. 检查分类页面是否存在
2. 转换分类页面内容
3. 如果分类名称是繁体，移动到简体名称

## 输出示例

```
处理 Category:片頭曲
  目标名称: 片头曲
  内容已转换
  页面已移动

处理 Category:片尾曲
  目标名称: 片尾曲
  内容已转换
  页面已移动

完成!
```

## 特性

- 批量处理多个分类
- 同时转换内容和移动页面
- 自动跳过不存在的页面

## 与 convert_cat_page.py 的区别

| 功能 | convert_cat_ending.py | convert_cat_page.py |
|------|----------------------|---------------------|
| 处理数量 | 多个分类 | 单个分类 |
| 移动页面 | ✅ | ❌ |
| 参数方式 | 命令行列表 | 单个参数 |

## 注意事项

- 会移动分类页面（如果名称需要转换）
- 移动时不创建重定向
- 不影响分类下的页面，只处理分类页本身
