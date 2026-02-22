# Leetfs 的试炼记录

## 基本信息

- GitHub ID: Leetfs
- 联系邮箱: <lee@mtftm.com>
- rootfs 发布 Repo: <https://github.com/Leetfs/lfs-riscv>

## Rootfs 资产

- 文件名: rootfs-riscv64-lfs-Leetfs.tar.zst
- SHA256: 02954b0b4f17ca061b9f65fd796aa17fd05000e42c974971396b68d16f6608f9

## 如何从 rootfs 运行起来

> 我们直接下载 rootfs 镜像~

```bash
wget https://github.com/Leetfs/lfs-riscv/releases/download/lfs-riscv/lfs-musl-riscv64.img

qemu-system-riscv64 \
    -machine virt \
    -m 512M \
    -smp 2 \
    -bios /usr/lib/riscv64-linux-gnu/opensbi/generic/fw_jump.bin \
    -kernel /mnt/lfs-riscv/sources/linux-6.6.10/arch/riscv/boot/Image \
    -drive file=/mnt/lfs-riscv/lfs-musl-riscv64.img,format=raw,if=virtio \
    -append "root=/dev/vda rw console=ttyS0 init=/init rootwait" \
    -nographic
```

启动啦！

## fastfetch 证据

![fastfetch 证据](../evidence/Leetfs/fastfetch.png)

## 这是如何锻造的 (LFS 过程简述)

- 参考的教程/版本: [Linux From Scratch - Version r12.4-97-systemd](https://linuxfromscratch.org/lfs/view/systemd/)，Donz的文档，前人的PR/blog
- 关键配置: gcc version 13.2.0 (GCC), Linux kernel 6.6.10, libc：musl, busybox-1.36.1

## 踩过的坑

- 运行镜像时报错：Kernel panic: VFS unable to mount root

确认 `root=/dev/vda` 和 `CONFIG_VIRTIO_BLK=y` 都无问题，排查发现是运行时错误的使用 `-hda` 挂载文件系统，`-hda` 是一个历史兼容参数，会被转换为`-drive if=ide`，但 riscv virt 没 ide，就会报错卡住。

解决方案：改为 `-drive if=virtio`

## 安全声明

- 我确认 rootfs 不包含任何密钥/Token/SSH Key/凭据/私人数据。
