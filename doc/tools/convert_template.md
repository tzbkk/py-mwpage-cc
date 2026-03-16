# convert_template.py - 模板转换工具

## 功能

完整转换模板及其所有引用页面，包括：
1. 转换模板内容
2. 转换所有引用该模板的页面
3. 移动模板页面到简体名称

## 用法

```bash
python src/convert_template.py [template_name]
```

### 参数

- `template_name`: 模板名称（默认：Template:音樂信息）

## 示例

```bash
# 转换默认模板
python src/convert_template.py

# 转换指定模板
python src/convert_template.py "Template:角色信息"
```

## 工作流程

1. **转换模板内容**
   - 读取模板页面
   - 转换为简体中文
   - 保存模板

2. **转换引用页面**
   - 查找所有引用该模板的页面
   - 批量转换这些页面的内容

3. **移动模板**
   - 如果模板名称是繁体，移动到简体名称
   - 不创建重定向

## 输出示例

```
转换模板: Template:音樂信息
模板内容已转换

获取引用 Template:音樂信息 的页面...
找到 15 个页面

[1/15] Template:音樂信息
  内容已转换

...

移动模板: Template:音樂信息 → Template:音乐信息
模板已移动

全部完成!
```

## 与 batch_convert.py 的区别

| 功能 | convert_template.py | batch_convert.py |
|------|---------------------|------------------|
| 转换模板本身 | ✅ | ❌ |
| 转换引用页面 | ✅ | ✅ |
| 移动模板 | ✅ | ❌ |

## 注意事项

- 会修改模板页面本身
- 会移动模板（如果名称需要转换）
- 操作不可逆，建议先备份
