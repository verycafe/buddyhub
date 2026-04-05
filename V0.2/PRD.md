# BuddyHub PRD

- Status: Active v0.2
- Date: 2026-04-05
- Repository: `verycafe/buddyhub`
- Product owner: `verycafe`

## 1. 产品一句话

BuddyHub 是一个通过独立 TUI 菜单定制 Claude Code 官方 Buddy 的工具。

它当前只面向：

- 官方右下角 Buddy
- `/buddy` 卡片

它不会再把产品定义成：

- 插件命令页
- 文字 Buddy
- 外部平行宠物

## 2. 当前版本目标

V0.2 要解决的是：

1. 用户安装 `buddyhub` 后，可以直接进入一级菜单。
2. 用户可以在菜单里设置语言、颜色、昵称。
3. 菜单右侧会基于本机真实 Buddy 状态显示预览。
4. `Apply` 会安全修改官方 Buddy。
5. `Restore` 会安全恢复。
6. `Uninstall` 不要求用户再手动跑第二条卸载命令。

## 3. 当前范围

### 3.1 当前公开能力

- `Language`
- `Color`
- `Nickname`
- `Apply`
- `Restore`
- `Uninstall`
- `Quit`

### 3.2 当前隐藏能力

本阶段继续隐藏：

- `element` 切换

原因：

- 当前版本先把颜色、昵称、探测、预览、恢复、卸载这条主路径做稳
- element 逻辑虽然保留在底层，但不作为公开菜单项

## 4. 产品对象

BuddyHub 的产品对象始终是用户当前的官方 Claude Buddy。

这意味着：

- 名称修改要作用于官方 Buddy
- 颜色修改要作用于官方 Buddy
- `/buddy` 卡片要和右下角 Buddy 保持一致

## 5. 当前事实

当前已经确认：

1. 官方 Buddy 的真实视觉目标在 Claude Code 主二进制内。
2. Buddy 名称可通过 Claude runtime config 安全覆盖。
3. 颜色通过当前已验证的原生 patch 点生效。
4. 已运行中的 Claude Code 进程不会自动热更新这些改动。
5. 当前体验必须按“应用后重启 Claude Code 生效”设计。

## 6. 关键用户流程

### 6.1 安装

当前对外安装方式只保留：

```bash
npm install -g github:verycafe/buddyhub
```

安装完成后，用户直接输入：

```bash
buddyhub
```

进入一级菜单。

### 6.2 首次启动

BuddyHub 首次启动时应：

1. 尝试自动识别 Claude
2. 读取当前真实 Buddy 状态
3. 根据系统语言选择默认菜单语言
4. 如果探测不完整，则进入 `Setup`
5. 在 `Setup` 中引导用户填写路径

### 6.3 配置与生效

用户流程应是：

1. 进入 `Color` 或 `Nickname`
2. 在右侧看到实时预览
3. 返回主菜单
4. 选择 `Apply`
5. 收到重启 Claude Code 提示
6. 重启后在右下角 Buddy 和 `/buddy` 卡片看到正式效果

### 6.4 恢复与卸载

- `Restore` 必须恢复原始 Buddy 状态
- `Uninstall` 必须自动：
  - 先 restore
  - 清理 BuddyHub 数据
  - 清理旧插件痕迹
  - 安排 package manager 卸载

## 6.5 UI 架构迁移计划

V0.2 当前已经确认：

- Ink 更适合作为 BuddyHub 的最终菜单 UI
- 当前 Python patch/detection 核心已经有较高验证积累
- 因此不应在 V0.2 中同时重写 UI 和 patch 核心

当前计划是：

1. `DEV` 分支继续推进 Ink UI
2. Ink 逐步接管：
   - 一级菜单
   - 二级菜单
   - 昵称输入
   - 预览
   - `Apply`
   - `Restore`
   - `Setup`
3. Python 侧在当前阶段只保留：
   - `buddyhub_core.py`
   - 一个稳定 JSON bridge
4. 当前 Python `curses` TUI 进入冻结状态：
   - 只允许修兼容性或阻塞性问题
   - 不再继续作为未来产品主界面投入新的体验打磨
5. 在 Ink 菜单完整覆盖公开能力之前，不切换当前公开主入口
6. 是否彻底移除 Python 核心并重写为 Node，不属于当前 V0.2 决策范围

这意味着：

- V0.2 的目标是 `Ink 成为唯一公开 UI`
- 不是 `立即把全部 patch 核心改写成 Node`

## 7. 设计原则

### 7.1 真实 Buddy 优先

预览、apply、restore 都必须基于本机真实 Buddy 状态，不得用虚构默认宠物替代。

### 7.2 菜单优先，不是命令优先

当前控制面应是一级菜单和二级菜单。

用户不应该被要求记忆一串子命令。

### 7.3 探测优先，手填兜底

BuddyHub 应先自动识别路径。

只有识别不到时，才进入 `Setup` 引导用户填写。

### 7.4 当前范围收敛

V0.2 当前先把：

- 独立 TUI
- 自动探测
- 颜色
- 昵称
- 预览
- apply / restore / uninstall

做稳。

element 不在当前对外范围里。

### 7.5 迁移纯度原则

BuddyHub 的“纯粹化”优先级是：

1. 先统一公开 UI
2. 再考虑是否统一核心语言

因此当前优先级应是：

- 先让 `buddyhub` 进入 Ink 菜单
- 再考虑未来是否需要移除 Python bridge / Python core

不应该为了技术栈统一而在当前阶段同时重写已验证的 patch 核心。

## 8. 当前非目标

V0.2 明确不做：

- Claude 运行状态驱动
- hook 状态宠物
- 插件 slash command 设置页
- `/config` 设置面板作为主入口
- element 公开切换
- 自定义平行 Buddy

## 9. 验收标准

当以下条件成立时，V0.2 视为命中目标：

1. 用户可以通过 `npm` 安装后直接运行 `buddyhub`
2. 用户可以通过一级菜单进入语言、颜色、昵称相关二级流程
3. BuddyHub 可以先自动探测 Claude 路径，失败时再进入 `Setup`
4. 右侧预览基于本机真实 Buddy 状态
5. `Apply` 后重启 Claude Code，右下角 Buddy 与 `/buddy` 卡片表现一致
6. `Restore` 和 `Uninstall` 都不要求用户自己手工查内部文件
7. `DEV` 分支上的 Ink 迁移不改变当前已验证 patch 核心的安全行为
