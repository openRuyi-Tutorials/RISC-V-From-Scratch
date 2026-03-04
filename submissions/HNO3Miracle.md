# HNO3Miracle 的试炼记录

## 基本信息

- GitHub ID: HNO3Miracle
- 联系邮箱: hno3miracle@example.com (需确认)
- rootfs 发布 Repo: https://github.com/HNO3Miracle/oerv-lfs

## Rootfs 资产

- 文件名: rootfs-riscv64-lfs-HNO3Miracle.tar.zst
- SHA256: e44a3fe2cbc2190325ca6ab79657345fa6633740a15ddbbe17f0af3eb2a1521c (ext4 镜像 SHA256)

## 如何从 rootfs 运行起来

### 解压发布包

首先，解压下载的压缩包并进入 release 目录：

```bash
tar -I zstd -xvf rootfs-riscv64-lfs-HNO3Miracle.tar.zst
cd release
```

### 方式 1: 使用 QEMU 系统模式

1. 运行脚本 `./run-qemu.sh`。
2. 系统将启动并自动运行 systemd，在出现 `login:` 提示符时输入 `root` 即可直接免密进入 shell。

## neofetch 证据

![neofetch](https://lg.hno3.top/lfs.png)

```
/\_/\          root@oerv-lfs
 =( °w° )=     -------------
   )   (  //   OS: Linux 6.6.10 riscv64
  (__ __)//    Host: riscv-virtio,qemu
   Acid OS     Kernel: 6.6.10
               Uptime: 1 min
               Shell: bash 5.2.21
               Memory: 46MiB / 1976MiB
```

## 这是如何锻造的（LFS 过程简述）

- 参考的教程/版本: RISC-V-From-Scratch / CLFS 
- 关键配置: 
    - 架构: riscv64-unknown-linux-gnu
    - C 库: glibc 2.40
    - 初始化系统: systemd 255
    - 编译器: GCC 13.2.0
    - 包管理器: pacman 6.0.2 (基于 OpenSSL 3.0.13, libarchive 3.7.2, curl 8.6.0， 未全部实现)
- 与“原教旨 LFS”的偏离:
    - **Merged /usr**: 采用了现代 Linux 的合并 /usr 架构。
    - **Multi-arch Path Compatibility**: 针对 RISC-V 64 位 Glibc 默认搜索 `/lib64/lp64d` 的特性，通过软链接实现了路径兼容。
    - **Systemd Optimization**: 禁用了 networkd 之外的大部分重量级组件，以缩短启动时间和减少依赖。

## 你踩过的坑

- **交叉编译器引导**: 解决了 Pass 1 阶段 GCC 与 C 库之间的循环依赖。
- **动态链接器加载失败**: 发现 `ld-linux` 强制要求多架构路径。通过在 `rootfs` 中建立 `lib64/lp64d` 软链接解决了 `systemd` 无法加载 `libssp.so.0` 的问题。
- **首次启动交互**: `systemd-firstboot` 会在缺失 `machine-id` 时阻塞启动。通过预置 `machine-id` 和 `os-release` 实现了系统的非交互式顺畅启动。
- **登录循环 (Login Loop)**: 由于 `util-linux` 编译时禁用了 `login` 且未安装 `shadow`，`agetty` 无法调用 `/bin/login` 导致闪退和无限重启。在 `rootfs` 中添加了一个简单的伪 `login` 脚本 (`exec /bin/bash -l`) 实现了免密直接启动 shell。

## 已知问题 / TODO（如有）

- [x] 完成 Stage 1: 交叉工具链
- [x] 完成 Stage 2: 临时系统
- [x] 完成 Stage 3: 最终系统构建
- [x] 配置 systemd 非交互引导
- [x] 修复 login 程序缺失导致的无限重启
- [ ]  pacman 无法下载需要证书的包，目前暂时也无法获取包

## 安全声明

- 我确认 rootfs 不包含任何密钥/Token/SSH Key/凭据/私人数据。
