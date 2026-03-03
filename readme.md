# 🎉 欢迎来到 RISC-V 新手村！

> 🏰 **恭喜你迈出了成为系统工程师的第一步！**
> 
> 这里是通往 **目标发行版** 的第一道门槛，也是一段精彩技术旅程的起点。
>
> ⚠️ **代码示例声明**：本文所有命令与脚本片段均为实例，仅用于演示思路与流程。请根据你的发行版、权限模型、目录布局和版本差异自行调整，并先在隔离环境验证。
>
> ✍️ **文档署名**：本文档由 **Avrova Donz** 借助 **ChatGPT 5.3** 完成。

---

## 🌟 目标与主线

本项目目标是完成可运行的 `riscv64` LFS 系统并提交合规卷轴。  
新人统一按 `glibc + systemd` 主线执行；完成后即可对齐目标发行版开发基线。

> ✅ **验收底线（必须满足）**：任意评审者拿到你的成品（Release 资产）后，按照你卷轴中的步骤逐条执行，应能把系统跑起来并进入可用环境。

---

## 📘 什么是 LFS

<strong>LFS（Linux From Scratch）</strong>不是“装一个现成发行版”，而是你亲手把系统一层层搭起来：

- 工具链（binutils/GCC）怎么从无到有
- C 库（glibc）如何成为用户态程序运行基础
- 用户态基础组件（bash/coreutils/util-linux/systemd）如何组合成可用系统
- 内核与用户空间在启动路径上如何衔接

做完一次 LFS，你获得的是“系统级因果关系”认知：  
为什么某个二进制跑不起来、为什么启动会卡、为什么路径污染会导致后期灾难。

---

## 🧠 为什么用 RISC-V 做这件事

选择 RISC-V 不是为了“冷门”，而是因为它非常适合训练系统构建能力：

- **架构链路清晰**：从 OpenSBI 到内核再到 init，启动路径更容易被看清
- **交叉构建特征明显**：Host/Target 边界非常明确，能强制你建立正确的工具链思维
- **工程迁移价值高**：把 riscv64 的构建链路走通后，排障方法可以迁移到其他架构

---

## 🏁 挑战定位：构建 + 表达

`RISC-V-From-Scratch` 的本质是 **挑战与自我展示**：

- 先完成主线：`glibc + systemd` 可启动、可验证、可提交
- 再展示你的工程判断：你做了哪些取舍、优化和扩展，为什么这么做

所以我们鼓励在卷轴里增加“自由发挥 / 花活展示”章节，展示你的独立思考与实现能力。

---

## 📚 新手村地图

``` 
RISC-V-From-Scratch/
|- readme.md
|- ROADMAP.md
|- FAQ.md
|- CHECKLIST.md
|- README.zh-CN.md
|- submissions/
`- evidence/
```

> 卷轴模板以本页内嵌模板为主，同时保留 `README.zh-CN.md` 作为唯一独立模板文件。

### ⚡ 推荐阅读与执行顺序

| 顺序 | 文档/目录 | 作用 |
|------|-----------|------|
| 1 | [🗺️ ROADMAP.md](ROADMAP.md) | 先确认新人唯一主线要求（`glibc + systemd`） |
| 2 | `submissions/` | 看历史卷轴结构与排障思路，减少盲区 |
| 3 | 本页 (`readme.md`) | 按三段式方法论推进完整构建 |
| 4 | [❓ FAQ.md](FAQ.md) | 卡住时按症状定位问题并修复 |
| 5 | [✅ CHECKLIST.md](CHECKLIST.md) + 模板 | 提交前逐项核对，避免返工 |

---

## 🎮 试炼流程

### 第一阶段：准备 (预计 1-2 天)

1. **确认主线要求**（建议先读 [🗺️ ROADMAP.md](ROADMAP.md)）：新人按 `glibc + systemd` 执行（预计 3-5 天打通首轮）；历史提交中的其他技术栈仅供排障参考。

2. **了解目标**：阅读本文档，理解 LFS/CLFS 的基本概念

3. **搭建环境**：准备一台 x86_64 Linux 宿主机（虚拟机即可）

4. **学习前辈经验**：浏览 `submissions/` 目录，查看其他同学的提交，获取灵感和参考

### 第二阶段：构建 (预计 1-2 周)

按照下面的**三段式构建方法论**，亲手打造你的 riscv64 根文件系统：

| 阶段 | 任务 | 输出 | 环境 |
|------|------|------|------|
| **Stage 1** | 构建交叉编译器 | `riscv64-unknown-linux-gnu-gcc` | Host (x86_64) |
| **Stage 2** | 构建临时系统 | `${CLFS}/tools` 完整工具链 | Host + QEMU |
| **Stage 3** | 构建最终系统 | 可启动的 rootfs | Chroot / QEMU |

### 第三阶段：提交 (预计 1 天)

1. 将 rootfs 发布到你自己的 GitHub Releases
2. 按照模板撰写提交文档
3. 提交 PR 到本仓库

---

## 🏗️ 三段式构建核心方法论

### 1. 三元目录隔离（铁律）

任何偏离此结构的构建都将在后期引入路径污染与权限混乱：

```bash
${CLFS}/              # 最终目标系统根目录（riscv64 架构）
${CLFS}/cross-tools/  # Host 架构可执行文件（x86_64->riscv64 交叉编译器）
${CLFS}/tools/        # Target 架构可执行文件（riscv64，构建期间通过 QEMU 解释执行）
${CLFS}/sources/      # 源码与构建目录（必须在普通用户权限下操作）
```

**关键原则**：
- `cross-tools` 与 `tools` **绝对分离**
- 所有构建过程不得在 `${CLFS}` 外安装任何文件

### 2. 版本锁定矩阵（关键）

RISC-V 生态演进快速，必须预先验证以下兼容性：

| 组件 | 推荐版本 | 注意事项 |
|------|----------|----------|
| QEMU | ≥ 8.0 | 低版本无法正确处理 glibc 2.38+ 的 `clone3` |
| GCC | 13.x | 与 Binutils 版本需匹配 |
| Binutils | 2.42 | - |
| Linux Kernel | 6.6.x | 头文件版本不必与运行内核完全一致 |

### 3. 编译器构建三 passes（CLFS 正统）

**Pass 1: 最小化交叉编译器**（无 libc）
```bash
# Binutils（无依赖）
../binutils-2.42/configure \
  --prefix=${CLFS}/cross-tools \
  --target=${TARGET} \
  --with-sysroot=${CLFS} \
  --disable-nls --disable-werror

# GCC（仅 C 语言，无 libc）
../gcc-13.2.0/configure \
  --prefix=${CLFS}/cross-tools \
  --target=${TARGET} \
  --with-sysroot=${CLFS} \
  --enable-languages=c \
  --disable-shared \
  --disable-threads \
  --without-headers
```

**Pass 2: C 库安装**
- **glibc 路径**：先安装内核头文件，再构建 glibc，使用 Pass 1 GCC

**Pass 3: 完整交叉编译器**
重新构建 GCC，启用 `--enable-threads=posix` 与 `--enable-shared`

---

## 🚀 进入目标环境

### 方案 A：QEMU 用户态 + Chroot（推荐）

```bash
# 注册 QEMU 二进制解释器（需 root，一次性）
cp /usr/bin/qemu-riscv64-static ${CLFS}/usr/bin/

# Debian/Ubuntu（推荐）
sudo update-binfmts --enable qemu-riscv64

# systemd 发行版（可选）
# sudo systemctl restart systemd-binfmt

# Chroot 进入（需 root）
sudo chroot "${CLFS}" /usr/bin/env -i \
  HOME=/root TERM=${TERM} PS1='(riscv64) \u:\w\$ ' \
  PATH=/tools/bin:/bin:/usr/bin \
  /tools/bin/bash --login
```

### 方案 B：Initramfs + QEMU 系统模式

当 QEMU 用户态不可行时，采用两阶段启动：

```bash
# 打包 cpio
find . | cpio -o -H newc | zstd > ../initramfs.cpio.zst

# 系统模式启动
qemu-system-riscv64 \
  -machine virt \
  -m 512M \
  -bios default \
  -kernel Image \
  -initrd initramfs.cpio.zst \
  -append "init=/bin/sh" \
  -nographic
```

---

## ⚠️ RISC-V 架构特化要点

### 页大小

RISC-V 支持 4KB/16KB/64KB 页大小，但用户态软件常硬编码 4KB 假设：

```bash
# 强制使用 4KB 页
# 内核配置: CONFIG_PAGE_SIZE_4KB=y
# glibc 构建: libc_cv_pagesize=4096
```

### 启动流程

```
OpenSBI (M-mode) -> Linux Kernel (S-mode) -> init (U-mode)
```

**无需构建 EDK2/UEFI**，QEMU `-bios default` 已提供 OpenSBI。

### 压缩指令集（RVC）

确保工具链与内核均启用 RVC 支持（默认）：
- GCC: `--with-arch=rv64gc`
- 内核: `CONFIG_RISCV_ISA_C=y`

---

## 🎨 Init 系统基线

新人统一使用 **systemd**（主线基线，复杂度高）。  
执行建议：先完成“可启动 + 可关机/重启 + 基础服务可管理”的最小闭环，再做功能扩展。

---

## ✅ 阶段性验证节点

### Node 1：工具链完整性
```bash
echo '#include <stdio.h>
int main(void) { printf("Hello %s\\n", "RISC-V"); return 0; }' | \
  ${TARGET}-gcc -x c - -o /tmp/test -static && \
  file /tmp/test  # 应显示静态链接的 riscv64 可执行文件
```

### Node 2：Chroot 环境
```bash
chroot "${CLFS}" /tools/bin/bash -c "gcc --version"
```

### Node 3：系统启动
```bash
qemu-system-riscv64 ... -append "init=/bin/sh"  # 单用户模式验证
```

### Node 4：服务管理
验证 `reboot` 与 `poweroff` 能正确触发内核关机。

---

## 🐛 常见故障速查

更多问题请查阅 [❓ FAQ.md](FAQ.md)，包含 20+ 个问题的详细解答。

| 故障 | 根因 | 修复 |
|------|------|------|
| **VFS: unable to mount root** | 缺少 `CONFIG_VIRTIO_BLK=y` | 检查 `dmesg \| grep virtio` |
| **Exec format error** | qemu-riscv64-static 未复制或 binfmt 未注册 | 验证复制和注册步骤 |
| **not found** (文件存在) | 动态链接器路径错误 | `readelf -l \| grep interpreter` |
| **内核启动后崩溃** | 设备树不匹配或缺少串口配置 | 添加 `earlycon=sbi` |

### 常见陷阱速查

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| **systemd 进入 emergency mode** | 启动后停在救援模式 | 检查 `root=`、`/etc/fstab` 与 `systemctl --failed` |
| **QEMU + glibc 2.42** | 程序运行崩溃 | 升级 QEMU 或使用打补丁的版本 |
| **chroot 黑屏** | 进入后无提示符 | chroot 前必须先安装 bash！ |
| **util-linux 安装报错** | `chgrp: Operation not permitted` | 检查必要工具是否存在，可忽略此错误 |

---

## 📋 提交规范

### 文件命名

| 文件 | 命名格式 | 示例 |
|------|----------|------|
| 提交卷轴 | `<githubid>.md` | `donz2026.md` |
| rootfs 包 | `rootfs-riscv64-lfs-<githubid>.tar.zst` | `rootfs-riscv64-lfs-donz2026.tar.zst` |
| 截图 | `fastfetch.png` / `neofetch.png` | `fastfetch.png` |

### 卷轴必须包含

1. ✅ 基本信息（GitHub ID、邮箱、Release 链接）
2. ✅ Rootfs SHA256 校验值
3. ✅ "如何运行"详细步骤
4. ✅ LFS 构建过程简述
5. ✅ 踩坑记录
6. ✅ 安全声明

### 验收底线（必须）

- 卷轴中的“如何运行”必须具备可复现性：评审者不能依赖你本地私有状态也能跑通。
- 前置条件必须写清楚（例如：QEMU 版本、宿主机依赖、镜像/内核来源、必要参数）。
- 步骤执行后至少应达到：系统可启动并进入可用 shell（以及你声明的验证动作可执行）。

### 推荐加分项（自由发挥 / 花活）

- 🔥 你做了什么额外工程动作（优化、自动化、可观测性、加固等）
- 🧠 为什么这么做（目标、取舍、风险）
- 📏 结果如何（体积/启动时间/稳定性/可维护性上的变化）

### 花活怎么写更有说服力（推荐结构）

按下面 4 段写，评审最容易看懂：

1. **目标**：你要解决什么具体问题（慢、臃肿、不稳定、难复现等）
2. **实现**：你改了什么（配置、脚本、流程、参数）
3. **验证**：怎么证明有效（命令输出、日志片段、前后对比）
4. **边界**：风险与回滚方式（失败如何恢复到主线可用状态）

### 可选花活方向（示例）

- 构建自动化：一键脚本、分阶段脚本、失败重试
- 体积优化：裁剪包、精简符号、移除非必要组件
- 启动优化：定位慢启动点，给出前后时间对比
- 可靠性增强：加入健康检查、关键服务守护策略
- 可观测性：启动日志采集、排障命令集、最小诊断工具箱
- 安全加固：最小权限、敏感文件扫描、构建产物审计

### 常见误区（尽量避免）

- 只写“我优化了很多”，没有可复现步骤或证据
- 只贴结果截图，没有解释为何这样设计
- 花活破坏主线可用性（不能启动、不能登录、不能关机）

### 🧾 Scroll Template（卷轴模板）

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

## 📎 拓展资源

想深入学习？这些资源会助你一臂之力：

- **[CLFS 项目](https://trac.clfs.org/)** - Cross Linux From Scratch 官方指南
- **[LFS 手册](https://linuxfromscratch.org/lfs/view/stable/)** - Linux From Scratch 权威文档
- **[RISC-V Machines](https://risc-v-machines.readthedocs.io/)** - RISC-V 虚拟化参考

---

## 💡 核心理念

> **阶段隔离与验证密度**

严格区分 `cross-tools`、`tools` 与最终系统，并在工具链完成、chroot 进入、系统启动三个节点做硬性验证，避免错误扩散到后期集成阶段。

---
