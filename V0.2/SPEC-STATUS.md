# BuddyHub V0.2 Spec Status

- Last updated: 2026-04-05
- Rule: whenever one spec reaches a new milestone, update this file in the same change.

| Spec | File | Status | Notes |
| --- | --- | --- | --- |
| 01 | `specs/01-customization-model-spec.md` | Done | 当前颜色、昵称、语言、隐藏 element 规则已落到实现。 |
| 02 | `specs/02-tui-menu-and-preview-spec.md` | In Progress | Python TUI 已稳定；Ink 现已通过 core-backed bridge 获取 canonical color availability model，但公开菜单契约与预览收口仍未完成。 |
| 03 | `specs/03-platform-detection-and-setup-spec.md` | Done | 自动探测、`Setup` 兜底、系统语言默认与 Ink `needs_setup -> Setup` 启动契约都已有实现和验证证据。 |
| 04 | `specs/04-apply-restore-and-uninstall-spec.md` | Done | Python 与 Ink 现都通过同一条 core lifecycle 执行 `apply/restore/uninstall`；bridge 读调用无副作用，自动卸载链也已接通。 |
| 05 | `specs/05-install-and-distribution-spec.md` | In Progress | npm 安装已上线，但当前公开入口仍是 Python TUI，且运行时前提与 Ink 切换条件还需收口。 |

## Current Ink Cutover Blockers

- 当前公开 `buddyhub` 入口仍是 Python TUI，而不是 Ink
- npm 公开安装路径与当前真实运行时前提仍存在偏差
- Ink 的公开菜单语义与最终产品预览结构仍需继续收口

## Status Definitions

- `Todo`: spec exists but implementation has not started
- `In Progress`: implementation exists, but scope or verification is not yet complete
- `Done`: implementation and verification evidence both exist for the current phase
