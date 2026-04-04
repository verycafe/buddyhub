# BuddyHub PRD

- Status: Draft v0.4
- Date: 2026-04-05
- Repository: `verycafe/buddyhub`
- Document owner: `verycafe`

## 1. 产品一句话

BuddyHub 是一个面向 Claude Code 官方 Buddy 的原生视觉增强项目。

它的目标只有一个：

- 在不替换、不伪造用户当前 Buddy 的前提下，增强 Claude Code 右下角官方 Buddy 的视觉元素

它当前明确不做：

- Claude 工作状态驱动
- 自定义平行 Buddy
- 文字面板型“伪 Buddy UI”

## 2. 当前事实

当前已经确认：

1. 用户真正关心的是 Claude Code 右下角已经存在的官方 Buddy。
2. `~/.claude` 是用户配置、plugin、transcript 目录，不是官方 Buddy 视觉表的已确认存放位置。
3. 当前 macOS 机器上，Claude Code 主二进制位于：
   - `/Users/tvwoo/.local/share/claude/versions/2.1.92`
4. 官方 Buddy 视觉表不是单独的外部 sprite 文件，而是嵌在 Claude Code 主二进制内部。
5. 在工作区里的 Claude 二进制副本上，只改 Buddy 原生视觉表，就能让右下角官方 Buddy 的元素变化。
6. 这条路径当前证明的是：
   - 官方 Buddy 的视觉元素可被原生修改
   - 但路径、实现和补丁方式都属于内部实现细节，不是公开稳定 API

## 3. 问题定义

当前问题不是“怎么显示一个 Buddy”，而是：

1. 如何只增强用户当前的官方 Buddy，而不是做第二套 UI。
2. 如何只改视觉元素，不把产品重新定义成状态同步工具。
3. 如何在不破坏 Claude Code 正常使用的前提下，安全地修改和恢复原生 Buddy 视觉。

## 4. 产品目标

### 4.1 核心目标

1. BuddyHub 只以 Claude Code 右下角官方 Buddy 为目标对象。
2. BuddyHub 只专注于官方 Buddy 的视觉元素增强。
3. BuddyHub 必须保留用户当前 Buddy 身份，不得替换成 BuddyHub 自己定义的宠物。
4. BuddyHub 必须支持安全备份、应用、恢复和卸载。
5. BuddyHub 不能让 Claude Code 变得不可启动、不可恢复或难以回滚。

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

### 5.2 只改视觉元素

BuddyHub 当前阶段只处理：

- 帽子
- 顶部元素
- 眼睛样式
- 物种对应帧
- 其他官方 Buddy 已存在或可补丁扩展的视觉元素

BuddyHub 当前阶段不处理：

- Claude 工作状态
- reaction
- 内部动态状态机

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

## 6. 目标用户

主要用户是：

- 已经在用 Claude Code 官方 Buddy 的用户
- 想增强官方 Buddy 外观的用户
- 不接受“再来一只新宠物”的用户
- 希望修改可恢复、可回退的用户

## 7. 产品定义

BuddyHub 当前阶段是一个 `官方 Buddy 原生视觉增强工具链`。

它由五层组成：

1. `识别层`
定位当前系统上的 Claude Code 安装与版本。

2. `身份层`
读取用户当前 Buddy 的真实身份字段，至少包括已验证的 `name/species`。

3. `原生视觉层`
定位 Claude Code 主二进制里的官方 Buddy 视觉表，并对目标元素做最小修改。

4. `备份恢复层`
保证所有修改都可备份、恢复、验证和回滚。

5. `诊断层`
只用于确认：
- 当前 Buddy 身份
- 当前安装路径
- 当前版本
- 当前 patch 是否生效

诊断层不是产品本体。

## 8. UI 定义

### 8.1 主 UI

BuddyHub 的主 UI 只有一个：

- Claude Code 右下角官方 Buddy

### 8.2 本阶段允许的增强

本阶段允许的增强包括：

- 顶部帽子/饰物
- 物种轮廓小修饰
- 眼睛或面部元素变化
- 其他不改变 Buddy 身份的原生视觉元素

### 8.3 本阶段不算交付的内容

以下都不算主体验完成：

- `inspect / doctor / help` 这类诊断输出
- 任何 status line 或文字诊断信息
- 任何额外文字视图

这些最多只算诊断面。

## 9. 视觉与身份模型

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

### 9.2 视觉元素来源

当前已确认官方 Buddy 视觉元素存在于 Claude Code 主二进制内部。

当前 macOS 机器上的已确认目标文件：

- `/Users/tvwoo/.local/share/claude/versions/2.1.92`

但这是当前环境的内部实现细节，不是跨平台稳定接口。

## 10. 生命周期

BuddyHub 当前阶段的生命周期应围绕原生补丁来设计：

1. detect
2. backup
3. patch
4. verify
5. restore
6. uninstall

### 10.1 Detect

必须识别：

- 当前平台
- 当前 Claude Code 安装类型
- 当前 Claude Code 版本
- 当前目标文件路径

### 10.2 Backup

应用任何补丁前，必须先备份原始目标文件。

### 10.3 Patch

补丁必须：

- 版本敏感
- 模式敏感
- 最小化
- 仅修改目标元素

### 10.4 Verify

补丁后必须验证：

- 文件仍可运行
- Claude Code 可启动
- 官方 Buddy 视觉真的变化

### 10.5 Restore

恢复路径必须简单明确：

- 恢复原始文件
- 重新验证 Claude Code 正常启动

## 11. 安全要求

BuddyHub 必须满足：

1. 不盲改系统文件
2. 不在没有备份的情况下改动 Claude 二进制
3. 不在版本不匹配时强行应用补丁
4. 不覆盖用户无关配置
5. 不把 `~/.claude/pet` 误当成官方 Buddy 控制面
6. 不把实验性路径伪装成跨平台稳定方案

## 12. 当前技术判断

截至当前仓库状态：

- 官方 Buddy 视觉增强是可行的
- 当前已验证的可行路径是 `原生二进制视觉表补丁`
- `状态驱动 Buddy` 不是当前阶段目标
- `plugin + hooks + status line` 不是当前阶段主产品路线

## 13. MVP 定义

BuddyHub 当前阶段的 MVP 定义是：

1. 能识别当前用户的官方 Buddy 身份
2. 能定位当前安装中的 Claude Code 主二进制
3. 能安全备份原始文件
4. 能对一个已验证的官方 Buddy 视觉元素做最小补丁
5. 能验证右下角官方 Buddy 的视觉确实发生变化
6. 能恢复原始文件

只有满足以上 6 条，才算这个阶段的 MVP 成立。

## 14. 验收标准

### 14.1 必须满足

1. 改动发生在官方 Buddy 本体，而不是平行 UI。
2. Buddy 视觉增强不依赖自定义状态系统。
3. BuddyHub 不伪造用户 Buddy 身份。
4. 备份、应用、恢复路径完整。
5. Claude Code 在补丁后仍可正常启动。

### 14.2 不计入完成

以下不计入本阶段完成：

- 文字诊断页好不好看
- status line 有没有接上
- hooks 是否完善
- Claude 工作状态是否映射
- reaction 是否可控

## 15. 当前风险

1. 路径和目标文件可能随平台、版本、安装方式变化。
2. 原生补丁需要处理代码签名与平台安全限制。
3. 目标模式可能在新版本二进制里变化。
4. 公开官方资料没有把这条路径定义成稳定扩展接口。

因此 BuddyHub 这一阶段必须被视为：

- `native patch research and tooling`

而不是：

- `stable public plugin integration`
