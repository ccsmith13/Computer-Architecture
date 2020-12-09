"""CPU functionality."""

import sys

HLT = 0b00000001		
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000111
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU.""" 
        self.ram = [0] * 256
        self.reg = [0] * 8
        # set the stack pointer 
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
        # Running
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self):
        try: 
            if len(sys.argv) < 2:
                print(f'Error: missing filename argument')
                sys.exit(1)

            # add a counter that adds memory at that index 
            ram_index = 0
                
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#")[0]
                    stripped_split_line = split_line.strip()
                
                if stripped_split_line != '':
                    command = int(stripped_split_line, 2)
                    # load command into memory
                    self.ram[ram_index] = command
                    ram_index += 1

        except FileNotFoundError:
            print(f'Your file {sys.argv[1]} could not be found in {sys.argv[0]}')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

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
        while self.running:

            command_to_execute = self.ram_read(self.pc)

            if command_to_execute == LDI:
                operation_1 = self.ram_read(self.pc + 1)
                operation_2 = self.ram_read(self.pc + 2)
                self.reg[operation_1] = operation_2
                self.pc += 3

            elif command_to_execute == PRN:
                operation_1 = self.ram_read(self.pc + 1)
                print(self.reg[operation_1])
                self.pc += 2

            elif command_to_execute == HLT:
                self.running = False
                self.pc += 1

            elif command_to_execute == PUSH: 
                # decrement the SP 
                self.reg[7] -= 1
                # starts at F4, decrements to F3 
                # copy value from given register in address SP is pointing to 
                reg_address = self.ram[self.pc+1]
                value = self.reg[reg_address]

                # copy into SP address 
                SP = self.reg[7]
                self.ram[SP] = value
            
            elif command_to_execute == POP: 
                SP = self.reg[7]
                value = self.ram[SP]
                reg_address = self.ram[self.pc+1]
                self.reg[reg_address] = value
                self.reg[7] += 1
                



