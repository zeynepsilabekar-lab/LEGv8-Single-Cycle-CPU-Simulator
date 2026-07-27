# LEGv8 Single-Cycle CPU Simulator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![Architecture](https://img.shields.io/badge/Architecture-LEGv8%20%2F%20ARMv8-orange)

A cycle-accurate **LEGv8 (ARMv8 subset) Single-Cycle CPU Simulator** implemented in Python. 

This project simulates the complete execution life-cycle of a single-cycle datapath processor—including **Instruction Fetch (IF), Decode (ID), Execution (EX), Memory Access (MEM), and Write-Back (WB)** stages—handling control signals, ALU operations, register updates, and memory interaction within a single clock cycle per instruction.

---

## 🛠️ Supported Instruction Set

The CPU simulator implements key LEGv8 instruction formats:

| Format | Instructions | Description |
| :--- | :--- | :--- |
| **R-format** | `ADD`, `SUB` | Register-register arithmetic operations |
| **I-format** | `ADDI`, `SUBI` | Immediate arithmetic operations |
| **D-format** | `LDUR`, `STUR` | Memory load and store with sign-extended offsets |
| **CB-format** | `CBZ` | Conditional branch if register is zero |
| **B-format** | `B` | Unconditional branch |
| **Special** | `HALT` (`0x00000000`) | Terminate CPU execution loop |

---

## 🏛️ Datapath & Architecture Highlights

- **Single-Cycle Timing:** Every instruction completes fetch, decode, execute, memory access, write-back, and PC update within one call to the simulation cycle.
- **Control Unit & ALU Control:** Decodes instruction opcodes to set hardware control signals (`Reg2Loc`, `ALUSrc`, `MemtoReg`, `RegWrite`, `MemRead`, `MemWrite`, `Branch`, `ALUOp`) and maps them to appropriate ALU operations.
- **Sign Extension Unit:** Handles sign extension for D-format offsets, I-format immediates, and B/CB-format branch targets.
- **Zero Register Handling:** Enforces LEGv8 `$XZR` (`X31`) read-only zero semantics.

---

## 📂 Project Structure

```text
.
├── cpu.py           # Top-level CPU: simulation loop, PC update, and datapath routing
├── control.py       # Main Control Unit and ALU Control Unit implementations
├── alu.py           # Arithmetic Logic Unit (ALU) execution & zero-flag generation
├── registers.py     # LEGv8 Register File (X0–X30 general-purpose, X31 zero register)
├── memory.py        # Instruction Memory and Data Memory interfaces
├── run_cpu.py       # Execution script to run .hex programs through the simulator
├── auto_grade.py    # Automated test runner evaluating against target CPU states
└── test_cases/      # Pre-encoded machine-code programs (.hex) for verification
