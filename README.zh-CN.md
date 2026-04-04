# BuddyHub

[English README](./README.md)

BuddyHub 是一个面向 Claude Code 的 Buddy 增强插件。

BuddyHub 的目标是增强用户当前的 Claude Buddy，而不是用 BuddyHub 自己定义的一只宠物替换它。

当前产品状态：

- BuddyHub 已能验证当前官方 Buddy 身份
- BuddyHub 已能追踪 Claude 侧运行时状态
- BuddyHub 还没有打通第三方对右下角官方 Buddy 的原生控制路径

核心产品规则：

- 真正目标是增强 Claude Code 右下角已经存在的官方 Buddy
- 文字命令和 status line 只是诊断/辅助层
- 仅有文字输出不算产品完成

当前仓库状态：

- 基于 hooks 的状态追踪
- 已验证 Buddy 身份读取
- `/buddyhub:status` 紧凑诊断视图
- `/buddyhub:open` 详细诊断视图
- 可选的 Claude Code 状态栏集成
- 安全的暂停、恢复、禁用、卸载流程

身份规则：

- 可以显示已验证的 Buddy 身份字段
- 未确认的 Buddy 身份字段必须保持 unavailable
- 不能用一个通用 Buddy 外形冒充用户当前 Buddy

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
- 诊断型文本/status 输出

还需要真实环境验证：

- 面向官方原生 Buddy 的可达控制面
- 右下官方 Buddy 的真实增强效果
- hook 到官方 Buddy 动态的真实传递
- 手动接入状态栏
- 至少一轮针对诊断层的跨终端冒烟测试

## 许可证

BuddyHub 采用 `AGPL-3.0-only`（仅 GNU Affero General Public License
v3.0）授权。如果你分发修改版本，或者让用户通过网络与修改版本交互，
你需要按 AGPLv3 提供对应源代码。详见
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE)。
