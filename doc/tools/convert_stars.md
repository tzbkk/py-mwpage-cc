# convert_stars.py - 单页面转换工具

## 功能

转换单个页面内容，保留图片字段不变。

## 用法

```bash
python tools/convert_stars.py [page_name]
```

### 参数

- `page_name`: 页面名称（默认：STARS）

## 示例

```bash
# 转换默认页面
python tools/convert_stars.py

# 转换指定页面
python tools/convert_stars.py "角色信息"

# 转换其他页面
python tools/convert_stars.py "主要角色"
```

## 工作流程

1. 获取指定页面
2. 转换页面内容（跳过图片字段）
3. 保存页面

## 输出示例

```
保存成功!
```

## 特性

- 自动跳过图片字段（图片、圖片）
- 只转换内容，不移动页面
- 适合转换单个页面

## 与其他工具的区别

- **convert_stars.py**: 转换单个页面
- **batch_convert.py**: 批量转换引用模板的页面
- **convert_category.py**: 转换分类下的所有页面

## 使用场景

- 快速转换单个页面
- 测试转换效果
- 处理不需要批量操作的单个页面

## 注意事项

- 只保存有实际变化的页面
- 不会移动/重命名页面
- 适合测试和小范围修改
