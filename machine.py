class Machine:
    def __init__(self, Debug=False):
        self.memory = []
        self.stack = []
        self.registers = [0] * 8
        self.PC = 0
        self.Debug = Debug

    # Read the next bytes
    def _read_bytes(self):
        bytes = int.from_bytes(self.memory[self.PC], byteorder='little') 

        self.PC += 1

        return bytes

    # Read binary file challenge.bin and load all of it into memory
    def load_program(self, filename):
        self.memory = []

        if self.Debug:
            print("[DEBUG] Loading program from file: " + filename)

        bytes_loaded = 0
        with open(filename, 'rb') as f:
            byte = f.read(2)
            bytes_loaded += 2
            while byte:
                self.memory.append(byte)
                byte = f.read(2)
                bytes_loaded += 2

        if self.Debug:
            print("[DEBUG] Loaded " + str(bytes_loaded) + " bytes")

    # Run the program
    def run(self):
        while True:
            opcode = self._read_bytes()
            self.parse_opcode(opcode)

    # halt: 0
    # stop execution and terminate the program
    def _halt(self):
        if self.Debug:
            print("[DEBUG] Halting")
        exit(1)

    # set: 1 a b
    # set register <a> to the value of <b>
    def _set(self):    
        a = self._read_bytes()

        b = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Setting register " + str(a) + " to " + str(b))

        self.registers[a] = b

    # push: 2 a
    # push <a> onto the stack
    def _push(self):
        a = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if self.Debug:
            print("[DEBUG] Pushing " + str(a) + " onto the stack")

        self.stack.append(a)

    # pop: 3 a
    # remove the top element from the stack and write it into <a>; 
    # empty stack = error
    def _pop(self):
        a = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if len(self.stack) == 0:
            raise ValueError("Stack underflow")

        self.registers[a] = self.stack.pop()

        if self.Debug:
            print("[DEBUG] Popping " + str(self.registers[a]) + " from the stack and setting it to register " + str(a))
    
    # eq: 4 a b c
    # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise   
    def _eq(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Setting register " + str(a) + " to " + str(1 if b == c else 0))

        self.registers[a] = 1 if b == c else 0

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # gt: 5 a b c
    # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
    def _gt(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Setting register " + str(a) + " to " + str(1 if b > c else 0))

        self.registers[a] = 1 if b > c else 0

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # jmp: 6 a
    # jump to <a>
    def _jmp(self):
        a = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if self.Debug:
            print("[DEBUG] Jumping to " + str(a))

        self.PC = a

    # jt: 7 a b
    # if <a> is nonzero, jump to <b>
    def _jt(self):
        a = self._read_bytes()

        b = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Jumping to " + str(b) + " if " + str(a) + " is nonzero")

        if a != 0:
            self.PC = b

            if self.Debug:
                print("[DEBUG] Jumping to " + str(b))

    # jf: 8 a b
    # if <a> is zero, jump to <b>
    def _jf(self):
        a = self._read_bytes()

        b = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Jumping to " + str(b) + " if " + str(a) + " is zero")

        if a == 0:
            self.PC = b

            if self.Debug:
                print("[DEBUG] Jumping to " + str(b))

    # add: 9 a b c
    # assign into <a> the sum of <b> and <c> (modulo 32768)
    def _add(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Adding " + str(b) + " and " + str(c) + " and storing the result in register " + str(a))

        self.registers[a] = (b + c) % 32768

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # mult: 10 a b c
    # assign into <a> the product of <b> and <c> (modulo 32768)
    def _mult(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Multiplying " + str(b) + " and " + str(c) + " and storing the result in register " + str(a))

        self.registers[a] = (b * c) % 32768

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # mod: 11 a b c
    # assign into <a> the remainder of <b> divided by <c>
    def _mod(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Modding " + str(b) + " and " + str(c) + " and storing the result in register " + str(a))

        self.registers[a] = b % c

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # and: 12 a b c
    # assign into <a> the bitwise and of <b> and <c>
    def _bitwise_and(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Bitwise ANDing " + str(b) + " and " + str(c) + " and storing the result in register " + str(a))

        self.registers[a] = b & c

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # or: 13 a b c
    # assign into <a> the bitwise or of <b> and <c>
    def _bitwise_or(self):
        a = self._read_bytes()

        b = self._read_bytes()

        c = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if c > 32775:
            raise ValueError("Value out of range")
        elif c >= 32768:
            c = self.registers[c - 32768]

        if self.Debug:
            print("[DEBUG] Bitwise ORing " + str(b) + " and " + str(c) + " and storing the result in register " + str(a))

        self.registers[a] = b | c

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # not: 14 a b
    # assign into <a> the bitwise not of <b>
    def _bitwise_not(self):
        a = self._read_bytes()

        b = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Bitwise NOTing " + str(b) + " and storing the result in register " + str(a))

        self.registers[a] = 32767 - b

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # rmem: 15 a b
    # read memory at address <b> and write it to <a>
    def _rmem(self):
        a = self._read_bytes()

        b = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Reading memory at " + str(b) + " and storing the result in register " + str(a))

        self.registers[a] = int.from_bytes(self.memory[b], byteorder='little')

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # wmem: 16 a b
    # write the value from <b> into memory at address <a>
    def _wmem(self):
        a = self._read_bytes()

        b = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if b > 32775:
            raise ValueError("Value out of range")
        elif b >= 32768:
            b = self.registers[b - 32768]

        if self.Debug:
            print("[DEBUG] Writing " + str(b) + " into memory at " + str(a))

        self.memory[a] = b.to_bytes(2, byteorder='little', signed=False)

        if self.Debug:
            print("[DEBUG] Memory at " + str(a) + " is now " + str(self.memory[a].hex()))

    # call: 17 a
    # write the address of the next instruction to the stack and jump to <a>
    def _call(self):
        a = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        self.stack.append(self.PC)
        self.PC = a

        if self.Debug:
            print("[DEBUG] Calling " + str(a))

    # ret: 18
    # remove the top element from the stack and jump to it; empty stack = halt
    def _ret(self):
        addr = self.stack.pop()
        if len(self.stack) == 0:
            raise ValueError("Stack is empty")

        self.PC = addr

        if self.Debug:
            print("[DEBUG] Returning from " + str(addr))

    # out: 19 a
    # write the character represented by ascii code <a> to the terminal
    def _out(self):
        a = self._read_bytes()

        if a > 32775:
            raise ValueError("Value out of range")
        elif a >= 32768:
            a = self.registers[a - 32768]

        if self.Debug:
            print("[DEBUG] Printing " + str(chr(a)))

        print(chr(a), end="")

    # in: 20 a
    # read a character from the terminal and write its ascii code to <a>; 
    # it can be assumed that once input starts, it will continue until a newline is encountered; 
    # this means that you can safely read whole lines from the keyboard and trust that they will be fully read
    def _read(self):
        a = self._read_bytes()

        a -= 32768
        if a < 0 or a > 7:
            raise ValueError("Register index out of range")

        if self.Debug:
            print("[DEBUG] Reading from keyboard and storing the result in register " + str(a))

        a = ord(input())
        self.registers[a] = a

        if self.Debug:
            print("[DEBUG] Register " + str(a) + " is now " + str(self.registers[a]))

    # noop: 21
    # no operation
    def _noop(self):
        if self.Debug:
            print("[DEBUG] No operation")
        pass

    # Parse op-codes
    def parse_opcode(self, opcode):
        if opcode == 0:
            self._halt()
        elif opcode == 1:
            self._set()
        elif opcode == 2:
            self._push()
        elif opcode == 3:
            self._pop()
        elif opcode == 4:
            self._eq()
        elif opcode == 5:
            self._gt()
        elif opcode == 6:
            self._jmp()
        elif opcode == 7:
            self._jt()
        elif opcode == 8:
            self._jf()
        elif opcode == 9:
            self._add()
        elif opcode == 10:
            self._mult()
        elif opcode == 11:
            self._mod()
        elif opcode == 12:
            self._bitwise_and()
        elif opcode == 13:
            self._bitwise_or()
        elif opcode == 14:
            self._bitwise_not()
        elif opcode == 15:
            self._rmem()
        elif opcode == 16:
            self._wmem()
        elif opcode == 17:
            self._call()
        elif opcode == 18:
            self._ret()
        elif opcode == 19:
            self._out()
        elif opcode == 20:
            self._read()
        elif opcode == 21:
            self._noop()
        else:
            if self.Debug:
                print("[DEBUG] Received opcode " + str(opcode) + " which is not a valid opcode")
            raise ValueError("Invalid opcode")