"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.reg = [0] * 8  # r0 - r7 where r5,r6,r7 are reserved
        self.pc = 0  # program counter, start at 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # current instruction
            ir = self.ram[self.pc]

            # LDI: has 2 operands base on opcode
            if ir == 0b10000010:
                # grab operands
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                # operand_a is the register address to store operand b
                self.reg[operand_a] = operand_b

                self.pc += 3

            # PRN: has 1 operand which is the register address of value to be printed
            elif ir == 0b01000111:
                operand_a = self.ram_read(self.pc + 1)
                data = self.reg[operand_a]

                print(data)

                self.pc += 2

            # HLT
            elif ir == 0b00000001:
                running = False

            else:
                print(f"Unknown instruction {ir} at address {self.pc}")
                sys.exit(1)

    def ram_read(self, MAR):
        # MAR - address being read
        # MDR - data that was stored
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MDR, MAR):
        # MAR - address being written to
        # MDR - data to be written
        self.ram[MAR] = MDR
