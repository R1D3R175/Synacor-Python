from machine import Machine

linux = Machine(Debug=True)

linux.load_program("challenge.bin")
linux.run()