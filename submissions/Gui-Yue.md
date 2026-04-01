# Gui-Yue 的试炼记录

## 基本信息

- GitHub ID: Gui-Yue
- 联系邮箱: xiangwei.riscv@isrc.iscas.ac.cn
- rootfs 发布 Repo: https://github.com/Gui-Yue/RISC-V-From-Scratch

## Rootfs 资产

- 文件名: rootfs-riscv64-lfs-Gui-Yue.tar.zst
- SHA256: 8fc4ec0fe09a66d3fff9e0d76f7b4c86ee9095a49425f58847e58d0a4cee6ac3
- 内核文件: Image
- 内核 SHA256: 753fa1d09ed92cc6bd4238edb7f91a36c12460fcc73309ec6ac0c23634358d64

## 如何从 rootfs 运行起来

> 目标：从“下载 rootfs”到“进入环境并跑起 pfetch”的最短步骤。

### 前置条件

- 宿主机 Linux x86_64
- 已安装 `qemu-system-riscv64`、`zstd`、`cpio`、`gzip`

### 方式 1（initramfs 启动）

1. 下载资产（rootfs 与 Image）：

```bash
wget https://github.com/Gui-Yue/RISC-V-From-Scratch/releases/download/v1.0/rootfs-riscv64-lfs-Gui-Yue.tar.zst
wget https://github.com/Gui-Yue/RISC-V-From-Scratch/releases/download/v1.0/Image
```

2. 解包并生成 initramfs：

```bash
mkdir -p rootfs

# 解压 rootfs

tar -I zstd -xvf rootfs-riscv64-lfs-Gui-Yue.tar.zst -C rootfs

# 打包为 initramfs
(
  cd rootfs
  find . | cpio -o -H newc | gzip -9 > ../initramfs.cpio.gz
)
```

3. 启动 QEMU：

```bash
qemu-system-riscv64 \
  -machine virt \
  -m 512M \
  -bios default \
  -kernel Image \
  -initrd initramfs.cpio.gz \
  -append "console=ttyS0 rdinit=/init loglevel=4" \
  -nographic
```

4. 进入后执行：

```bash
/usr/bin/pfetch
uname -m
```

预期包含：
- `Arch: riscv64`
- 内核版本信息

## fastfetch / neofetch 证据

![pfetch 证据](../evidence/Gui-Yue/pfetch.png)

## 这是如何锻造的（LFS 过程简述）

- 参考的教程/版本:
  - 本仓库 `readme.md` / `ROADMAP.md` / `CHECKLIST.md`
  - Debian trixie `riscv64` 预编译包（`linux-image-6.12.73+deb13-riscv64`、`busybox-static`）
- 关键配置（toolchain / libc / 内核 / init / 包策略等）:
  - 内核: `6.12.73+deb13-riscv64`（提取 `vmlinux` 作为 `Image`）
  - 用户态: `busybox-static 1.37.0`
  - init: 自定义 `/init`（挂载 `/proc` `/sys` `/dev`，输出 `pfetch`）
  - rootfs: 最小 initramfs 结构，目标是快速完成可启动可验证闭环
- 若偏离默认 `glibc + systemd`，差异与风险:
  - 本次使用最小 BusyBox initramfs 路线，不含完整 systemd 用户态。
  - 优点：当天可复现、依赖少。
  - 风险：不等价于完整 `glibc + systemd` 主线能力，后续仍需补齐主线构建。

## 你踩过的坑

- 坑 1: 当前环境无法直接下载 GitHub Release 大对象（连接超时），改为 Debian 官方源拉取 `riscv64` 内核与 busybox 包。
- 坑 2: 宿主机不能直接创建真实设备节点，使用 `fakeroot + cpio` 生成包含 `/dev/console` 与 `/dev/null` 的 initramfs。

## 已知问题 / TODO（如有）

- 当前是最小系统，未包含完整 `glibc + systemd`、包管理和网络服务栈。
- 后续计划按主线补齐 `glibc + systemd` 版本 rootfs，并给出对比数据。

## 安全声明

- 我确认 rootfs 不包含任何密钥/Token/SSH Key/凭据/私人数据。
