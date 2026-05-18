# DGU: Dynamic Configuration-Guided Kernel Fuzzing

DGU is a Syzkaller-based prototype for configuration-sensitive Linux kernel fuzzing.  
It extends Syzkaller with dynamically generated pseudo-syscalls for Linux runtime configuration interfaces, such as parameters exposed through `/proc/sys` and `/sys`.

The goal of DGU is to help kernel fuzzing explore configuration-dependent kernel states that are hard to reach under default runtime settings.

## Overview

Modern Linux kernels expose thousands of writable runtime configuration interfaces.  
These interfaces can change kernel behavior at runtime and affect how later system calls execute. However, directly adding all configuration interfaces into the fuzzing space may significantly dilute normal syscall exploration.

DGU addresses this problem by organizing related configuration items into semantic clusters and enabling them during fuzzing in a coverage-guided manner. The system is built on top of Syzkaller and reuses its executor, corpus management, coverage feedback, and crash detection infrastructure.

## Key Features

- Extracts writable runtime configuration interfaces from `/proc/sys` and `/sys`.
- Converts configuration writes into Syzkaller-compatible pseudo-syscalls.
- Supports generated pseudo-syscalls such as `syz_proc_sys_generated_*`.
- Uses configuration clustering to reduce random and redundant configuration exploration.
- Enables finer-grained unit configuration calls during fuzzing based on runtime feedback.
- Preserves compatibility with the Syzkaller fuzzing workflow.
- Includes a bug list discovered during evaluation.

## Repository Structure

```text
.
├── syzkaller/              # Syzkaller-based fuzzing framework
├── sys/                    # Syzlang descriptions and generated syscall definitions
├── executor/               # Executor-side support for pseudo-syscalls
├── scripts/                # Helper scripts for extraction, generation, or experiment control
├── bugs/                   # Bug list and case studies
└── README.md
