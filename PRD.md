# BuddyHub PRD

- Status: Draft v0.2
- Date: 2026-04-04
- Repository: `verycafe/buddyhub`
- Document owner: `verycafe`

## 1. 产品一句话

BuddyHub 是一个面向 Claude Code 的反应式 Buddy 插件。

它安装后会以低干扰的文本 UI 显示 Buddy 状态，并根据 Claude Code 的工作状态切换文案；同时它必须支持开启、关闭、安全卸载，并且不能影响用户正常使用 Claude Code。

## 2. 背景

Claude Code 已公开支持：

- plugins
- plugin marketplaces
- hooks
- status line
- MCP

但目前没有公开、稳定的官方 Buddy API 可供第三方直接复用。

这意味着 BuddyHub 的第一版不应该押注于“嵌入 Claude Code 内部原生 Buddy UI”，而应该基于已公开能力做一个稳定、可安装、可关闭、可卸载的 Buddy 系统。

## 3. 问题定义

对于 Claude Code 用户，当前存在三个现实缺口：

1. Claude 的工作状态虽然存在，但不够可视化。  
用户知道 Claude 在“干活”，但很难一眼看出它当前是在思考、读文件、改代码、跑命令，还是在等待输入。

2. 陪伴式体验缺少可控边界。  
很多“桌宠式”工具看起来有趣，但容易侵入主工作流、难以关闭、难以卸载，或者对主程序稳定性产生影响。

3. 插件化产品常常忽略生命周期管理。  
安装只是第一步。一个真正可用的 Buddy 产品必须同时解决：
- 如何开启
- 如何临时关闭
- 如何恢复
- 如何彻底清理卸载
- 如何保证 Claude Code 本体始终可正常工作

## 4. 产品目标

### 4.1 核心目标

1. 用户可以通过 Claude Code 的官方插件分发机制安装 BuddyHub。
2. 安装后用户可以通过状态栏和命令看到一个状态驱动的 Buddy 文本层。
3. BuddyHub 必须支持显式开启和关闭。
4. BuddyHub 必须支持安全、一键式卸载路径。
5. BuddyHub 不能阻塞、破坏或显著拖慢 Claude Code 的正常工作。
6. 第一版尽量不依赖远程服务，默认本地优先。

### 4.2 非目标

- 不在 V1 里依赖未公开的官方 Buddy 内部接口。
- 不在 V1 里做多人协作、团队共享、云同步。
- 不在 V1 里做复杂游戏化体系或皮肤商城。
- 不在 V1 里要求用户使用 tmux。
- 不在 V1 里强依赖 MCP 才能完成核心 Buddy 展示。

## 5. 产品原则

### 5.1 非侵入

BuddyHub 是 Claude Code 的侧边能力，不是主工作流接管者。

要求：

- 不占用正文主区域
- 不阻挡输入区
- 默认低干扰
- 所有自动化行为都可理解、可关闭

### 5.2 失败可退化

BuddyHub 的任何异常都不能影响 Claude Code 主体使用。

要求：

- 文本 UI 或状态栏输出异常时 Claude Code 仍能正常工作
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

## 6. 目标用户

### 6.1 主要用户

- 高频使用 Claude Code 的个人开发者
- 希望获得“Claude 正在做什么”的即时反馈的用户
- 喜欢轻量陪伴式体验，但讨厌复杂配置和侵入性工具的用户

### 6.2 用户诉求

- “我想一眼看出 Claude 现在在干嘛。”
- “我希望它有 Buddy 感，但不要挡我工作。”
- “我想要能随时关掉，不影响 Claude 本体。”
- “如果不喜欢了，我希望可以彻底卸载，不留脏状态。”

## 7. 产品定义

BuddyHub V1 是一个 `状态驱动的 Claude Buddy 可视化插件`。

它由以下四层组成：

1. `安装层`
通过自建 marketplace 完成安装。

2. `状态层`
通过 Claude Code hooks 和本地运行信息感知 Claude 的当前工作状态。

3. `展示层`
通过 status line、状态命令和详情命令显示当前状态。

4. `控制层`
支持开启、关闭、恢复、状态查看和安全卸载。

## 8. V1 UI 定义

### 8.1 主 UI

V1 的主 UI 是 `TUI-first`。

定义如下：

- 主环境式 UI 为 Claude Code status line
- 主详情 UI 为 `/buddyhub:open`
- 主紧凑状态 UI 为 `/buddyhub:status`
- 不依赖任何独立窗口能力

### 8.2 默认显示内容

默认显示：

- Buddy 名称
- 当前状态
- 当前项目名（如可用）

例如：

- `Buddy: Buddy | thinking | buddyhub`
- `Buddy: Buddy | waiting`

### 8.3 详情视图

`/buddyhub:open` 打开详细文本视图。

V1 详情视图至少包含：

- Buddy 名称
- 当前状态
- 最近一次状态变更时间
- 当前项目信息
- 当前是否启用
- 快捷操作入口

V1 可以先不做完整属性面板，但要为后续 Buddy 属性展示预留位置。

### 8.4 可选状态栏同步

V1 支持可选的 Claude Code status line 同步。

目的：

- 让 Buddy 在不同终端产品里保持一致的低干扰可见性
- 作为最稳定的 ambient UI 存在

### 8.6 明确不做

V1 不承诺：

- 把 Buddy 直接嵌入 Claude Code 的原生内部 UI 插槽
- 接管 Claude Code 的正文布局
- 修改 Claude Code 的核心渲染逻辑

## 9. 状态模型

### 9.1 BuddyHub 生命周期状态

BuddyHub 本身应有独立生命周期：

- `installed`
- `enabled`
- `paused`
- `disabled`
- `error`
- `uninstalled`

其中：

- `enabled`：Buddy 运行中
- `paused`：已安装但暂停自动更新或显示
- `disabled`：用户显式关闭，Buddy 不主动运行
- `error`：BuddyHub 自身异常，但 Claude Code 继续正常工作

### 9.2 Claude 工作状态

V1 的 Buddy 可视状态至少包含：

- `idle`
- `thinking`
- `reading`
- `coding`
- `running`
- `browsing`
- `waiting`
- `done`
- `error`

这些状态来自对 Claude Code 公开 hook 事件和本地运行信号的映射。

### 9.3 显示规则

- 默认优先显示 Claude 当前工作状态
- 如果 BuddyHub 被暂停或禁用，UI 显示为 `paused` 或不显示
- 如果 status line 未接入，用户仍可通过 `/buddyhub:status` 和 `/buddyhub:open` 获取完整状态

## 10. 安装、启用、关闭、卸载

### 10.1 安装目标体验

目标安装路径：

```text
/plugin marketplace add verycafe/buddyhub
/plugin install buddyhub@buddyhub
```

安装完成后，BuddyHub 进入 `installed + enabled` 或 `installed + paused` 的可预测状态，不能出现“装完不知道有没有生效”的体验。

### 10.2 启用

BuddyHub 必须支持用户显式启用。

启用后的要求：

- 状态监测开始生效
- status line 同步可按配置启用
- `/buddyhub:status` 和 `/buddyhub:open` 可立即使用

### 10.3 关闭

BuddyHub 必须支持用户显式关闭。

关闭后的要求：

- 自动状态更新停止
- Claude Code 主体行为保持不变
- 用户无需卸载插件也可恢复“纯净使用”

关闭应优先理解为“停用 BuddyHub 的运行能力”，而不是破坏安装结构。

### 10.4 一键安全卸载

BuddyHub 必须支持清晰、低风险的一键卸载路径。

卸载后的要求：

- 清理 BuddyHub 写入的状态文件和缓存
- 移除 BuddyHub 注册的 hooks、status line 或相关配置引用
- 不破坏用户原有 Claude Code 配置
- 不留下必须手工排查的残余状态

如果平台层卸载与数据清理分为两个动作，产品必须提供清晰的一步式用户体验说明，而不是让用户自己找文件。

### 10.5 恢复

用户关闭 BuddyHub 后，必须可以低成本重新启用，而不需要重新安装。

## 11. 安全与非干扰要求

这是 V1 的硬性要求。

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

V1 不应在 hook 路径中执行高成本网络调用。

### 11.3 TUI 显示安全要求

BuddyHub 的显示层必须是文本优先、可失败退化的。

要求：

- status line 未配置时，命令界面仍可完整使用
- 任一文本命令失败不影响 Claude Code 主流程
- 不使用终端专属图形协议作为 V1 前置条件

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

## 12. 技术方案要求

### 12.1 分发

采用 Claude Code 官方支持的自建 marketplace 分发：

- 仓库根目录放 `.claude-plugin/marketplace.json`
- 插件主体放在 `plugins/buddyhub/`
- 用户通过 marketplace 安装

### 12.2 核心组成

V1 的最小可行组成：

- plugin commands 或 skills
- hooks
- 本地状态文件
- 可选 status line 脚本
- 详细文本状态视图

### 12.3 不依赖 tmux

V1 不以 tmux 为基础设施前提。

如果后续支持 tmux，必须是兼容项，而不是前置条件。

### 12.4 关于 MCP

MCP 不是 V1 Buddy 展示的前置条件。

V1 可以不使用 MCP，或只在后续增强版中引入 MCP 用于：

- 结构化记忆
- 工具扩展
- 更多命令能力

## 13. 命令设计方向

V1 命令设计应围绕“查看状态”和“控制生命周期”。

建议命令：

- `/buddyhub:help`
- `/buddyhub:status`
- `/buddyhub:pause`
- `/buddyhub:resume`
- `/buddyhub:open`
- `/buddyhub:doctor`

说明：

- `help`：展示命令和说明
- `status`：展示 Buddy 当前状态、启用状态和关键配置
- `pause`：暂停 BuddyHub 自动运行
- `resume`：恢复 BuddyHub 自动运行
- `open`：打开 Buddy 详细文本视图
- `doctor`：检查运行状态、配置和常见问题

卸载可以是产品级操作，但在 PRD 阶段不假定具体命令名，避免写入未验证的平台 API。

## 14. MVP 范围

### 14.1 必须包含

- 自建 marketplace 分发
- 可安装 BuddyHub 插件
- 状态驱动的文本 UI
- `/buddyhub:status` 紧凑状态视图
- `/buddyhub:open` 详细文本视图
- 可选 status line 同步
- 启用能力
- 关闭能力
- 清晰的安全卸载路径
- 非侵入运行保证
- 文档化的数据路径和配置路径

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
3. Buddy 以低干扰方式更新显示
4. 用户需要时点击查看详情

### 15.3 用户临时关闭

1. 用户执行暂停或关闭动作
2. Buddy 立即停止显示或停止更新
3. Claude Code 使用体验恢复为无 Buddy 状态

### 15.4 用户恢复使用

1. 用户执行恢复动作
2. BuddyHub 重新开始状态同步和显示

### 15.5 用户卸载

1. 用户执行官方或产品提供的卸载入口
2. BuddyHub 停止所有运行组件
3. BuddyHub 清理自身状态
4. Claude Code 保持可正常使用

## 16. 成功指标

### 16.1 产品指标

- 用户可在 5 分钟内完成安装并看到 Buddy
- 用户可在 30 秒内找到关闭 Buddy 的方式
- 用户可在 30 秒内找到恢复 Buddy 的方式
- 用户可在一次明确流程内完成卸载

### 16.2 稳定性指标

- BuddyHub 异常时，Claude Code 仍可正常使用
- 状态切换可稳定工作
- 文本 UI 不形成明显资源占用问题
- hooks 不引入可感知阻塞

## 17. 风险与约束

### 17.1 平台约束

- 公开文档没有确认第三方插件可向 Claude Code 内部主 UI 注入任意自定义组件
- 因此 V1 不应承诺“嵌入式原生 Buddy”

### 17.2 产品风险

- 如果 Buddy 太活跃，会打扰用户
- 如果关闭路径不够明确，用户会失去信任
- 如果卸载不干净，产品会被视为不安全

### 17.3 工程风险

- hooks 设计不当可能拖慢主流程
- 文本输出设计不当可能造成体验噪音
- 配置写入不谨慎可能污染用户 Claude 设置

## 18. 验收标准

V1 完成时，必须满足以下条件：

1. 用户可通过 Claude Code 插件分发路径完成安装。
2. 安装后用户能看到可工作的 Buddy 文本状态层。
3. 用户可以显式关闭 BuddyHub。
4. 用户可以显式重新开启 BuddyHub。
5. 用户有明确、低风险的卸载路径。
6. BuddyHub 异常时，Claude Code 仍可正常使用。
7. 文档清楚说明数据、配置、关闭和卸载。
8. 产品不要求 tmux、远程服务器或云账户才能完成核心展示功能。

## 19. 参考依据

本 PRD 主要基于以下资料整理：

- Claude Code 插件与 marketplace 相关官方文档
- Claude Code hooks 相关官方文档
- Claude Code status line 相关官方文档
- 本地 `~/.claude/pet` 原型运行证据
- 仓库内研究资料：
  - [Claude Code Buddy Notes](/Users/tvwoo/Projects/buddyhub/research/claude-code-buddy.md)
  - [Recon Reference Notes](/Users/tvwoo/Projects/buddyhub/research/recon-reference.md)
