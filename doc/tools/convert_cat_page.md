# convert_cat_page.py - 分类页面批量转换工具

## 功能

批量转换分类页面的内容为简体中文。

## 用法

```bash
python src/convert_cat_page.py [page1] [page2] ...
python src/convert_cat_page.py --from-file categories.txt
```

### 参数

- `page1, page2, ...`: 分类页面名称列表
- `--from-file FILE`: 从文件读取页面列表
- `--dry-run`: 预览模式，不实际保存

## 示例

```bash
# 转换单个分类
python src/convert_cat_page.py "Category:音乐"

# 批量转换多个分类
python src/convert_cat_page.py "Category:音乐" "Category:角色" "Category:地点"

# 从文件读取
python src/convert_cat_page.py --from-file categories.txt

# 预览模式
python src/convert_cat_page.py "Category:音乐" --dry-run
```

### 文件格式

categories.txt 文件格式（以 # 开头的行会被忽略）：
```
Category:音乐
Category:角色
# 这是注释
Category:地点
```

## 工作流程

1. 获取分类页面
2. 转换页面内容为简体中文
3. 验证文件名保护
4. 保存页面

## 输出示例

```
=== 批量转换分类页面 ===
共 2 个页面

[1/2] Category:音乐
  ✓ Category:音乐 已转换

[2/2] Category:角色
  ℹ️  Category:角色 无需转换

✅ 完成统计:
  - 总页面数: 2
  - 已修改: 1
  - 跳过: 1
  - 失败: 0
```

## 特性

- 支持批量处理多个分类页面
- 从命令行参数或文件读取页面列表
- 预览模式 (--dry-run) 查看将要执行的操作
- 自动文件名保护验证
- 统计信息显示成功/失败/跳过数量
- 速率限制自动处理

## 与其他分类工具的区别

| 工具 | 功能 | 是否移动 | 处理对象 |
|------|------|---------|---------|
| convert_cat_page.py | 批量转换分类内容 | ❌ | 分类页面本身 |
| convert_cat_ending.py | 批量转换并移动 | ✅ | 分类页面本身 |
| convert_category.py | 转换分类下的页面 | ❌ | 分类下的页面 |

## 使用场景

- 批量转换多个分类页面
- 分类页面不需要改名时
- 测试分类转换效果
- 快速处理多个分类

## 注意事项

- 只转换分类页面本身，不影响分类下的页面
- 不会移动/重命名分类
- 建议先使用 --dry-run 预览
- 建议先在小范围测试
- **脚本只修改 Wiki 页面内容，不会修改任何脚本文件**
