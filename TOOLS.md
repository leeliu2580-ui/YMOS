# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Search Skills

- 已安装：`skills/exa-search`
- 已安装：`skills/grok-search`
- 使用原则：
  - `exa-search` → 官方文档、参数、定价、官网、正文提取
  - `grok-search` → 实时动态、社区讨论、舆情扫描、多源综述
- 投研默认规则：
  - `grok-search` 负责看外面现在怎么说
  - `exa-search` 负责回到官方或源头找证据
- 详细说明见：`docs/搜索技能使用说明.md`

Add whatever helps you do your job. This is your cheat sheet.
