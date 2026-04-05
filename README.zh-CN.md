# BuddyHub

[English README](./README.md)

BuddyHub 是一个面向 Claude Code 官方 Buddy 的原生视觉定制项目。

它的目标只有一个：

- 增强 Claude Code 右下角已经存在的官方 Buddy 视觉元素

## 当前方向

BuddyHub 现在只专注于一件事：

- 用可配置的附加元素增强用户当前官方 Buddy
- 提供独立 TUI 菜单式的颜色和昵称设置，并在当前版本隐藏元素切换
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
- 右下角官方 Buddy 和 `/buddy` 卡片现在按同一条显示名来源与已验证颜色来源保持一致
- `~/.claude/pet` 不是当前官方 Buddy 视觉增强的主交付路径

## 产品规则

只有当 Claude Code 右下角官方 Buddy 本体真的被增强时，产品才算成功。

文字输出、诊断命令或辅助界面都不算产品主 UI。

## 当前仓库重点

- 官方 Buddy 原生视觉研究
- 版本敏感的二进制补丁
- 外部 TUI 菜单式配置器
- 备份与恢复安全
- 官方 Buddy 视觉变化的验证

## 当前 TUI 入口

现在可以直接运行独立菜单：

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub
```

## 无需发布账号的安装方式

BuddyHub 现在可以直接从 GitHub 安装，不需要先发布到 PyPI、npm 或 Homebrew。

### pip

直接从 GitHub 安装：

```bash
python3 -m pip install "git+https://github.com/verycafe/buddyhub.git"
```

安装完成后，直接运行：

```bash
buddyhub
```

### npm

直接从 GitHub 安装：

```bash
npm install -g github:verycafe/buddyhub
```

安装完成后，直接运行：

```bash
buddyhub
```

### brew

Homebrew 方式目前还没有正式发布。
当前已验证、且不需要账号的安装方式是 `pip` 和 `npm`。

当前一级菜单：
- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Quit`

当前阶段范围说明：
- `element` 切换在这一版里继续隐藏
- BuddyHub 会保持当前已安装元素不变；如果当前没有元素，就继续保持 `none`
- 当前真正开放给用户编辑的只有 `Color` 和 `Nickname`

TUI 会先读取本机当前已安装 Buddy 的真实状态，然后显示：
- `已安装状态`
- `草稿状态`
- `已安装预览`
- `草稿预览`

执行 `Apply` 或 `Restore` 之后，TUI 会显示单独的结果卡片，不再只靠底部一行提示。
结果卡还会汇总这次真正改动了哪些官方 Buddy 可见属性，例如：
- `Display name`
- `Color`

如果想快速做一次非交互检查：

```bash
/Users/tvwoo/Projects/buddyhub/buddyhub --dump-state
```

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
