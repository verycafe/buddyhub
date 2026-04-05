# BuddyHub PRD

- Status: Draft v0.5
- Date: 2026-04-05
- Repository: `verycafe/buddyhub`
- Document owner: `verycafe`

## 1. 产品一句话

BuddyHub 是一个面向 Claude Code 官方 Buddy 的原生视觉定制工具。

它的目标是：

- 在不替换用户当前 Buddy 的前提下，为右下角官方 Buddy 增加可配置的视觉元素
- 让用户可以通过设置入口配置元素、颜色和昵称
- 在安装或升级后自动应用当前配置，并明确提示用户重启 Claude Code 生效

它当前明确不做：

- Claude 工作状态驱动
- 自定义平行 Buddy
- 文字面板型“伪 Buddy UI”
- 把诊断命令当作产品主体验

## 2. 当前事实

当前已经确认：

1. 用户真正关心的是 Claude Code 右下角已经存在的官方 Buddy。
2. 官方 Buddy 的视觉渲染不在公开插件 API 里，而在 Claude Code 主二进制内部。
3. 当前 macOS 机器上，Claude Code 主二进制位于：
   - `/Users/tvwoo/.local/share/claude/versions/2.1.92`
4. 对主二进制副本做最小视觉补丁，能够改变右下角官方 Buddy 的原生视觉元素。
5. `~/.claude/pet` 不是当前产品的主控制路径。
6. 当前已稳定验证的真实 Buddy identity 来源是 transcript 中的 `companion_intro`，至少可读到：
   - `name`
   - `species`
7. 当前没有证据证明“已运行中的 Claude Code 进程”能热更新 Buddy 视觉；现阶段应按“补丁后重启生效”设计。

## 3. 问题定义

当前要解决的问题不是“再做一个 Buddy”，而是：

1. 如何只增强用户当前的官方 Buddy，而不是替换成 BuddyHub 自己的宠物。
2. 如何让增强是统一的“附加元素”，而不是只对某个物种做特例改形。
3. 如何让用户能通过设置入口配置元素、颜色、昵称并看到预览。
4. 如何在安装后自动应用当前配置，同时保持安全备份、恢复和卸载。

## 4. 产品目标

### 4.1 核心目标

1. BuddyHub 只以 Claude Code 右下角官方 Buddy 为目标对象。
2. BuddyHub 当前阶段只专注于官方 Buddy 的视觉元素增强和视觉定制。
3. BuddyHub 必须保留用户当前 Buddy 身份，不得把官方 Buddy 替换成 BuddyHub 自己定义的宠物。
4. BuddyHub 必须支持安全备份、应用、恢复和卸载。
5. BuddyHub 安装或升级后，应自动应用当前配置，并明确提示用户重启 Claude Code。
6. BuddyHub 必须提供一个设置入口，用于配置元素、颜色和昵称，并提供预览。

### 4.2 本阶段明确不做

- 不做 Claude 工作状态同步
- 不做 `thinking / coding / running` 之类的状态驱动 Buddy
- 不做 status line 作为产品主界面
- 不做 hooks 作为产品主线
- 不做平行文字 Buddy
- 不把诊断命令面板当作主交付物

## 5. 核心原则

### 5.1 官方 Buddy 优先

BuddyHub 的产品对象始终是：

- 用户当前的官方 Claude Buddy

不是：

- 自定义 ASCII 宠物
- 外部桌宠
- 文本替身 UI

### 5.2 只做附加式视觉增强

BuddyHub 当前阶段只处理：

- 顶部元素，例如帽子、发饰、光环、书本、咖啡杯、键盘等
- 面部附近的小型附加元素
- 不改变主体身份的颜色增强
- 不替换官方名字的昵称显示

BuddyHub 当前阶段不处理：

- Claude 工作状态
- reaction
- 内部动态状态机
- 重新定义 Buddy 物种主体

### 5.3 安全优先

任何原生修改都必须：

- 先备份
- 后应用
- 可恢复
- 可验证
- 可拒绝

如果版本不匹配、签名失败、模式不匹配或验证失败，BuddyHub 必须停止，而不是硬改。

### 5.4 不偷换核心体验

MVP 不能把产品偷换成：

- 文本状态工具
- 诊断工具
- status line 工具
- 插件命令集合

只有当右下角官方 Buddy 的视觉真的被增强时，产品才算命中主目标。

### 5.5 不伪造未验证能力

如果某项能力当前版本还没有确认可补丁实现，例如：

- 实时热预览
- 某个颜色槽位的安全 patch 点

BuddyHub 必须：

- 在设置页中明确标记为 unavailable 或 experimental
- 不能假装该能力已经成立

## 6. 目标用户

主要用户是：

- 已经在用 Claude Code 官方 Buddy 的用户
- 想增强官方 Buddy 外观的用户
- 不接受“再来一只新宠物”的用户
- 希望修改可恢复、可回退的用户

## 7. 产品定义

BuddyHub 当前阶段是一个 `官方 Buddy 原生视觉定制工具链`。

它由六层组成：

1. `识别层`
定位当前系统上的 Claude Code 安装与版本。

2. `身份层`
读取用户当前 Buddy 的真实身份字段，至少包括已验证的 `name/species`。

3. `定制模型层`
定义元素、颜色、昵称等用户可配置项。

4. `预览层`
向用户展示“应用后大致效果”的预览，但不得把未重启生效的结果谎称为已应用。

5. `原生补丁层`
把当前选中的视觉定制应用到 Claude Code 主二进制中的官方 Buddy 渲染表。

6. `备份恢复层`
保证所有修改都可备份、恢复、验证和回滚。

## 8. 用户体验定义

### 8.1 安装与首次生效

安装或升级后，BuddyHub 应：

1. 检测当前 Claude Code 安装
2. 识别用户当前 Buddy
3. 读取当前保存的设置
4. 自动 apply 当前配置
5. 明确提示用户重启 Claude Code 以看到正式生效结果

### 8.2 设置入口

BuddyHub 必须提供一个设置入口。

该入口至少应支持：

- 选择元素
- 选择颜色
- 设置昵称
- 查看预览
- 应用当前设置
- 恢复原始视觉

设置入口本身是控制面，不是产品主 UI。产品主 UI 仍然是右下角官方 Buddy。

### 8.3 预览定义

BuddyHub 必须提供预览能力，但当前阶段不得默认承诺“正在运行的 Claude Code 内即时热预览”。

V1 允许的预览方式包括：

- 基于补丁 profile 的静态预览
- 基于 rehearsal target 的预览
- 基于已知元素槽位生成的效果预览

V1 不允许：

- 把未重启的当前进程效果称为“已正式生效”

## 9. 定制模型

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
- 紫色

颜色只应用于已验证可补丁的视觉槽位。

当前已验证：

- `orange` 可在当前 `2.1.92 + blob` 目标上通过原生 color-token patch 生效

当前仍未验证：

- 粉色
- 蓝色
- 绿色
- 红色
- 黑色
- 紫色

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
