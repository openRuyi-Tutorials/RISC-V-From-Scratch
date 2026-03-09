# 🗺️ 新手村主线执行指南

> 🎯 本指南以默认主线 **glibc + systemd** 为指导基线。
> 
> 新人默认目标：一次走通 `glibc + systemd` 基础系统，然后进入 RISC-V Linux 研发协作。
> 
> 本项目为独立训练路径，与任何具体发行版解耦。
> 
> ⚠️ **代码示例声明**：本文所有命令与脚本片段均为实例，仅用于说明流程。请按你的环境做参数与路径修订。

---

## 🎯 主线总览

```
第一次尝试 LFS?
  |
  +--> 默认主线: glibc + systemd (预计 3-5 天)
          |
          +--> 完成后进入 RISC-V Linux 研发协作
```

说明：
- 新人先执行 `glibc + systemd` 默认主线，优先完成团队基线能力。
- 历史提交中的其他技术栈会保留，可用于排障与设计参考。
- `SysVinit` 路线仅作历史参考；当前 LFS 官方主线已放弃对 `SysVinit` 路线的支持。
- 若要走花活路线（如更换 libc 或 1 号进程），允许提交，但需写清与默认主线的差异、额外步骤、风险与回滚。

---

## 🏭 默认主线 (glibc + systemd)

**预计时间**：3-5 天  
**与 RISC-V Linux 工程实践关系**：直接相关，属于新人主线基线能力

### 主线适用对象

- 新加入项目、需要和团队基线一致的同学
- 想直接进入可协作、可维护的系统构建路径
- 后续要做 BLFS 扩展或包维护的同学

### 技术基线

| 特性 | 说明 |
|------|------|
| **C 库** | glibc 2.40+ |
| **Init** | systemd |
| **用户态** | GNU coreutils + bash + util-linux |
| **复杂度** | ⭐⭐⭐⭐ 很高 |
| **定位** | 新人默认主线 |

### 关键步骤

```bash
# Stage 1: 构建交叉编译器（无 libc）
# - binutils
# - GCC（最小化，仅 C 语言）

# Stage 2: 构建基础系统
# - Linux 头文件
# - glibc（完整 C 库）
# - GCC（完整版，支持 C++、线程）

# Stage 3: 构建用户态与启动系统
# - bash / coreutils / util-linux
# - systemd

# Stage 4: 启动与服务验证
# - 串口登录
# - reboot / poweroff
```

### 主线检查点（提交前）

- [ ] GCC 三阶段构建完成
- [ ] glibc 动态链接器存在（`ld-linux-riscv64*.so.1`）
- [ ] chroot 环境可进入并执行基础命令
- [ ] systemd 基础配置完成
- [ ] 系统可启动到登录提示
- [ ] `reboot` / `poweroff` 行为正常

---

## 📚 参考案例

- `submissions/purofle.md`
- `submissions/AvrovaDonz2026.md`
- `submissions/Jvlegod.md`
- 其他历史提交可参考其排障思路与文档结构；新人仍应先按默认主线完成首轮闭环。

---

## 🎯 最终建议

新人直接按 `glibc + systemd` 完成一次从工具链到可启动系统的全流程；
完成后再做 BLFS 扩展与性能/体积优化。
