# BuddyHub

[English README](./README.md)

BuddyHub 是一个面向 Claude Code 的反应式 Buddy 插件。

V1 采用 `TUI-first` 方案：

- 基于 hooks 的状态追踪
- `/buddyhub:status` 紧凑状态视图
- `/buddyhub:open` 详细文本视图
- 可选的 Claude Code 状态栏集成
- 安全的暂停、恢复、禁用、卸载流程

BuddyHub 不要求：

- 外部 GUI 窗口
- 终端专属图形能力
- tmux

## 安装目标

BuddyHub 目标通过 Claude Code marketplace 流程安装：

```text
/plugin marketplace add verycafe/buddyhub
/plugin install buddyhub@buddyhub
```

## 主要命令

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:open`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:disable`
- `/buddyhub:doctor`
- `/buddyhub:statusline-on`
- `/buddyhub:statusline-off`
- `/buddyhub:uninstall`

## 状态栏

BuddyHub 自带状态栏脚本：

- [plugins/buddyhub/scripts/statusline.py](/Users/tvwoo/Projects/buddyhub/plugins/buddyhub/scripts/statusline.py)

V1 不会自动修改 Claude Code 设置。先运行 `/buddyhub:statusline-on` 获取脚本路径，再手动接入 Claude Code 的 status line 配置。

## 文档

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## 当前进展

已经具备：

- marketplace manifest
- plugin manifest
- 命令面
- hook 驱动状态运行时
- 本地测试说明

还需要真实环境验证：

- 已登录 Claude Code 会话中的真实安装
- Claude Code 内部真实 hook payload 行为
- 手动接入状态栏
- 至少一轮跨终端冒烟测试

## 许可证

BuddyHub 采用 `AGPL-3.0-only`（仅 GNU Affero General Public License
v3.0）授权。如果你分发修改版本，或者让用户通过网络与修改版本交互，
你需要按 AGPLv3 提供对应源代码。详见
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE)。
