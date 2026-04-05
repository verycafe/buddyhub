# BuddyHub V0.2 Spec Status

- Last updated: 2026-04-05
- Rule: whenever one spec reaches a new milestone, update this file in the same change.

| Spec | File | Status | Notes |
| --- | --- | --- | --- |
| 01 | `specs/01-customization-model-spec.md` | Done | 当前颜色、昵称、语言、隐藏 element 规则已落到实现。 |
| 02 | `specs/02-tui-menu-and-preview-spec.md` | In Progress | Python TUI 已稳定；Ink 已接通菜单/预览原型，但仍存在 canonical UI model、availability gating、菜单契约对齐等切换阻塞项。 |
| 03 | `specs/03-platform-detection-and-setup-spec.md` | In Progress | 自动探测与 `Setup` 兜底已实现；Ink 仍需真正遵守 `needs_setup -> Setup` 的公开契约。 |
| 04 | `specs/04-apply-restore-and-uninstall-spec.md` | In Progress | Python 主链已实现；Ink 已接通真实 `apply/restore`，但 `uninstall` 仍未接入，bridge 也仍依赖 Python TUI。 |
| 05 | `specs/05-install-and-distribution-spec.md` | In Progress | npm 安装已上线，但当前公开入口仍是 Python TUI，且运行时前提与 Ink 切换条件还需收口。 |

## Current Ink Cutover Blockers

- bridge 目前仍以 `BuddyHubTUI` 作为真实行为来源，而不是稳定 core/service 层
- bridge 的只读 `dump-*` 调用当前不是严格无副作用
- Ink 尚未完整接通 `Setup` 与 `Uninstall`
- Ink 颜色菜单尚未完整使用 canonical availability model
- npm 公开安装路径与当前实际入口、运行时前提仍存在偏差

## Status Definitions

- `Todo`: spec exists but implementation has not started
- `In Progress`: implementation exists, but scope or verification is not yet complete
- `Done`: implementation and verification evidence both exist for the current phase
