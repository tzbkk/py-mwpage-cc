# test_fandom.py - 连接测试工具

## 功能

测试与 Fandom Wiki 的连接和登录。

## 用法

```bash
python tools/test_fandom.py [page_name]
```

### 参数

- `page_name`: 要测试的页面名称（默认：STARS）

## 示例

```bash
# 测试默认页面
python tools/test_fandom.py

# 测试指定页面
python tools/test_fandom.py "首页"

# 测试其他页面
python tools/test_fandom.py "Template:音樂信息"
```

## 输出示例

```
登录成功! 用户: Lunisha Kumina@lunishabot

页面标题: STARS
是否存在: True

页面内容:
{{音乐信息
|名称 = STARS
...
}}
```

## 测试内容

1. **连接测试**
   - 连接到 Wiki 站点
   - 使用配置的账号登录

2. **页面测试**
   - 获取指定页面
   - 检查页面是否存在
   - 读取并显示页面内容

## 使用场景

- 首次配置时测试连接
- 验证登录凭据
- 检查页面是否可访问
- 调试连接问题

## 特性

- 只读操作，不修改任何内容
- 验证配置是否正确
- 快速检查 Wiki 访问权限

## 故障排除

如果连接失败，检查：
1. `config.json` 中的站点配置
2. 机器人账号和密码
3. 网络连接
4. Wiki 站点是否可访问

## 注意事项

- 这是第一个应该运行的工具
- 确保配置正确后再运行其他工具
- 只用于测试，不做任何修改
