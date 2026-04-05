# BuddyHub

[English README](./README.md)

BuddyHub 是一个面向 Claude Code 官方 Buddy 的原生视觉定制项目。

它的目标只有一个：

- 增强 Claude Code 右下角已经存在的官方 Buddy 视觉元素

## 当前方向

BuddyHub 现在只专注于一件事：

- 用可配置的附加元素增强用户当前官方 Buddy
- 提供元素、颜色和昵称相关设置
- 应用当前保存配置，并提示用户重启 Claude Code

BuddyHub 当前不再把这些当作主线：

- Claude 运行状态追踪
- status line 主体验
- hooks 驱动 Buddy 行为
- 平行文字 Buddy 产品

## 已经证明的事实

- 官方 Buddy 的视觉表嵌在 Claude Code 主二进制里
- 在当前 macOS 机器上，已确认的示例目标文件是：
  - `/Users/tvwoo/.local/share/claude/versions/2.1.92`
- 对该二进制的工作区副本做补丁后，右下角官方 Buddy 本体确实发生了视觉变化
- 当前对 `blob` 已验证可用的附加元素有：
  - `tophat`
  - `coffee`
  - `book`
- 当前已验证可用的颜色预设有：
  - `green`
  - `orange`
  - `blue`
  - `pink`
  - `purple`
  - `red`
  - `black`
- 当前仍显示但未验证、不会生效的颜色预设是：
  - `white`
- 右下角官方 Buddy 的显示名现在也已验证可通过这里安全覆盖：
  - `~/.claude.json` 的 `companion.name`
- `~/.claude/pet` 不是当前官方 Buddy 视觉增强的主交付路径

## 产品规则

只有当 Claude Code 右下角官方 Buddy 本体真的被增强时，产品才算成功。

文字输出、诊断命令或辅助界面都不算产品主 UI。

## 当前仓库重点

- 官方 Buddy 原生视觉研究
- 版本敏感的二进制补丁
- 附加元素目录与设置模型
- 备份与恢复安全
- 官方 Buddy 视觉变化的验证

## 文档

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## 范围说明

当前已验证的原生路径是这台机器和这类安装方式下的内部实现细节。

它还不是官方公开文档里承诺的稳定 API，也不能直接当作跨平台固定路径。

## 许可证

BuddyHub 采用 `AGPL-3.0-only`（仅 GNU Affero General Public License
v3.0）授权。如果你分发修改版本，或者让用户通过网络与修改版本交互，
你需要按 AGPLv3 提供对应源代码。详见
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE)。
