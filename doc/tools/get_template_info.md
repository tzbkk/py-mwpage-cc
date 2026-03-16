# get_template_info.py - 模板信息查询工具

## 功能

获取并显示模板的详细信息。

## 用法

```bash
python src/get_template_info.py [template_name]
```

### 参数

- `template_name`: 模板名称（默认：Template:音樂信息）

## 示例

```bash
# 查询默认模板
python src/get_template_info.py

# 查询指定模板
python src/get_template_info.py "Template:角色信息"

# 查询其他模板
python src/get_template_info.py "Template:音乐信息"
```

## 输出示例

```
模板页面: Template:音樂信息
是否存在: True

模板内容:
<includeonly>
{| class="infobox"
|-
! colspan="2" | {{{名称}}}
...
</includeonly>
```

## 显示信息

- 模板页面名称
- 模板是否存在
- 模板的完整内容

## 使用场景

- 查看模板内容
- 确认模板是否存在
- 检查模板语法
- 调试模板问题

## 特性

- 只读操作，不修改任何内容
- 快速查看模板信息
- 适合调试和检查

## 注意事项

- 只显示信息，不做任何修改
- 可以查看任何页面的信息
- 适合在执行批量操作前检查模板状态
