# BuddyHub V0.2 Spec Status

- Last updated: 2026-04-05
- Rule: whenever one spec reaches a new milestone, update this file in the same change.

| Spec | File | Status | Notes |
| --- | --- | --- | --- |
| 01 | `specs/01-customization-model-spec.md` | Done | 当前颜色、昵称、语言、隐藏 element 规则已落到实现。 |
| 02 | `specs/02-tui-menu-and-preview-spec.md` | In Progress | Python TUI 已稳定；`DEV` 分支上的 Ink 原型现已接通真实状态读取、一级/二级菜单、昵称输入与即时预览。 |
| 03 | `specs/03-platform-detection-and-setup-spec.md` | In Progress | 自动探测与 `Setup` 兜底已实现，Linux/Windows 仍需更多真实环境验证。 |
| 04 | `specs/04-apply-restore-and-uninstall-spec.md` | In Progress | Python 主链已实现；`DEV` 分支 Ink 原型已通过 JSON bridge 接通真实 `apply/restore`，`uninstall` 仍未接入 Ink。 |
| 05 | `specs/05-install-and-distribution-spec.md` | In Progress | npm 安装已上线，其他分发方式当前不作为公开主路径。 |

## Status Definitions

- `Todo`: spec exists but implementation has not started
- `In Progress`: implementation exists, but scope or verification is not yet complete
- `Done`: implementation and verification evidence both exist for the current phase
