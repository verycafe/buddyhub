# BuddyHub

[English README](./README.md)

BuddyHub 是一个面向 Claude Code 官方 Buddy 的独立 TUI 配置器。

它会直接调整 Claude Code 里的真实 Buddy，并提供预览、应用、恢复和自动卸载。

## 安装

直接用 `npm` 从 GitHub 安装：

```bash
npm install -g github:verycafe/buddyhub
```

安装完成后直接运行：

```bash
buddyhub
```

首次启动时，如果系统语言可以被可靠识别，BuddyHub 会默认使用系统语言作为菜单语言。

## 平台探测

- BuddyHub 会先尝试通过 `PATH` 上的 `claude` 启动器自动识别 Claude
- 在 macOS 和 Linux 上，如果存在标准版本目录，BuddyHub 也会继续扫描版本目录
- 如果自动探测仍然不完整，BuddyHub 会先进入 `Setup`，引导用户手动填写：
  - Claude 可执行文件路径
  - Claude 配置文件路径

这些覆盖路径会保存在 BuddyHub 自己的设置里，后续启动会继续复用。

`Setup` 里也会直接给出参考提示，例如：

- macOS/Linux：`which claude`
- Windows：`where claude`
- 额外参考：`claude doctor`

## 菜单

当前一级菜单：
- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Uninstall`
- `Quit`

当前阶段范围说明：
- `element` 切换在这一版里继续隐藏
- BuddyHub 会保持当前已安装元素不变；如果当前没有元素，就继续保持 `none`
- 当前真正开放给用户编辑的只有 `Color` 和 `Nickname`

TUI 启动后会先读取本机当前已安装 Buddy 的真实状态，并在右侧显示实时预览。

执行 `Apply` 后，需要重启 Claude Code 才会重新加载官方 Buddy。

`Uninstall` 现在是全自动的：
- 如果 BuddyHub 当前有补丁，会先自动恢复
- 自动删除旧的 Claude 插件痕迹，例如 `~/.claude/plugins/.../buddyhub*`
- 自动删除 BuddyHub 独立数据目录 `~/.buddyhub`
- 会自动在后台安排当前 BuddyHub 的 npm 卸载

## 文档

- [PRD.md](/Users/tvwoo/Projects/buddyhub/PRD.md)
- [TESTING.md](/Users/tvwoo/Projects/buddyhub/TESTING.md)
- [specs/README.md](/Users/tvwoo/Projects/buddyhub/specs/README.md)
- [research/README.md](/Users/tvwoo/Projects/buddyhub/research/README.md)

## 许可证

BuddyHub 采用 `AGPL-3.0-only`（仅 GNU Affero General Public License
v3.0）授权。如果你分发修改版本，或者让用户通过网络与修改版本交互，
你需要按 AGPLv3 提供对应源代码。详见
[LICENSE](/Users/tvwoo/Projects/buddyhub/LICENSE)。
