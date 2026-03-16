# py-mwpage-cc

Fandom Wiki/MediaWiki 页面简繁转换自动化工具

## 项目结构

```
py-mwpage-cc/
├── fandom_bot.py        # 核心库
├── src/               # 12个通用工具
├── doc/                 # 完整文档
├── .env.example         # 配置示例
└── requirements.txt     # 依赖列表
```

## 特性

- ✅ 繁体中文 → 简体中文批量转换
- ✅ 支持模板、分类、页面批量处理
- ✅ 通用化设计，可配置使用
- ✅ 完整的命令行参数支持
- ✅ 详细的文档和示例

## 统计

- 工具脚本：12个
- 文档文件：16个
- 总代码行数：2557行
- 配置方式：.env 或 config.json

## 快速开始

```bash
# 克隆仓库
git clone <your-repo-url> py-mwpage-cc
cd py-mwpage-cc

# 安装依赖
pip install -r requirements.txt

# 配置
cp .env.example .env
# 编辑 .env 填入配置

# 测试
python src/test_fandom.py
```

## 许可证

MIT License
