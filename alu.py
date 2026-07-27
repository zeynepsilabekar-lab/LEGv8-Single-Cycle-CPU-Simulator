class ALU:
    def execute(self, operand_a, operand_b, alu_control):
        result = 0
        zero_flag = False

        if alu_control == '0000': 
            result = operand_a & operand_b
            
        elif alu_control == '0001': 
            result = operand_a | operand_b
            
        elif alu_control == '0010': 
            result = operand_a + operand_b
            
        elif alu_control == '0110':  
            result = operand_a - operand_b
            
        elif alu_control == '0111':  
            result = operand_b
            
        elif alu_control == '1100':  
            result = ~(operand_a | operand_b)

        if result == 0:
            zero_flag = True
        else:
            zero_flag = False

        return result, zero_flag
