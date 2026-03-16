# 配置说明

## 配置方式

本工具支持两种配置方式，推荐使用 `.env` 文件。

### 方式1：使用 .env 文件（推荐）

**优点：**
- 不会被 Git 提交（已在 .gitignore 中）
- 更安全，适合存储敏感信息
- 简单直观

**步骤：**
```bash
cp .env.example .env
# 编辑 .env 文件
```

**配置内容：**
```bash
# Wiki 站点配置
FANDOM_DOMAIN=your-wiki.fandom.com
FANDOM_PATH=/zh/

# 机器人账号
FANDOM_USERNAME=YourBot@BotName
FANDOM_PASSWORD=your_bot_password

# 转换模式
CONVERSION_MODE=t2s
```

### 方式2：使用 config.json 文件

**优点：**
- 结构化配置
- 支持复杂配置
- 可添加注释说明

**步骤：**
```bash
cp config.json.example config.json
# 编辑 config.json 文件
```

**配置内容：**
参考 `config.json.example` 文件，根据注释说明填入配置。

## 配置优先级

1. 如果存在 `.env` 文件，优先使用环境变量
2. 如果不存在 `.env`，则使用 `config.json`
3. 如果都不存在，程序会报错提示

## 获取机器人密码

1. 登录你的 Fandom Wiki
2. 访问 `Special:BotPasswords` 页面
3. 创建新的机器人密码
4. 填写机器人名称（如：MyBot）
5. 选择需要的权限（至少需要编辑、移动页面权限）
6. 保存生成的密码

**账号格式：** `你的用户名@机器人名称`
**示例：** `AdminUser@MyBot`

## 配置项说明

### FANDOM_DOMAIN
- Wiki 站点域名
- 示例：`karakai-jouzu-no-takagi-san.fandom.com`

### FANDOM_PATH
- Wiki 路径
- 中文 Wiki 通常是 `/zh/`
- 英文 Wiki 通常是 `/`

### FANDOM_USERNAME
- 机器人账号
- 格式：`用户名@机器人名`

### FANDOM_PASSWORD
- 机器人密码
- 在 `Special:BotPasswords` 生成

### CONVERSION_MODE
- 转换模式
- `t2s`：繁体转简体
- `s2t`：简体转繁体
- 其他模式参考 OpenCC 文档

## 安全提示

- ⚠️ **不要**将 `.env` 或 `config.json` 提交到 Git
- ⚠️ **不要**在公开场合分享你的机器人密码
- ⚠️ 定期更换机器人密码
- ⚠️ 只给予必要的权限

## 故障排除

### 连接失败
1. 检查域名是否正确
2. 检查网络连接
3. 确认 Wiki 站点可访问

### 登录失败
1. 检查用户名格式是否正确
2. 检查密码是否正确
3. 确认机器人密码已创建
4. 检查权限设置

### 配置未生效
1. 确认文件名正确（`.env` 或 `config.json`）
2. 检查文件格式是否正确
3. 确认没有多余的空格或引号
