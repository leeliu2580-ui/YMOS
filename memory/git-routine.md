# Git 例行规则

## 目标
- 重要改动必须进入 git 记录。
- 避免把缓存、输出产物、临时文件一并提交。

## 当前策略
- 默认使用白名单提交。
- 自动提交只做 **本地 commit**，不自动 push。
- push GitHub 由人工确认后执行。

## 白名单范围（当前版本）
- `Eyes/`
- `Brain/`
- `持仓与关注/`
- `skills/`
- `memory/`
- `MEMORY.md`
- `IDENTITY.md`
- `USER.md`
- 常用测试/工具脚本（按脚本内配置）

## 明确排除
- `output/`
- `.tools/`
- `.openclaw/`
- `.clawhub/`
- Python 缓存 / node_modules / 临时文件
