"""CPU functionality."""

import sys

HLT = 0b00000001		
LDI = 0b10000010
PRN = 0b01000111

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
        # Running
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
            if command_to_execute == PRN:
                operation_1 = self.ram_read(self.pc + 1)
                print(self.reg[operation_1])
                self.pc += 2
            if command_to_execute == HLT:
                self.running = False
                self.pc += 1
