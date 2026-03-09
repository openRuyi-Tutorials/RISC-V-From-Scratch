# ❓ 常见问题解答 (FAQ)

> 这里收集了历届试炼者遇到的典型问题及解决方案
> 
> 💡 **提示**：本文档基于 AvrovaDonz2026、Jvlegod、purofle 等同学的实际踩坑经验整理
> 
> 📌 **变量说明**：本文命令默认使用 `${CLFS}` 与 `${TARGET}`。若你使用不同变量名（如 `$LFS`），请按需替换。
> 
> 🎯 **主线说明**：新人统一按 `glibc + systemd` 执行；本文排障也以该主线为准。
>
> ⚠️ **代码示例声明**：本文所有命令与脚本片段均为实例，仅用于说明排障思路，不保证可直接在任意环境执行。
>
> ✍️ **文档署名**：本文档由 **Avrova Donz** 借助 **ChatGPT 5.3** 完成。

## 📑 目录

### [🔧 工具链构建问题](#toolchain)
- [A01: GCC 编译报错 "flex: not found" / "bison: not found"](#a01)
- [A02: GCC 编译报错 "cannot find cc1"](#a02)
- [A03: 程序提示 "not found" 但文件实际存在](#a03)
- [A04: configure 报错 "cannot guess build type"](#a04)

### [🚀 启动问题](#boot)
- [B01: VFS: unable to mount root fs](#b01)
- [B02: Chroot 后 "Exec format error"](#b02)
- [B03: 内核启动后黑屏/无输出](#b03)
- [B04: 程序运行崩溃 / 无法启动 shell](#b04)

### [⚙️ systemd 启动问题](#systemd-boot)
- [C01: systemd 启动后进入 emergency mode](#c01)
- [C02: chroot 环境执行 systemctl 报 “Failed to connect to bus”](#c02)
- [C03: 串口没有出现登录提示（无 getty）](#c03)

### [🔧 构建问题](#build)
- [D01: util-linux 安装报错 "chgrp: Operation not permitted"](#d01)
- [D02: 进入 chroot 后 "黑屏一片"](#d02)
- [D03: GCC Stage 2 构建后仍不支持 C++ 线程](#d03)

### [🔄 Initramfs/Rootfs 切换问题](#switching)
- [E01: pivot_root 失败](#e01)
- [E02: initramfs 到 rootfs 切换后服务无法启动](#e02)

### [🌐 网络配置问题](#network)
- [F01: QEMU 中网络不通](#f01)
- [F02: curl 访问 https 网站报错](#f02)

### [📋 提交相关问题](#submission)
- [G01: rootfs 文件应该多大？](#g01)
- [G02: 如何生成 SHA256？](#g02)

### [🧪 收尾检查](#final-checklist)
- [📌 最后排查清单](#final-checklist)
- [🧪 可靠性附录（主线流程）](#reliability-appendix)

---

<a id="toolchain"></a>
## 🔧 工具链构建问题

<a id="a01"></a>
### A01: GCC 编译报错 "flex: not found" / "bison: not found"

**症状**：
```
make: flex: Command not found
make: bc: Command not found
```

**原因**：缺少构建内核和 GCC 必需的工具。

**解决**：
```bash
# Ubuntu/Debian
sudo apt install flex bison bc

# Fedora
sudo dnf install flex bison bc
```

---

<a id="a02"></a>
### A02: GCC 编译报错 "cannot find cc1"

**症状**：
```
gcc: error trying to exec 'cc1': execvp: No such file or directory
```

**原因**：GCC 使用相对路径定位 cc1，交叉编译时路径解析失败。

**解决**：使用 `-B` 选项指定工具路径：
```bash
${TARGET}-gcc -B${CLFS}/cross-tools/libexec/gcc/${TARGET}/13.2.0/ ...
```

或在构建 GCC 时确保 `libexec` 目录结构正确。

---

<a id="a03"></a>
### A03: 程序提示 "not found" 但文件实际存在

**症状**：二进制文件存在，但执行时报 `not found` 或动态链接错误。  

**原因**：通常是动态链接器路径不正确，或目标 rootfs 中缺失对应解释器。  

**解决**：检查解释器并确认 glibc 链接器就位（注意命令执行上下文）：
```bash
# [Host] 在构建目录检查目标系统二进制
${TARGET}-readelf -l ${CLFS}/bin/ls | grep interpreter
ls ${CLFS}/lib/ld-linux-riscv64*.so.1

# [Guest] 在已启动目标系统内检查
readelf -l /bin/ls | grep interpreter
ls /lib/ld-linux-riscv64*.so.1
```

若解释器路径不一致，请按 `readelf` 输出修正 rootfs 内链接器位置。

---

<a id="a04"></a>
### A04: configure 报错 "cannot guess build type"

**症状**：
```
configure: error: cannot guess build type; you must specify one
```

**原因**：常见于 `config.guess/config.sub` 太旧，无法识别当前构建环境；或交叉编译参数里 `--build/--host` 填反。

**解决**：先更新 `config.guess/config.sub`，并确保 `--build` 是宿主机架构：
```bash
./configure \
  --build="$(gcc -dumpmachine)" \
  --host=riscv64-unknown-linux-gnu \
  ...
```

**参考**：purofle 在构建 Flex 时遇到

---

<a id="boot"></a>
## 🚀 启动问题

<a id="b01"></a>
### B01: VFS: unable to mount root fs

**症状**：
```
VFS: Cannot open root device "vda" or unknown-block(0,0): error -6
Please append a correct "root=" boot option
```

**原因**：
1. 内核缺少 VirtIO 块设备驱动
2. `root=` 参数与设备名不匹配

**解决**：
1. 确保内核配置包含：
   ```
   CONFIG_VIRTIO_BLK=y
   CONFIG_VIRTIO_PCI=y
   ```

2. 检查 QEMU 参数，确保设备名匹配：
   ```bash
   # virtio 设备对应 /dev/vda
   -drive file=lfs-riscv64.img,format=raw,id=hd0,if=none \
   -device virtio-blk-device,drive=hd0
   -append "root=/dev/vda rw"
   
   # 或使用 SCSI（对应 /dev/sda）
   -drive file=lfs-riscv64.img,format=raw,if=scsi
   -append "root=/dev/sda rw"
   ```

---

<a id="b02"></a>
### B02: Chroot 后 "Exec format error"

**症状**：
```bash
chroot "${CLFS}" /tools/bin/bash
# => exec format error
```

**原因**：
1. `qemu-riscv64-static` 未复制到 chroot 环境
2. binfmt_misc 未注册或注册失败

**解决**：
```bash
# 1. [Host] 复制 QEMU 解释器到目标 rootfs
cp /usr/bin/qemu-riscv64-static ${CLFS}/usr/bin/

# 2. [Host] 优先使用系统工具注册 binfmt（需要 root）
sudo update-binfmts --enable qemu-riscv64

# 3. 验证注册状态
cat /proc/sys/fs/binfmt_misc/qemu-riscv64 | head -n 3
```

**补充**：如果你的发行版使用 systemd-binfmt，可以：
```bash
# 检查服务状态
systemctl status systemd-binfmt.service

# 检查是否已注册
cat /proc/sys/fs/binfmt_misc/qemu-riscv64 | head -1
# 应显示: enabled
```

**参考**：purofle 的经验

---

<a id="b03"></a>
### B03: 内核启动后黑屏/无输出

**症状**：QEMU 启动后没有任何输出，或只有早期 printk。

**原因**：
1. 内核未启用串口控制台
2. 设备树与内核不匹配

**解决**：
```bash
# 1. 确保内核配置包含
CONFIG_SERIAL_8250=y
CONFIG_SERIAL_8250_CONSOLE=y
CONFIG_HVC_RISCV_SBI=y

# 2. 启动参数添加 earlycon
-append "earlycon=sbi console=ttyS0"

# 3. QEMU 参数确认
-nographic  # 或 -serial stdio
```

---

<a id="b04"></a>
### B04: 程序运行崩溃 / 无法启动 shell

**症状**：内核启动正常，但运行用户程序时崩溃或卡住。

**原因**：QEMU 版本与 glibc 版本不兼容。

**解决**：

**purofle 发现**：在部分版本组合下，glibc 2.42 需要 QEMU 提供 termios2 支持，否则程序可能崩溃。

```bash
# 检查 QEMU 版本
qemu-system-riscv64 --version

# 如果使用 glibc 2.42+，建议优先使用较新 QEMU（或使用包含 termios2 支持的补丁版本）
# 补丁地址:
# https://github.com/qemu/qemu/compare/v10.1.2...dramforever:qemu:add-termios2

# 临时解决：降级 glibc 到 2.40 或升级 QEMU
```

**参考**：purofle 的重要发现

---

<a id="systemd-boot"></a>
## ⚙️ systemd 启动问题

<a id="c01"></a>
### C01: systemd 启动后进入 emergency mode

**症状**：系统启动后进入 `emergency mode`，或提示挂载/依赖失败。  

**常见原因**：
1. `/etc/fstab` 设备项与实际块设备不一致
2. 内核参数 `root=` 指向错误设备
3. 根目录关键挂载点状态异常（`/proc`、`/sys`、`/dev`）

**排查与修复**：
```bash
# [Guest] 1) 查看失败单元
systemctl --failed

# [Guest] 2) 查看本次启动错误日志
journalctl -b -p err

# [Guest] 3) 核对设备与 fstab
lsblk -f
cat /etc/fstab

# [Guest] 4) 修复后重载配置并恢复默认目标
systemctl daemon-reload
systemctl default
```

可用 `systemctl is-system-running` 验证整体状态（`running` 为最佳，`degraded` 需继续查 failed unit）。

---

<a id="c02"></a>
### C02: chroot 环境执行 systemctl 报 “Failed to connect to bus”

**症状**：
```
System has not been booted with systemd as init system (PID 1). Can't operate.
Failed to connect to bus: Host is down
```

**原因**：chroot 中 PID 1 通常不是 systemd，这是预期行为。  

**正确做法**：
1. chroot 阶段只做文件与配置准备，不以 `systemctl` 成功为标准。  
2. 在 QEMU 正式启动后再验证 systemd 行为。  

```bash
# 在启动后的目标系统里执行
ps -p 1 -o comm=
systemctl status
systemctl list-units --type=service --state=running | head
```

`ps -p 1` 输出必须是 `systemd`，systemd 相关检查才有意义。

---

<a id="c03"></a>
### C03: 串口没有出现登录提示（无 getty）

**症状**：内核日志输出正常，但迟迟没有 `login:`。  

**常见原因**：
1. 内核参数缺少 `console=ttyS0`
2. `serial-getty@ttyS0.service` 未启用
3. 内核未启用串口控制台支持

**排查与修复**：
```bash
# [Guest] 1) 检查内核参数
cat /proc/cmdline

# [Guest] 2) 检查并启用串口 getty
systemctl status serial-getty@ttyS0.service
systemctl enable serial-getty@ttyS0.service
systemctl restart serial-getty@ttyS0.service
```

若仍失败，回查内核配置：`CONFIG_SERIAL_8250=y` 与 `CONFIG_SERIAL_8250_CONSOLE=y`。

---

<a id="build"></a>
## 🔧 构建问题

<a id="d01"></a>
### D01: util-linux 安装报错 "chgrp: Operation not permitted"

**症状**：
```
chgrp: changing group of '/mnt/lfs/usr/bin/wall': Operation not permitted
make[4]: *** [Makefile:18850: install-exec-hook-wall] Error 1
```

**原因**：安装脚本尝试修改文件组，但在某些环境下权限不足。

**解决**：

**Jvlegod 发现**：此错误不影响核心工具的安装，可以忽略。

```bash
# 检查必要工具是否已安装
ls -l ${CLFS}/bin/mount
ls -l ${CLFS}/sbin/agetty
ls -l ${CLFS}/usr/lib/libmount.so.1

# 如果都存在，说明安装已成功，可以忽略 chgrp 错误
```

**参考**：Jvlegod 的经验

---

<a id="d02"></a>
### D02: 进入 chroot 后 "黑屏一片"

**症状**：chroot 成功后，没有任何提示符或输出。

**原因**：没有安装可用 shell（通常是 `bash`），或 `/bin/sh` 未正确指向。

**解决**：

**Jvlegod 提醒**：必须在 chroot 前确保目标系统里至少有一个可用 shell（推荐 `bash`）。

```bash
# 先检查 shell 是否存在
test -x ${CLFS}/bin/bash || test -x ${CLFS}/bin/sh || echo "缺少 shell"

# 若已安装 bash，确保 /bin/sh 指向可用 shell
ln -sf bash ${CLFS}/bin/sh

# 不建议将 /bin/sh 指向非主线 shell 方案
```

---

<a id="d03"></a>
### D03: GCC Stage 2 构建后仍不支持 C++ 线程

**症状**：编译 C++ 程序时，`<thread>` 头文件找不到或链接失败。

**原因**：Stage 2 构建时未启用必要的库。

**解决**：

**Jvlegod 的 Stage 2 配置**：
```bash
../configure \
  --target=riscv64-unknown-linux-gnu \
  --prefix=${CLFS}/tools \
  --with-sysroot=${CLFS} \
  --disable-nls \
  --disable-multilib \
  --enable-languages=c,c++ \
  --enable-shared \
  --enable-threads=posix
```

其中最关键的是：
- `--enable-shared`
- `--enable-threads=posix`

---

<a id="switching"></a>
## 🔄 Initramfs/Rootfs 切换问题

<a id="e01"></a>
### E01: pivot_root 失败

**症状**：
```bash
pivot_root: Invalid argument
```

**原因**：
1. 新 root 不是挂载点
2. 旧 root 有繁忙的挂载点

**解决**：
```bash
# 正确流程：确保新 root 是一个挂载点
mount --bind ${NEW_ROOT} ${NEW_ROOT}
pivot_root ${NEW_ROOT} ${NEW_ROOT}/mnt
exec chroot . /bin/sh < /dev/console > /dev/console 2>&1
```

或使用 `switch_root`（常见于 util-linux / initramfs 工具集）：
```bash
# 在 initramfs 中
mount -t devtmpfs devtmpfs /dev
# ... 找到真实 root 并挂载到 /newroot ...
exec switch_root /newroot /sbin/init
```

---

<a id="e02"></a>
### E02: initramfs 到 rootfs 切换后服务无法启动

**症状**：切换后系统无法找到设备、网络不工作等。

**原因**：initramfs 中的设备节点、挂载信息未正确传递。

**解决**：
```bash
# 1. 确保 devtmpfs 已挂载
mount -t devtmpfs devtmpfs /dev

# 2. 转移关键挂载点
mount --move /dev /newroot/dev
mount --move /proc /newroot/proc
mount --move /sys /newroot/sys
```

---

<a id="network"></a>
## 🌐 网络配置问题

<a id="f01"></a>
### F01: QEMU 中网络不通

**症状**：无法 ping 通外网。

**解决**：

**purofle 的完整方案**：

```bash
# 1. [Host] 启动 QEMU 时添加网络设备
qemu-system-riscv64 \
    ... \
    -netdev user,id=net0,hostfwd=tcp::2222-:22 \
    -device virtio-net-device,netdev=net0

# 2. [Host] 确保内核支持 VirtIO_NET
CONFIG_VIRTIO_NET=y

# 3. [Guest] 配置网络（任选其一）
ip link set dev eth0 up
dhcpcd eth0
# 或静态地址（QEMU usernet 常见网段）
ip addr add 10.0.2.15/24 dev eth0
ip route add default via 10.0.2.2 dev eth0

# 4. [Guest] 配置 DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

---

<a id="f02"></a>
### F02: curl 访问 https 网站报错

**症状**：
```
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

**原因**：缺少 CA 根证书。

**解决**：

**purofle 建议**：先编译安装 `make-ca` 及其依赖。

```bash
# 参考 BLFS: https://linuxfromscratch.org/blfs/view/systemd/postlfs/make-ca.html
# 安装后更新证书
make-ca -g
```

---

<a id="submission"></a>
## 📋 提交相关问题

<a id="g01"></a>
### G01: rootfs 文件应该多大？

**建议大小**：
- **主线最小可用系统**（glibc + systemd）：~150-300MB
- **带常用用户态工具**：~300-600MB
- **包含开发/调试工具**：~600MB+

**实际数据**：
| 同学 | C库 | Init | 大小 |
|------|-----|------|------|
| AvrovaDonz2026 | musl | BusyBox + `/init` | ~2MB |
| Jvlegod | glibc | SysVinit | 未标注 |
| purofle | glibc | systemd | ~500MB+ |

> 说明：
> - 历史数据会保留，不因默认路线调整而删除。
> - 当前新人默认指导仍是 `glibc + systemd`。
> - `SysVinit` 仅作为历史完成记录保留；当前 LFS 官方主线已放弃对 `SysVinit` 路线的支持。
> - 若选择花活路线（例如切换 libc 或 1 号进程），可以提交，但请在卷轴中明确写清与默认主线的差异、额外步骤、风险与回滚。

**优化**：
```bash
#  strip 符号
find ${CLFS}/bin ${CLFS}/sbin ${CLFS}/usr/bin ${CLFS}/usr/sbin -type f \
  -exec ${TARGET}-strip --strip-unneeded {} + 2>/dev/null || true

# 删除静态库（如果不需要编译）
rm -rf ${CLFS}/usr/lib/*.a

# 使用 zstd 高压缩
tar -cf rootfs.tar -C ${CLFS} .
zstd -T0 --ultra -22 rootfs.tar
```

---

<a id="g02"></a>
### G02: 如何生成 SHA256？

```bash
# [Host] 先设置你的 GitHub ID
GITHUB_ID=your_github_id

# Linux
sha256sum rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst

# macOS
shasum -a 256 rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst
```

---

<a id="final-checklist"></a>
## 📌 最后排查清单

1. 先看 `readelf -l` 的解释器路径是否与 rootfs 一致。
2. 再看 `dmesg` 与启动参数，确认内核驱动和 `root=` 设备名匹配。
3. 对照 `submissions/` 的已成功案例，逐项比对差异。

---

<a id="reliability-appendix"></a>
## 🧪 可靠性附录（主线流程）

下面是一组可直接复用的“最小验证集”，用于确认 `glibc + systemd` 主线是否真的跑通。

### A. 启动链路最小验证

```bash
uname -m                       # 期望: riscv64
ps -p 1 -o comm=               # 期望: systemd
cat /proc/cmdline              # 期望包含: console=ttyS0 和正确 root=
```

### B. 链接器与动态库验证

```bash
readelf -l /bin/ls | grep interpreter
ls -l /lib/ld-linux-riscv64*.so.1
ldd /bin/ls
```

判定标准：
- `interpreter` 路径存在于 rootfs 中。
- `ldd /bin/ls` 不出现 `not found`。

### C. systemd 健康度验证

```bash
systemctl is-system-running
systemctl --failed
journalctl -b -p err --no-pager | tail -n 50
```

判定标准：
- `is-system-running` 为 `running` 或 `degraded`。
- 如为 `degraded`，`systemctl --failed` 必须可解释且可修复。

### D. 关键挂载点验证

```bash
findmnt / /proc /sys /dev
mount | grep -E ' on /(proc|sys|dev) '
```

判定标准：
- `/proc`、`/sys`、`/dev` 均已正确挂载。
- 不存在“只读导致服务初始化失败”的异常。

### E. 提交前快检（5 条）

```bash
# [Guest] 1) glibc 链接器检查
test -e /lib/ld-linux-riscv64-lp64d.so.1 && echo "glibc linker OK"

# [Guest] 2) PID 1 是否为 systemd
test "$(ps -p 1 -o comm=)" = "systemd" && echo "systemd PID1 OK"

# [Guest] 3) 失败单元计数
systemctl --failed --no-legend | wc -l

# [Host] 4) 产物哈希
GITHUB_ID=your_github_id
sha256sum rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst

# [Host] 5) 产物文件类型
file rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst
```
