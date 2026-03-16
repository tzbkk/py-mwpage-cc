# batch_convert.py - 批量转换工具

## 功能

批量转换所有引用指定模板的页面内容。

## 用法

```bash
python src/batch_convert.py <template_name>
```

### 参数

- `template_name`: 模板名称（如 "Template:音樂信息"）

## 示例

```bash
# 转换所有使用 Template:音樂信息 的页面
python src/batch_convert.py "Template:音樂信息"

# 转换其他模板
python src/batch_convert.py "Template:角色信息"
```

## 工作流程

1. 获取所有引用指定模板的页面
2. 遍历每个页面
3. 转换页面内容（繁体→简体）
4. 如果内容有变化，则保存

## 输出示例

```
获取引用 Template:音樂信息 的页面...
找到 15 个页面

[1/15] 处理: 雖然不會說出口。
  已保存

[2/15] 处理: 愛歌
  无需修改

...

全部完成!
```

## 特性

- 自动跳过图片字段
- 只保存有实际变化的页面
- 显示处理进度

## 注意事项

- 需要先配置 `config.json`
- 模板名称需要包含 "Template:" 前缀
- 不会移动/重命名页面，只转换内容
