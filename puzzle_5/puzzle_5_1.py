from dataclasses import dataclass
from enum import Enum

# instructions
# 99         - halt
# 1 X Y res  - adds numbers from position `X` and `Y` and stores in position `pos`
# 2 X Y res  - multiply numbers from position `X` and `Y` and stores in position `pos`

PROGRAM = '3,225,1,225,6,6,1100,1,238,225,104,0,1101,65,39,225,2,14,169,224,101,-2340,224,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1001,144,70,224,101,-96,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,92,65,225,1102,42,8,225,1002,61,84,224,101,-7728,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,67,73,224,1001,224,-4891,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1102,54,12,225,102,67,114,224,101,-804,224,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,19,79,225,1101,62,26,225,101,57,139,224,1001,224,-76,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1102,60,47,225,1101,20,62,225,1101,47,44,224,1001,224,-91,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1,66,174,224,101,-70,224,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,226,226,224,102,2,223,223,1005,224,329,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,389,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,419,1001,223,1,223,1008,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,1007,226,677,224,102,2,223,223,1005,224,464,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,584,101,1,223,223,1107,677,226,224,1002,223,2,223,1005,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,629,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,677,677,224,102,2,223,223,1006,224,659,101,1,223,223,1008,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226'

class ParamMode(Enum):
    position_mode = '0'
    immediate_mode = '1'


@dataclass
class Instruction:
    opcode: int
    param_1_mode: ParamMode
    param_2_mode: ParamMode
    param_3_mode: ParamMode


class IntcodeComputer:
    def load_program(self, program):
        self.memory = program
        self.pc = 0
        self.instruction_registry = None


    def execute_program(self):
        while True:
            self.instruction_registry = self._get_instruction()
            opcode = self.instruction_registry.opcode

            if opcode == 99:
                break
            elif opcode == 1: 
                result_pos = self.memory[self.pc + 3]
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                self.memory[result_pos] = x + y
                self.pc += 4
            elif opcode == 2:
                result_pos = self.memory[self.pc + 3]
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                self.memory[result_pos] = x * y
                self.pc += 4
            elif opcode == 3:
                print('>> ', end = '')
                result_pos = self.memory[self.pc + 1]
                self.memory[result_pos] = int(input())
                self.pc += 2
            elif opcode == 4:
                result_pos = self.memory[self.pc + 1]
                print(self.memory[result_pos])
                self.pc += 2


    def _get_value_from_param(self, param_pos, param_mode):
        param_value = self.memory[self.pc + param_pos]
        if param_mode == ParamMode.position_mode:
            return self.memory[param_value]
        if param_mode == ParamMode.immediate_mode:
            return param_value
        else:
            raise Exception('Unknown param mode')


    def _get_instruction(self):
        instruction = self.memory[self.pc]
        instruction = f'{instruction:05}'
        return Instruction(
            opcode = int(instruction[-2:]),
            param_1_mode = ParamMode(instruction[2]),
            param_2_mode = ParamMode(instruction[1]),
            param_3_mode = ParamMode(instruction[0])
        )

computer = IntcodeComputer()
computer.load_program([int(value) for value in PROGRAM.split(',')])
computer.execute_program()
