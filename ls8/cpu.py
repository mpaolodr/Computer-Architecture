"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # 256 bytes of memory
        self.reg = [0] * 8  # r0 - r7 where r5,r6,r7 are reserved
        self.pc = 0  # program counter, start at 0
        self.running = False  # will switch to True when run method is called
        self.sp = 7  # index in register which has the address in memory to store stack
        self.ir_table = {
            LDI: self.LDI,
            PRN: self.PRN,
            HLT: self.HLT,
            ADD: self.ADD,
            MUL: self.MUL,
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET
        }

    def load(self, filename):
        """Load a program into memory."""

        # open file and store instructions in memory
        with open(f"examples/{filename}") as f:
            address = 0

            for line in f:
                line = line.split("#")
                line = line[0].strip()

                if line == "":
                    continue

                value = int(line, 2)

                self.ram_write(value, address)

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

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

        self.running = True
        sp = self.sp
        # initial value at r7
        # address in memory if stack is empty
        self.reg[sp] = 0xf4

        while self.running:
            IR = self.ram[self.pc]
            self.ir_table[IR]()

    def ram_read(self, MAR):
        # MAR - address being read
        # MDR - data that was stored
        MDR = self.ram[MAR]
        return MDR

    def ram_write(self, MDR, MAR):
        # MAR - address being written to
        # MDR - data to be written
        self.ram[MAR] = MDR

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.reg[operand_a] = operand_b

        self.pc += 3

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        value = self.reg[operand_a]

        print(value)

        self.pc += 2

    def HLT(self):
        self.running = False

    def ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.alu("ADD", operand_a, operand_b)

        self.pc += 3

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.alu("MUL", operand_a, operand_b)

        self.pc += 3

    def PUSH(self):
        # register index to grab the address in memory
        sp = self.sp
        self.reg[sp] -= 1

        stack_addr = self.reg[sp]

        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        self.ram_write(value, stack_addr)

        self.pc += 2

    def POP(self):
        sp = self.sp
        stack_addr = self.reg[sp]

        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(stack_addr)

        self.reg[reg_num] = value
        self.reg[sp] += 1
        self.pc += 2

    def CALL(self):
        # grab return address - index in ram that has the next instruction after call
        return_addr = self.pc + 2

        # push to stack
        self.reg[self.sp] -= 1
        self.ram_write(return_addr, self.reg[self.sp])

        # set pc
        reg_num = self.ram_read(self.pc + 1)
        sub_addr = self.reg[reg_num]

        self.pc = sub_addr

    def RET(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
