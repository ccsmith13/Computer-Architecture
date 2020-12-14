"""CPU functionality."""

import sys

HLT = 0b00000001		
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
MOD = 0b10100100
SHL = 0b10101100
SHR = 0b10101101
OR = 0b10101010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU.""" 
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        #IR: Instruction Register
        self.ir = 0
        #MAR: Memory Address Register
        self.mar = 0
        #MDR: Memory Data Register
        self.mdr = 0
        #FL: Flags
        self.fl = 0
        #HLT: Halted status (True / False) 
        self.halted = False

    # Defining some properties for easier use with functions / reusability 
    @property
    def sp(self):
        return self.reg[7]

    @property
    def operand_a(self):
        return self.ram_read(self.pc + 1)

    @property
    def operand_b(self):
        return self.ram_read(self.pc + 2)
    
    @property
    def instruction_size(self):
        return ((self.ir >> 6) & 0b11) + 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self):
            ram_index = 0

            if len(sys.argv) < 2:
                print('Load error: Please add the name of the second file you want to load')
                exit()

            filename = sys.argv[1]
            
            try:
                with open(filename, 'r')as f:
                    for line in f:
                        if line != "\n" and line[0] != "#":
                            self.ram[ram_index] = int(line[0:8], 2)
                            ram_index += 1
            except FileNotFoundError:
                print(f'Error: file {filename} not found.')
                exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == OR:
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == CMP:
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl |= 0b100
            else: 
                self.fl &= 0b011
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl |= 0b010
            else:
                self.fl &= 0b101
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl |= 0b001
            else: 
                self.fl &= 0b110
        
        elif op == MOD: 
                if self.reg[reg_b] == 0:
                    print("Error: second register == 0 in MOD command")
                    self.running = False
                else: 
                    self.reg[reg_a] %= self.reg[reg_b]
        
        elif op == SHL:
            # <<= is the bitwise operator to shift bits to the left
            self.reg[reg_a] <<= self.reg[reg_b]
        
        elif op == SHR:
            # >>= is the bitwise operator to shift bits to the right 
            self.reg[reg_a] >>= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")
        
        self.reg[reg_a] = self.reg[reg_a] & 0xFF

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram_read(self.pc)
            self.run_command(ir, self.operand_a, self.operand_b)

    def run_command(self, command_to_execute, operand_a, operand_b):
        alu_function = command_to_execute >> 5 & 0b1
        sets_pc = command_to_execute >> 4 & 0b1
        number_of_operands = (command_to_execute >> 6 & 0b11)
        
        if not sets_pc: 
            if command_to_execute == LDI:
                operation_1 = self.ram_read(self.pc + 1)
                operation_2 = self.ram_read(self.pc + 2)
                self.reg[operation_1] = operation_2

            elif command_to_execute == PRN:
                print(self.reg[self.ram_read(self.pc + 1)])

            elif command_to_execute == HLT:
                self.halted = True

            elif command_to_execute == PUSH: 
                self.reg[7] -= 1
                reg_address = self.ram[self.pc+1]
                value = self.reg[reg_address]
                self.ram[self.reg[7]] = value
            
            elif command_to_execute == POP: 
                value = self.ram[self.reg[7]]
                reg_address = self.ram[self.pc+1]
                self.reg[reg_address] = value
                if self.reg[7] < 0xF4: 
                    self.reg[7] += 1
                else:
                    print("Error: Stack Underflow")
                    sys.exit(1)

            elif command_to_execute == CALL: 
                self.reg[7] -= 1
                self.ram_write(self.reg[7], self.pc + self.instruction_size)
                self.pc = self.reg[self.operand_a]               

            elif command_to_execute == RET: 
                self.pc = self.ram_read(self.reg[7])
                self.reg[7] += 1
            elif alu_function: 
                self.alu(command_to_execute, operand_a, operand_b)
            self.pc += number_of_operands + 1
        else: 
            if command_to_execute == JMP: 
                self.pc = self.reg[self.operand_a]
            elif command_to_execute == JEQ: 
                if self.fl & 0b1: 
                    self.pc = self.reg[self.operand_a]
                else:
                    self.pc += 2
            elif command_to_execute == JNE: 
                if not self.fl & 0b1: 
                    self.pc = self.reg[self.operand_a]
                else:
                    self.pc += 2
            else: 
                self.pc += (command_to_execute >> 6)+1 


            



