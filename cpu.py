# Name: Zeynep Sıla
# Surname: Bekar

from memory import InstructionMemory, DataMemory
from registers import RegisterFile
from control import MainControl, ALUControl
from alu import ALU

class LEGv8_CPU:
    def __init__(self, hex_file_path):
        self.pc = 0
        self.imem = InstructionMemory(hex_file_path)
        self.dmem = DataMemory()
        self.reg_file = RegisterFile()
        self.main_ctrl = MainControl()
        self.alu_ctrl = ALUControl()
        self.alu = ALU()
        self.halted = False
        self.current_instr = 0
        self.ctrl_signals = {}

    def run(self):
        cycle = 0
        print("--- Simulation Start ---")
        while not self.halted:
            self.step()
            if not self.halted:
                self.log_state(cycle)
            cycle += 1
        print("--- Simulation Halted ---")

    def step(self):
        self.current_instr = self.imem.read(self.pc)

        if self.current_instr == 0:
            self.halted = True
            return

        opcode = (self.current_instr >> 21) & 0x7FF
        rm = (self.current_instr >> 16) & 0x1F
        rn = (self.current_instr >> 5) & 0x1F
        rt = self.current_instr & 0x1F

        i_immediate = (self.current_instr >> 10) & 0xFFF
        if i_immediate & 0x800:
            i_immediate -= 0x1000

        d_address = (self.current_instr >> 12) & 0x1FF
        if d_address & 0x100:
            d_address -= 0x200

        cbz_address = (self.current_instr >> 5) & 0x7FFFF
        if cbz_address & 0x40000:
            cbz_address -= 0x80000

        b_address = self.current_instr & 0x3FFFFFF
        if b_address & 0x2000000:
            b_address -= 0x4000000

        self.ctrl_signals = self.main_ctrl.decode(opcode)

        is_cbz = ((opcode >> 3) == 180 or opcode == 1440)

        read_reg1 = rn
        if is_cbz:
            read_reg2 = rt
        else:
            read_reg2 = rt if self.ctrl_signals['Reg2Loc'] else rm

        data1, data2 = self.reg_file.read(read_reg1, read_reg2)

        operand_a = data1
        if self.ctrl_signals['ALUSrc']:
            opcode_10bit = opcode >> 1
            if opcode_10bit in [580, 836] or opcode in [1160, 1161, 1672, 1673]:
                operand_b = i_immediate
            else:
                operand_b = d_address
        else:
            operand_b = data2

        alu_control_code = self.alu_ctrl.get_alu_control(self.ctrl_signals['ALUOp'], opcode)
        alu_result, zero_flag = self.alu.execute(operand_a, operand_b, alu_control_code)

        alu_result = alu_result & 0xFFFFFFFFFFFFFFFF

        read_data = 0
        if self.ctrl_signals['MemWrite']:
            self.dmem.write_word(alu_result, data2)

        if self.ctrl_signals['MemRead']:
            read_data = self.dmem.read_word(alu_result)

        if self.ctrl_signals['RegWrite']:
            write_data = read_data if self.ctrl_signals['MemtoReg'] else alu_result
            self.reg_file.write(rt, write_data)

        if (opcode >> 5) == 5:  # Unconditional Branch (B)
            self.pc += (b_address * 4)
        elif self.ctrl_signals['Branch'] and zero_flag:  # Conditional Branch (CBZ)
            self.pc += (cbz_address * 4)
        else:
            self.pc += 4

    def log_state(self, cycle):
        print(f"Cycle: {cycle}")
        print(f"PC: {self.pc}")
        print(f"Instruction: 0x{self.current_instr:08X}")

        if self.ctrl_signals:
            print("Control Signals:")
            for key, value in self.ctrl_signals.items():
                print(f"  {key}: {value}")
        else:
            print("Control Signals: [MISSING - Check step() implementation]")

        print("Registers (Non-Zero):")
        for i in range(32):
            val = self.reg_file.read(i, 31)[0]
            if val != 0:
                print(f"  X{i}: {val}")
        print("-" * 20)