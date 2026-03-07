# corestudy 的试炼记录

## 基本信息

- GitHub ID: corestudy
- 联系邮箱: 2760018909@qq.com
- rootfs 发布 Repo: https://github.com/corestudy/RISC-V-From-Scratch


## Rootfs 资产

- 文件名: rootfs-riscv64-lfs-corestudy.tar.zst
- SHA256: 132ba5c1cbfc44b0d765cbc698928a0cbce57ca0ab1aba4bdaae0c442f8cb3fa  

## 如何从 rootfs 运行起来

> 目标：从“下载 rootfs”到“进入环境并跑起 fastfetch/neofetch”的最短步骤。
> 验收底线：任何人下载你的 Release 资产后，按本节步骤执行，必须能跑起来。

解压发布包
首先，解压下载的压缩包并进入 cls 目录：

tar -I zstd -xvf rootfs-riscv64-lfs-corestudy.tar.zst
cd cls


### 方式 1: 使用 QEMU 系统模式


运行脚本 ./start-qemu.sh。
系统将启动并自动运行 systemd，在出现 login: 提示符时输入 root 即可直接免密进入 shell。

<!-- 可选区 -->

## fastfetch 证据

<!-- 此处插入截图（可选） -->
![alt text](image.png)

## 这是如何锻造的（LFS 过程简述）

- 参考的教程/版本: RISC-V-From-Scratch / CLFS
- 关键配置（toolchain / glibc / 内核 / systemd / 包策略等）:
    glibc-2.39              
    bash-5.2.21                
    util-linux-2.39.3
    coreutils-9.4         
    grep-3.11            
    riscv64-cross.txt   
    binutils-2.42              
    sed-4.9
    gcc-13.2.0            
    linux-6.6.30         
    systemd-255

## 你踩过的坑

登陆时死循环：systemd的动态库错误，没有shadow。Systemd 能拉起了登录界面（agetty），但是无法调用底层的 /bin/login 程序。导致一直死循环。 \
为了实现root 免密登录，我写了一个脚本绕过/bin/login，让agetty直接调用root的bash

## 已知问题 / TODO（如有）

- ...


## 安全声明

- 我确认 rootfs 不包含任何密钥/Token/SSH Key/凭据/私人数据。