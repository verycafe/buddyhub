# BuddyHub PRD

- Status: Draft v0.3
- Date: 2026-04-04
- Repository: `verycafe/buddyhub`
- Document owner: `verycafe`

## 1. 产品一句话

BuddyHub 是一个面向 Claude Code 的 Buddy 增强插件。

它的目标不是做一个平行的文字宠物，而是在不替换、不伪造用户当前 Claude Buddy 的前提下，增强 Claude Code 右下角官方 Buddy 的动态表现；同时它必须支持开启、关闭、安全卸载，并且不能影响用户正常使用 Claude Code。

## 2. 背景

Claude Code 已公开支持：

- plugins
- plugin marketplaces
- hooks
- status line
- MCP

但当前公开文档没有确认第三方插件可以直接控制官方 Buddy 的内部动态状态。

本地研究进一步确认：

- Claude Code 本体内部确实存在原生 Buddy 控制链路
- 本地 transcript 可读到真实 Buddy 身份字段 `name/species`
- 当前环境 `claude auth status --json` 已确认 `apiProvider = firstParty`
- 但目前还没有确认第三方插件可稳定写入官方 Buddy 的内部反应状态 `companionReaction`
- 官方 Buddy 的动态链路目前更像是 Claude Code 本体内部 `_S7 -> Oo_ -> setAppState(companionReaction)` 的原生流程

这意味着 BuddyHub 的真正目标仍然是“增强 Claude Code 内部原生 Buddy UI”，但在技术上必须先确认是否存在可用控制面；在此之前，任何文字视图都只能算诊断与研究工具，不能算产品完成。

## 3. 问题定义

对于 Claude Code 用户，当前存在三个现实缺口：

1. Claude 的工作状态虽然存在，但不够可视化。  
用户知道 Claude 在“干活”，但很难一眼看出它当前是在思考、读文件、改代码、跑命令，还是在等待输入。

2. 用户真正想增强的是右下角官方 Buddy。  
如果产品改成另一套平行宠物或文字面板，就会偏离目标。

3. 插件化产品常常忽略生命周期管理。  
一个真正可用的 Buddy 产品必须同时解决：
- 如何开启
- 如何临时关闭
- 如何恢复
- 如何彻底清理卸载
- 如何保证 Claude Code 本体始终可正常工作

## 4. 产品目标

### 4.1 核心目标

1. 用户可以通过 Claude Code 的官方插件分发机制安装 BuddyHub。
2. BuddyHub 的核心成功标准是增强 Claude Code 右下角官方 Buddy，而不是输出一套平行文字 Buddy。
3. BuddyHub 必须优先读取用户当前 Claude Buddy 的真实身份信息。
4. BuddyHub 必须支持显式开启和关闭。
5. BuddyHub 必须支持安全、一键式卸载路径。
6. BuddyHub 不能阻塞、破坏或显著拖慢 Claude Code 的正常工作。
7. 第一版尽量不依赖远程服务，默认本地优先。
8. BuddyHub 不得用自定义的通用 Buddy 替代用户当前 Claude Buddy。
9. 文字命令与状态栏只能作为诊断或辅助面，不得被当作产品本体。

### 4.2 非目标

- 不把并行文字面板重新定义成“Buddy 产品本体”。
- 不在 V1 里做多人协作、团队共享、云同步。
- 不在 V1 里做复杂游戏化体系或皮肤商城。
- 不在 V1 里要求用户使用 tmux。
- 不在 V1 里强依赖 MCP 才能完成核心 Buddy 展示。

## 5. 产品原则

### 5.1 非侵入

BuddyHub 是 Claude Code 的增强层，不是主工作流接管者。

要求：

- 不阻挡正文主区域
- 不阻挡输入区
- 默认低干扰
- 所有自动化行为都可理解、可关闭

### 5.2 失败可退化

BuddyHub 的任何异常都不能影响 Claude Code 主体使用。

要求：

- 诊断视图或状态栏异常时 Claude Code 仍能正常工作
- hooks 异常时应快速失败并退出
- 状态读取失败时回退为空状态，不阻塞会话
- 任何可选功能都要支持 fail-open

### 5.3 用户控制权优先

用户必须清楚知道：

- BuddyHub 是否启用
- 当前显示来自什么状态
- 如何暂停
- 如何恢复
- 如何卸载
- 数据保存在哪里

### 5.4 本地优先

V1 默认不要求：

- 远程账户
- 云数据库
- 独立服务器

### 5.5 Buddy 身份保真优先

BuddyHub 的核心对象是 `用户当前的 Claude Buddy`，不是 BuddyHub 自己定义的一只宠物。

要求：

- 必须优先读取用户当前 Buddy 的真实身份信息
- 增强应建立在真实 Buddy 之上，而不是替换成 BuddyHub 自定义形态
- 未验证的字段必须明确标记为 `unknown` 或 `unavailable`
- 不能把 reverse-engineered schema 当作当前用户真实值直接填充
- 不能用通用 ASCII 宠物骨架冒充用户 Buddy 的原始外形

### 5.6 核心体验不可被 MVP 偷换

BuddyHub 的核心体验是：

- 增强用户当前的官方 Claude Buddy

因此：

- MVP 可以砍外围功能
- 但不能把产品偷换成文字管理面板
- `/buddyhub:open` 或 `/buddyhub:status` 只能是辅助与诊断入口
- 如果官方 Buddy 没有被增强，产品就不能被视为完成

## 6. 目标用户

### 6.1 主要用户

- 高频使用 Claude Code 的个人开发者
- 喜欢 Claude Buddy，但希望它更有动态反馈的用户
- 希望获得轻量陪伴感，但讨厌侵入式工具的用户

### 6.2 用户诉求

- “我想增强的就是右下角那个官方 Buddy。”
- “我希望它能更明显地反映 Claude 在干什么。”
- “我不想看到另一套假的 Buddy UI。”
- “我想要能随时关掉，不影响 Claude 本体。”

## 7. 产品定义

BuddyHub 是一个 `以官方 Claude Buddy 为核心对象的增强插件`。

它由以下六层组成：

1. `安装层`
通过自建 marketplace 完成安装。

2. `状态层`
通过 Claude Code hooks 和本地运行信息感知 Claude 的当前工作状态。

3. `身份层`
读取用户当前 Claude Buddy 的真实身份信息，并记录字段来源与可信度。

4. `官方控制层`
负责找到并驱动 Claude Code 内部官方 Buddy 的可用控制面。

当前已知：

- 官方 Buddy 动态不是简单 transcript 字段
- 其原生控制依赖 Claude Code 内部 app state
- 目前尚未确认第三方插件能写入该 app state

5. `诊断层`
通过状态命令、详情命令和可选 status line 暴露调试与验证信息。

6. `控制层`
支持开启、关闭、恢复、状态查看和安全卸载。

## 8. UI 定义

### 8.1 主 UI

BuddyHub 的主 UI 目标是：

- Claude Code 右下角已经存在的官方 Buddy

定义如下：

- 主用户可见 Buddy 必须是官方原生 Buddy
- `/buddyhub:open` 与 `/buddyhub:status` 只作为诊断面
- status line 只作为可选辅助面
- 不依赖任何独立窗口能力

### 8.2 目标体验

目标体验应当是：

- 用户看向 Claude Code 右下角，就能看到官方 Buddy 的动态变化
- BuddyHub 的增强建立在真实 Buddy 身份之上
- 不出现第二套伪装成主产品的文字宠物

如果当前技术实现还做不到这一点：

- 文字视图只能标记为诊断层
- 不能把诊断层输出宣称为主体验
- 项目状态必须明确标记为“研究/实验阶段”，不能伪装成主目标已完成

### 8.3 诊断详情视图

`/buddyhub:open` 打开详细诊断视图。

它至少包含：

- 已验证的 Buddy 名称
- 已验证的 Buddy identity 字段及来源
- 当前状态
- 最近一次状态变更时间
- 当前项目信息
- 当前是否启用
- 当前官方控制面状态
- 快捷操作入口

规则：

- 如果只确认到 `name/species`，就只显示这两个字段
- 如果 `rarity/shiny/hat/eye/stats` 没有真实来源，就不能显示伪造值
- 通用状态图标可以存在，但必须被表述为 `BuddyHub 诊断提示`

### 8.4 可选状态栏同步

BuddyHub 支持可选的 Claude Code status line 同步。

目的：

- 暴露支持性诊断信息
- 在不同终端产品里保持一致的低干扰提示

它不是主 Buddy 体验。

## 9. 状态与身份模型

### 9.1 BuddyHub 生命周期状态

- `installed`
- `enabled`
- `paused`
- `disabled`
- `error`
- `uninstalled`

### 9.2 Claude 工作状态

当前整理的工作状态语义至少包括：

- `idle`
- `thinking`
- `reading`
- `coding`
- `running`
- `browsing`
- `waiting`
- `done`
- `error`

这些状态只有真正驱动到官方 Buddy 时，才算满足核心目标。

### 9.3 Buddy 身份字段

BuddyHub V1 必须区分：

- `工作状态字段`：由 hooks 和运行信号驱动
- `Buddy 身份字段`：由用户当前 Claude Buddy 的真实来源驱动

Buddy 身份字段示例：

- `name`
- `species`
- `rarity`
- `shiny`
- `hat`
- `eye`
- `stats`

规则：

- 只有存在真实来源的字段才能进入显示层
- reverse-engineered schema 只用于兼容性理解，不能直接作为用户值
- 字段必须记录来源，例如 transcript attachment、local runtime、reverse-engineered reference

## 10. 安装、启用、关闭、卸载

### 10.1 安装目标体验

目标安装路径：

```text
/plugin marketplace add verycafe/buddyhub
/plugin install buddyhub@buddyhub
```

安装完成后，BuddyHub 进入 `installed + enabled` 或 `installed + paused` 的可预测状态。

但产品完成标准不是“文字命令能跑”，而是“官方 Buddy 增强路径真实生效”。

### 10.2 启用

启用后的要求：

- 状态监测开始生效
- 诊断命令与可选 status line 可立即使用
- 如官方 Buddy 控制面已接通，原生 Buddy 增强应同时生效

### 10.3 关闭

关闭后的要求：

- 自动状态更新停止
- 官方 Buddy 增强立即停止
- Claude Code 主体行为保持不变

### 10.4 一键安全卸载

卸载后的要求：

- 清理 BuddyHub 写入的状态文件和缓存
- 移除 BuddyHub 注册的 hooks、status line 或相关配置引用
- 不破坏用户原有 Claude Code 配置
- 不留下必须手工排查的残余状态

### 10.5 恢复

用户关闭 BuddyHub 后，必须可以低成本重新启用，而不需要重新安装。

## 11. 安全与非干扰要求

### 11.1 不能影响 Claude Code 正常工作

BuddyHub 不能：

- 阻塞 Claude 响应
- 破坏 Claude 输入输出
- 修改 Claude 的核心行为逻辑
- 因自身异常导致 Claude 会话不可用

### 11.2 Hook 安全要求

所有 hooks 必须遵守：

- 快速执行
- 可失败退出
- 不因异常阻塞主流程
- 不做 V1 必需性之外的重型操作

### 11.3 诊断显示安全要求

BuddyHub 的诊断显示层必须是文本优先、可失败退化的。

要求：

- status line 未配置时，命令界面仍可完整使用
- 任一文本命令失败不影响 Claude Code 主流程
- 不使用终端专属图形协议作为前置条件

### 11.4 配置安全要求

BuddyHub 对 Claude 配置的修改必须：

- 可追踪
- 可逆
- 尽量命名空间隔离
- 避免覆盖用户已有自定义设置

### 11.5 数据安全要求

BuddyHub 必须清楚说明：

- 写入哪些本地文件
- 写入路径在哪里
- 哪些数据是缓存
- 哪些数据会在卸载时删除

BuddyHub 还必须区分：

- BuddyHub 自己写入的运行时数据
- Claude 自己拥有、BuddyHub 只读取的 Buddy 身份来源

BuddyHub 不能删除或篡改 Claude 自身的 Buddy 身份数据源。

## 12. 技术方案要求

### 12.1 分发

采用 Claude Code 官方支持的自建 marketplace 分发：

- 仓库根目录放 `.claude-plugin/marketplace.json`
- 插件主体放在 `plugins/buddyhub/`
- 用户通过 marketplace 安装

### 12.2 核心组成

当前最小可行组成：

- plugin commands 或 skills
- hooks
- Buddy identity reader
- 官方 Buddy 控制面适配层
- 本地状态文件
- 可选 status line 脚本
- 诊断视图

### 12.3 不依赖 tmux

如果后续支持 tmux，必须是兼容项，而不是前置条件。

### 12.4 关于 MCP

MCP 不是核心 Buddy 增强的前置条件。

## 13. 命令设计方向

命令设计应围绕“查看诊断状态”和“控制生命周期”。

建议命令：

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:open`
- `/buddyhub:doctor`

说明：

- `help`：展示命令和说明
- `status`：展示诊断状态、已验证身份字段、启用状态和关键配置
- `pause`：暂停 BuddyHub 自动运行
- `resume`：恢复 BuddyHub 自动运行
- `open`：打开详细诊断视图，并展示真实来源的 Buddy 字段与控制面状态
- `doctor`：检查运行状态、配置和常见问题

## 14. MVP 范围

### 14.1 必须包含

- 自建 marketplace 分发
- 可安装 BuddyHub 插件
- 面向官方 Buddy 的增强目标
- 用户当前 Buddy 身份读取
- `/buddyhub:status` 诊断视图
- `/buddyhub:open` 详细诊断视图
- 可选 status line 同步
- 启用能力
- 关闭能力
- 清晰的安全卸载路径
- 非侵入运行保证
- 文档化的数据路径和配置路径

补充说明：

- 如果官方 Buddy 增强控制面还未打通，MVP 仍处于研究/实验状态
- 文字诊断层不能单独算作产品完成

### 14.2 可以延后

- 复杂记忆系统
- MCP 工具能力
- 团队共享
- 云同步
- 游戏化成长系统
- 多 Buddy 管理

## 15. 用户流程

### 15.1 首次安装

1. 用户添加 marketplace
2. 用户安装 BuddyHub
3. 用户看到 BuddyHub 已成功启用或进入默认状态
4. 用户能立即理解如何暂停、恢复和卸载

### 15.2 正常使用

1. 用户打开 Claude Code
2. BuddyHub 读取 Claude 当前状态
3. 官方 Buddy 在右下角以更明显的动态方式更新显示
4. 用户需要时使用诊断命令查看细节

### 15.3 用户临时关闭

1. 用户执行暂停或关闭动作
2. 官方 Buddy 增强立即停止
3. Claude Code 使用体验恢复为无 BuddyHub 增强状态

### 15.4 用户恢复使用

1. 用户执行恢复动作
2. BuddyHub 重新开始状态同步和增强

### 15.5 用户卸载

1. 用户执行官方或产品提供的卸载入口
2. BuddyHub 停止所有运行组件
3. BuddyHub 清理自身状态
4. Claude Code 保持可正常使用

## 16. 成功指标

### 16.1 产品指标

- 用户可在 5 分钟内完成安装并看到官方 Buddy 增强生效
- 用户可在 30 秒内找到关闭 BuddyHub 的方式
- 用户可在 30 秒内找到恢复 BuddyHub 的方式
- 用户可在一次明确流程内完成卸载

### 16.2 稳定性指标

- BuddyHub 异常时，Claude Code 仍可正常使用
- 官方 Buddy 状态切换可稳定工作
- 诊断 UI 不形成明显资源占用问题
- hooks 不引入可感知阻塞

## 17. 风险与约束

### 17.1 平台约束

- 公开文档没有确认第三方插件可向 Claude Code 内部主 UI 写入官方 Buddy 的内部动态状态
- 当前主要技术问题不是“有没有 Buddy schema”，而是“有没有第三方可达的官方 Buddy 控制面”
- 当前本地研究还显示：即使 `apiProvider` 已是 `firstParty`，第三方插件仍未证明可达 `companionReaction` 写入路径

### 17.2 产品风险

- 如果把文字诊断层错当成产品本体，会直接偏离需求
- 如果 Buddy 太活跃，会打扰用户
- 如果关闭路径不够明确，用户会失去信任
- 如果卸载不干净，产品会被视为不安全

### 17.3 工程风险

- hooks 设计不当可能拖慢主流程
- 配置写入不谨慎可能污染用户 Claude 设置
- 如果官方控制面只能通过非公开内部路径访问，后续版本兼容性会有风险
