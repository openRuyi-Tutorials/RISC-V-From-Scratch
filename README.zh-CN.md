# 📜 卷轴模板（中文）

> 本文件是独立模板入口；完整规则与说明以 `readme.md` 为准。  
> 验收底线：任意评审者拿到你的 Release 资产后，按卷轴步骤逐条执行，必须能把系统跑起来并进入可用环境。

将下面模板复制到 `submissions/<githubid>.md` 后按实际情况填写：

```md
# <githubid> 的试炼记录

## 基本信息

- GitHub ID: <githubid>
- 联系邮箱: <email>
- rootfs 发布 Repo: https://github.com/<you>/<repo>

## Rootfs 资产

- 文件名: rootfs-riscv64-lfs-<githubid>.tar.zst
- SHA256: <sha256>

## 如何从 rootfs 运行起来

> 目标：从“下载 rootfs”到“进入环境并跑起 fastfetch/neofetch”的最短步骤。
> 验收底线：任何人下载你的 Release 资产后，按本节步骤执行，必须能跑起来。

### 方式 1

1. ...

<!-- 可选区 -->

## fastfetch / neofetch 证据

<!-- 此处插入截图（可选） -->

## 这是如何锻造的（LFS 过程简述）

- 参考的教程/版本:
- 关键配置（toolchain / glibc / 内核 / systemd / 包策略等）:
- 与“原教旨 LFS”的偏离（如有）:

## 你踩过的坑

- 坑 1: ...
- 坑 2: ...

## 已知问题 / TODO（如有）

- ...

## 自由发挥 / 花活展示（可选但强烈推荐）

- 我额外做了什么：
- 这样做的动机与取舍：
- 关键实现（配置/脚本/命令）：
- 如何复现与验证（建议附命令）：
- 结果对比（如体积、启动时间、稳定性）：
- 风险与回滚方式（失败时如何恢复主线）：

## 安全声明

- 我确认 rootfs 不包含任何密钥/Token/SSH Key/凭据/私人数据。
```
