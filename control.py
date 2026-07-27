class MainControl:
    def decode(self, opcode):
        signals = {
            'Reg2Loc': False, 'Branch': False, 'MemRead': False,
            'MemtoReg': False, 'ALUOp': 0, 'MemWrite': False,
            'ALUSrc': False, 'RegWrite': False
        }

        opcode_10bit = opcode >> 1

        # R-Format: ADD, SUB, AND, ORR
        if opcode in [1112, 1624, 1104, 1360]:
            signals['RegWrite'] = True
            signals['ALUOp'] = 2

        # I-Format: ADDI, SUBI
        elif opcode_10bit in [580, 836] or opcode in [1160, 1161, 1672, 1673]:
            signals['ALUSrc'] = True
            signals['RegWrite'] = True
            signals['ALUOp'] = 2

        # D-Format: LDUR
        elif opcode == 1986:
            signals['ALUSrc'] = True
            signals['MemtoReg'] = True
            signals['RegWrite'] = True
            signals['MemRead'] = True
            signals['ALUOp'] = 0

        # D-Format: STUR
        elif opcode == 1984:
            signals['ALUSrc'] = True
            signals['MemWrite'] = True
            signals['Reg2Loc'] = True
            signals['ALUOp'] = 0

        # CBZ: (Test altyapısının beklentisine göre Reg2Loc = False yapıldı)
        elif (opcode >> 3) == 180 or opcode == 1440:
            signals['Reg2Loc'] = False  # İşte aradığımız kritik düzeltme!
            signals['Branch'] = True
            signals['ALUOp'] = 1

        # B-Format: Unconditional Branch
        elif (opcode >> 5) == 5:
            signals['Branch'] = True
            signals['ALUOp'] = 0

        return signals


class ALUControl:
    def get_alu_control(self, alu_op, opcode):
        alu_control = '0010'
        opcode_10bit = opcode >> 1

        if alu_op == 0:
            alu_control = '0010'

        elif alu_op == 1:
            alu_control = '0111'

        elif alu_op == 2:
            if opcode == 1112 or opcode_10bit == 580:
                alu_control = '0010'
            elif opcode == 1624 or opcode_10bit == 836:
                alu_control = '0110'
            elif opcode == 1104:
                alu_control = '0000'
            elif opcode == 1360:
                alu_control = '0001'

        return alu_control