# PRD Index

BuddyHub product docs are now versioned.

## Current Version

Use the active development docs in:

- [V0.2/PRD.md](/Users/tvwoo/Projects/buddyhub/V0.2/PRD.md)
- [V0.2/specs/README.md](/Users/tvwoo/Projects/buddyhub/V0.2/specs/README.md)
- [V0.2/SPEC-STATUS.md](/Users/tvwoo/Projects/buddyhub/V0.2/SPEC-STATUS.md)

## Archive

The pre-versioned snapshot is preserved in:

- [V0.1/PRD.md](/Users/tvwoo/Projects/buddyhub/V0.1/PRD.md)
- [V0.1/specs/README.md](/Users/tvwoo/Projects/buddyhub/V0.1/specs/README.md)

## Rule

Current development should read and update `V0.2/` documents.

### 9.1 身份字段

BuddyHub 只允许使用真实来源字段。

当前已确认可作为真实来源的字段：

- `name`
- `species`

当前未确认稳定来源的字段：

- `rarity`
- `shiny`
- `hat`
- `eye`
- `stats`

规则：

- 未确认字段不得伪造
- reverse-engineered schema 只能作为研究参考，不能直接当用户真实值写入产品面

### 9.2 元素模型

视觉增强应尽量采用“附加元素”模型，而不是改 Buddy 主体。

V1 的元素设计应采用统一槽位：

- `top`
  - 帽子
  - 书本
  - 光环
- `front`
  - 咖啡杯
- `face`
  - 眼镜
- `side`
  - 键盘
  - 小道具
- `label`
  - 昵称显示

每个元素必须定义：

- 适用槽位
- 对齐锚点
- 是否适合所有物种
- 是否遮挡主体
- 是否需要颜色

### 9.3 颜色模型

BuddyHub 应提供一组离散颜色预设，而不是任意自由拾色。

V1 预设色包括：

- 橙色
- 粉色
- 蓝色
- 绿色
- 红色
- 黑色
- 白色
- 紫色

颜色只应用于已验证可补丁的视觉槽位。

当前已验证：

- `green` 作为当前默认绿色可在当前 `2.1.92 + blob` 目标上保留生效
- `orange` 可在当前 `2.1.92 + blob` 目标上通过原生 color-token patch 生效
- `blue` 可在当前 `2.1.92 + blob` 目标上通过已验证的 success RGB patch 生效
- `pink` 可在当前 `2.1.92 + blob` 目标上通过已验证的 success RGB patch 生效
- `purple` 可在当前 `2.1.92 + blob` 目标上通过已验证的 success RGB patch 生效
- `red` 可在当前 `2.1.92 + blob` 目标上通过已验证的 success RGB patch 生效
- `black` 可在当前 `2.1.92 + blob` 目标上通过已验证的 success RGB patch 生效

当前仍未验证：

- 白色

### 9.4 昵称模型

昵称不是替换用户真实 Buddy name。

当前已验证实现是：

- BuddyHub 通过 `~/.claude.json` 中的 `companion.name` 修改右下角官方 Buddy 的显示名
- BuddyHub 在 apply 前必须备份该配置，并在 restore 时恢复原名

规则：

- BuddyHub 必须明确显示当前运行时原名与用户保存的昵称
- BuddyHub 不得在没有备份和恢复链的情况下修改显示名
- 其他平台或安装类型在没有验证前不得宣称昵称已支持

## 10. 生命周期

BuddyHub 当前阶段的生命周期应围绕原生补丁来设计：

1. detect
2. load settings
3. backup
4. patch
5. verify
6. prompt restart
7. restore
8. uninstall

### 10.1 Detect

必须识别：

- 当前平台
- 当前 Claude Code 安装类型
- 当前 Claude Code 版本
- 当前目标文件路径
- 当前 Buddy identity
- 当前可用 patch profile

### 10.2 Load Settings

必须加载用户当前选择的：

- 元素
- 颜色
- 昵称

### 10.3 Backup

应用任何补丁前，必须先备份原始目标文件。

### 10.4 Patch

补丁必须：

- 版本敏感
- 模式敏感
- 最小化
- 仅修改目标元素或目标文本槽位

### 10.5 Verify

补丁后必须验证：

- 文件仍可运行
- Claude Code 可启动
- 预期补丁已经进入目标文件

如果当前阶段无法自动验证最终视觉，应明确要求用户重启后人工确认。

### 10.6 Prompt Restart

apply 完成后必须明确提示：

- 当前运行中的 Claude Code 不会热加载该补丁
- 需要重启 Claude Code 才能正式看到右下角 Buddy 的变化

### 10.7 Restore

恢复路径必须简单明确：

- 恢复原始文件
- 重新验证 Claude Code 正常启动

## 11. 成功标准

当前阶段产品成功，至少满足：

1. 用户安装 BuddyHub 后，当前选择配置会被自动 apply。
2. 用户被明确提示需要重启 Claude Code。
3. 用户可以通过设置入口选择元素和颜色。
4. BuddyHub 只增强官方 Buddy，不新增第二套 Buddy。
5. 用户可以恢复原始视觉。
6. 昵称能力只有在验证可实现时才暴露为正式功能。

## 12. 当前阶段验收标准

1. BuddyHub 能识别当前 Claude Code 安装和当前 Buddy。
2. BuddyHub 能对官方 Buddy 应用统一附加元素，而不是只做单物种专用修改。
3. BuddyHub 能应用至少一组颜色预设。
4. BuddyHub 有设置入口，并可显示预览。
5. BuddyHub 安装或升级后会自动 apply 当前设置，并提示用户重启。
6. BuddyHub 能安全 restore。
