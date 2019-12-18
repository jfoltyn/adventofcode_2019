import itertools
import sys
import os

from dataclasses import dataclass
from enum import Enum

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
    def load_program(self, program, input = []):
        self.memory = program
        self.pc = 0
        self.instruction_registry = None
        self.output = []
        self.input = input


    def get_output(self):
        return self.output


    def execute_program(self):
        while True:
            self.instruction_registry = self._get_instruction()
            opcode = self.instruction_registry.opcode

            if opcode == 99:
                break
            elif opcode == 1: # ADD x y result_pos
                result_pos = self.memory[self.pc + 3]
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                self.memory[result_pos] = x + y
                self.pc += 4
            elif opcode == 2: # MULTIPLY x y result_pos
                result_pos = self.memory[self.pc + 3]
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                self.memory[result_pos] = x * y
                self.pc += 4
            elif opcode == 3: # INPUT result_pos
                result_pos = self.memory[self.pc + 1]
                if len(self.input) > 0:
                    self.memory[result_pos] = self.input.pop(0)
                    print(f'>> {self.memory[result_pos]}')
                else:
                    self.memory[result_pos] = int(input())
                self.pc += 2
            elif opcode == 4: # OUTPUT value_pos
                result_pos = self.memory[self.pc + 1]
                print(self.memory[result_pos])
                self.output.append(self.memory[result_pos])
                self.pc += 2
            elif opcode == 5: # JUMP-IF-TRUE test_value pc_value
                test_value = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                pc_value = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                if test_value != 0:
                    self.pc = pc_value
                else:
                    self.pc += 3
            elif opcode == 6: # JUMP-IF-FALSE test_value pc_value
                test_value = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                pc_value = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                if test_value == 0:
                    self.pc = pc_value
                else:
                    self.pc += 3
            elif opcode == 7: # LESS-THAN x y result_pos 
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                result_pos = self.memory[self.pc + 3]
                if x < y:
                    self.memory[result_pos] = 1
                else:
                    self.memory[result_pos] = 0
                self.pc += 4
            elif opcode == 8: # EQUALS x y result_pos 
                x = self._get_value_from_param(1, self.instruction_registry.param_1_mode)
                y = self._get_value_from_param(2, self.instruction_registry.param_2_mode)
                result_pos = self.memory[self.pc + 3]
                if x == y:
                    self.memory[result_pos] = 1
                else:
                    self.memory[result_pos] = 0
                self.pc += 4


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


def get_possible_phase_setting_sequences():
    return list(itertools.permutations([0, 1, 2, 3, 4]))


raw_program = open(os.path.join(sys.path[0], 'input')).read()
program_listed = [int(value) for value in raw_program.split(',')]

amp1 = IntcodeComputer()
amp2 = IntcodeComputer()
amp3 = IntcodeComputer()
amp4 = IntcodeComputer()
amp5 = IntcodeComputer()

max_thrust = 0

iter = 1
phase_settings_permutations = get_possible_phase_setting_sequences()
for phase_setting in phase_settings_permutations:
    print(f'>> Testing {phase_setting} ({iter}/{len(phase_settings_permutations)})')
    iter += 1

    amp1.load_program(program_listed, [phase_setting[0], 0])
    amp1.execute_program()

    amp2.load_program(program_listed, [phase_setting[1], amp1.get_output()[0]])
    amp2.execute_program()

    amp3.load_program(program_listed, [phase_setting[2], amp2.get_output()[0]])
    amp3.execute_program()

    amp4.load_program(program_listed, [phase_setting[3], amp3.get_output()[0]])
    amp4.execute_program()

    amp5.load_program(program_listed, [phase_setting[4], amp4.get_output()[0]])
    amp5.execute_program()

    if amp5.get_output()[0] > max_thrust:
        max_thrust = amp5.get_output()[0]

print(max_thrust)