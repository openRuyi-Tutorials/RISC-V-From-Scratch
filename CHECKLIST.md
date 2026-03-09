# ✅ 通关检查清单

> 在提交 PR 之前，请逐项确认你已经完成以下要求
>
> ⚠️ **代码示例声明**：本清单中的命令均为实例，仅用于演示检查思路。执行前请先确认环境变量、文件名与目录路径符合你的实际情况。
>
> ✍️ **文档署名**：本文档由 **Avrova Donz** 借助 **ChatGPT 5.3** 完成。

---

## 🧭 0. 环境变量确认

执行清单前，先确认你当前 shell 里有以下变量：

```bash
export CLFS=${CLFS:-$HOME/clfs-riscv64}
export TARGET=${TARGET:-riscv64-unknown-linux-gnu}
export GITHUB_ID=${GITHUB_ID:-your_github_id}
echo "CLFS=${CLFS}"
echo "TARGET=${TARGET}"
echo "GITHUB_ID=${GITHUB_ID}"
```

---

## 📋 第一阶段：构建验证

### 工具链检查

- [ ] 交叉编译器 `${TARGET}-gcc` 可以生成 riscv64 可执行文件
  ```bash
  ${TARGET}-gcc -x c - -o /tmp/test - <<<'int main(){return 0;}'
  file /tmp/test  # 应显示: ELF 64-bit LSB executable, UCB RISC-V
  ```

- [ ] 交叉编译器支持 C++（如需要）
  ```bash
  ${TARGET}-g++ --version
  ```

- [ ] 工具链路径正确分离
  ```bash
  ls ${CLFS}/cross-tools/bin/  # x86_64 上运行的交叉工具
  ls ${CLFS}/tools/bin/        # riscv64 架构的工具（用于 chroot）
  ```

### 基础系统检查

- [ ] coreutils 已安装且可执行
  ```bash
  ${TARGET}-readelf -h ${CLFS}/bin/ls | grep Machine
  # 应显示: RISC-V
  ```

- [ ] C 库已正确安装
  ```bash
  # glibc
  ls ${CLFS}/lib/ld-linux-riscv64*.so.1
  ```

- [ ] 若目标是参与 RISC-V Linux 研发协作，已完成 glibc 关键链路
  ```bash
  test -e ${CLFS}/lib/ld-linux-riscv64-lp64d.so.1 && echo "glibc linker OK"
  test -x ${CLFS}/bin/bash && echo "bash OK"
  test -x ${CLFS}/usr/bin/rpm || echo "rpm 可在后续阶段补齐"
  ```

- [ ] 基本目录结构完整
  ```bash
  ls ${CLFS}/
  # 应有: bin boot dev etc home lib lib64 mnt opt proc root run sbin srv sys tmp usr var
  ```

---

## 🚀 第二阶段：启动验证

### QEMU 系统模式启动

- [ ] 可以使用 initramfs 启动
  ```bash
  qemu-system-riscv64 \
      -machine virt -m 512M -bios default \
      -kernel Image -initrd initramfs.cpio.zst \
      -append "init=/init console=ttyS0" -nographic
  # 应能看到登录提示或 shell
  ```

- [ ] 可以使用磁盘镜像启动
  ```bash
  qemu-system-riscv64 \
      -machine virt -m 512M -bios default \
      -kernel Image \
      -append "root=/dev/vda rw console=ttyS0" \
      -drive file=lfs-riscv64.img,format=raw,id=hd0,if=none \
      -device virtio-blk-device,drive=hd0 \
      -nographic
  # 应能挂载 rootfs 并启动 init
  ```

### 基本功能验证

- [ ] Shell 可以正常运行
  ```bash
  /bin/sh -c 'echo OK'  # 输出 OK
  ```

- [ ] 基本命令可用
  ```bash
  ls /bin | wc -l       # 有若干命令
  cat /proc/cpuinfo     # 能看到 CPU 信息
  uname -m              # 输出 riscv64
  ```

- [ ] 可以正常关机/重启
  ```bash
  reboot    # 或
  poweroff  # 应能正常触发内核关机，而非卡死
  ```

---

## 📦 第三阶段：打包验证

### 文件命名检查

- [ ] rootfs 文件名符合规范
  ```
  rootfs-riscv64-lfs-<你的GitHubID>.tar.zst
  # 示例: rootfs-riscv64-lfs-donz2026.tar.zst
  ```

- [ ] 提交文件名符合规范
  ```
  submissions/<你的GitHubID>.md
  # 示例: submissions/donz2026.md
  ```

### 内容完整性检查

- [ ] rootfs 包含必要的目录结构
  ```bash
  tar -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst | head -20
  # 应看到: bin/, dev/, etc/, lib/, usr/ 等
  ```

- [ ] 关键文件存在
  ```bash
  tar -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst | grep -E 'bin/sh|init'
  # 应有 /bin/sh 或 /init
  ```

- [ ] SHA256 校验值已计算
  ```bash
  sha256sum rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst
  # 记录这个值，需要写入提交文档
  ```

---

## 📝 第四阶段：文档检查

### 基本信息（必须）

- [ ] GitHub ID 正确
- [ ] 联系邮箱有效
- [ ] Rootfs Release 链接可访问
- [ ] SHA256 校验值正确

### 运行指南（必须）

- [ ] 提供了从下载到运行的完整步骤
- [ ] 命令可以复制粘贴执行
- [ ] 包含了启动 QEMU 的完整参数
- [ ] 说明了如何退出 QEMU（Ctrl+A X）
- [ ] 在干净环境按卷轴步骤完整演练过，确认可启动并进入可用 shell
- [ ] 已写清运行前置条件（QEMU 版本、宿主机依赖、内核/镜像来源）
- [ ] 步骤不依赖本机私有路径、历史缓存或未说明的本地文件

### 构建过程（推荐）

- [ ] 说明了参考的教程/版本
- [ ] 列出了关键组件版本（gcc/glibc/内核等）
- [ ] 说明了与 vanilla LFS 的差异
- [ ] 若偏离默认主线（`glibc + systemd`），已明确列出与默认主线的差异点与必要补充步骤

### 自由发挥 / 花活（推荐）

- [ ] 卷轴中有独立章节描述额外工程动作（优化/自动化/加固/可观测性等）
- [ ] 明确写出动机与取舍（为什么这么做，而不是只贴结果）
- [ ] 给出至少一项可验证证据（命令、配置片段或前后对比数据）
- [ ] 说明了复现步骤（他人按步骤可重复你的结果）
- [ ] 若更换 libc 或 1 号进程，已说明与默认 `glibc + systemd` 在启动、服务管理、排障方法上的差异
- [ ] 给出风险与回滚方案（保证主线可恢复）

### 安全声明（必须）

- [ ] 明确声明不包含密钥/Token/SSH Key
- [ ] 确认没有打包宿主机的敏感目录（`~/.ssh/`, `/etc/ssh/` 等）

---

## 🖼️ 第五阶段：截图验证

### 截图要求

- [ ] 截图来自 fastfetch/neofetch/pfetch 的输出
- [ ] 清晰显示 **riscv64** 架构信息
- [ ] 显示基本的系统信息（OS、Kernel、Uptime 等）
- [ ] 图片格式为 PNG
- [ ] 文件大小合理（< 1MB）

### 截图示例检查

截图中应包含以下信息：
- [ ] 架构: `riscv64` 或 `RISC-V`
- [ ] 操作系统名称（你的 LFS 系统名）
- [ ] 内核版本
- [ ] 主机名

---

## 🔒 第六阶段：安全检查

### 敏感文件检查

确保 rootfs 中**不包含**：

- [ ] SSH 私钥（`~/.ssh/id_*`）
- [ ] SSH 已知主机（`~/.ssh/known_hosts`）
- [ ] Git 凭证（`~/.git-credentials`）
- [ ] API Token/密钥（`~/.config/` 下的敏感文件）
- [ ] 云服务配置（`~/.aws/`, `~/.azure/` 等）
- [ ] 浏览器数据
- [ ] 历史记录文件（`.bash_history`, `.zsh_history`）

### 验证方法

```bash
# 检查 SSH 密钥
tar -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst | grep -E '\.ssh|id_rsa|id_ed25519'
# 应该没有输出

# 检查 home 目录
tar -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst | grep '/root/\.'
# 应该只有必要的配置文件

# 检查 etc/ssh
tar -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst | grep 'etc/ssh'
# 如果没有 SSH 服务，应该为空
```

---

## 🎯 最终检查

### GitHub Release 检查

- [ ] rootfs 已上传到 GitHub Releases
- [ ] Release 页面可以公开访问
- [ ] 文件名与提交文档中一致
- [ ] 可以正常下载

### PR 提交检查

- [ ] Fork 了本仓库
- [ ] 在 `submissions/` 目录添加了 `<githubid>.md`
- [ ] （可选）在 `evidence/<githubid>/` 目录添加了截图
- [ ] 提交信息清晰（如 "Add submission for <githubid>"）
- [ ] 只提交了必要的文件（没有提交 rootfs 二进制）

---

## 🏆 通关标准

全部检查项完成后，你的提交应该：

1. ✅ **可复现**：按照你的文档，其他人可以运行起你的 rootfs
2. ✅ **可验证**：截图证明这是 riscv64 架构运行的系统
3. ✅ **安全**：不包含任何敏感信息
4. ✅ **规范**：文件命名和格式符合要求

---

## 📝 提交前最后确认

```bash
# 1. 验证 rootfs 可以解压
tar --zstd -tf rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst > /dev/null && echo "OK"

# 2. 验证 SHA256
sha256sum rootfs-riscv64-lfs-${GITHUB_ID}.tar.zst

# 3. 检查提交文件
ls submissions/${GITHUB_ID}.md
git status  # 确认没有提交大文件

# 4. 验证 Markdown 格式
# （确保没有语法错误，标题层级正确）
```

---

祝你好运，试炼者！🎉
