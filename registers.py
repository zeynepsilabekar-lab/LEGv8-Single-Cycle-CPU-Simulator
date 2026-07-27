class RegisterFile:
    def __init__(self):
        self.registers = [0] * 32

    def read(self, reg1, reg2):
        data1 = self.registers[reg1]
        data2 = self.registers[reg2]
        return data1, data2

    def write(self, reg, value):
        # LEGv8'de X31 (XZR) yazmacı her zaman 0'dır, üzerine yazma engellenir.
        if reg != 31:
            self.registers[reg] = value & 0xFFFFFFFFFFFFFFFF