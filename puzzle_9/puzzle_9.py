import os
import sys

from IntcodeComputer_9 import IntcodeComputer


raw_program = open(os.path.join(sys.path[0], 'input')).read()
program_listed = [int(value) for value in raw_program.split(',')]


computer = IntcodeComputer()
computer.load_program(program_listed)
computer.continue_execution()
computer.enter_input(2) # enter_input(1) for Part One
computer.continue_execution()

print(computer.get_output())
