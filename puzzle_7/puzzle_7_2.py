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
    def __init__(self):
        self.pc = 0
        self.instruction_registry = None

        # IO
        self._input_register = None
        self._output_register = []

        # FLAGS
        self.flag_waiting_for_input = False
        self.flag_halt = False

    def load_program(self, program):
        self.memory = program


    def get_output(self):
        return self._output_register

    
    def enter_input(self, input):
        if not self.flag_waiting_for_input:
            raise Exception('Not expected input')
        else:
            self._input_register = input


    def continue_execution(self):
        if self.flag_halt:
            return

        while True:
            self.instruction_registry = self._get_instruction()
            opcode = self.instruction_registry.opcode

            if opcode == 99:
                self.flag_halt = True
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
                if self._input_register == None:
                    self.flag_waiting_for_input = True
                    return
                else:
                    result_pos = self.memory[self.pc + 1]
                    self.memory[result_pos] = self._input_register
                    self._input_register = None
                    print(f'>> {self.memory[result_pos]}')
                    self.pc += 2
            elif opcode == 4: # OUTPUT value_pos
                result_pos = self.memory[self.pc + 1]
                print(self.memory[result_pos])
                self._output_register.append(self.memory[result_pos])
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


def get_possible_phase_setting_sequences(possible_values):
    return list(itertools.permutations(possible_values))


raw_program = open(os.path.join(sys.path[0], 'input')).read()
program_listed = [int(value) for value in raw_program.split(',')]

max_thrust = 0
phase_settings_permutations = get_possible_phase_setting_sequences([5,6,7,8,9])

for setting_permutation, phase_setting in enumerate(phase_settings_permutations, start=1):
    print(f'# Testing {phase_setting} ({setting_permutation}/{len(phase_settings_permutations)})')
    
    amps = [IntcodeComputer() for _ in range(5)]
    for amp in amps:
        amp.load_program(program_listed)
    
    amp_input = 0

    for i, amp in enumerate(amps):
        amp.continue_execution()
        amp.enter_input(phase_setting[i])
        amp.continue_execution()
        amp.enter_input(amp_input)
        amp.continue_execution()

        amp_input = amp.get_output()[-1]

    while not amps[4].flag_halt:
        for amp in amps:
            amp.enter_input(amp_input)
            amp.continue_execution()
            amp_input = amp.get_output()[-1]

    if amps[4].get_output()[-1] > max_thrust:
        max_thrust = amps[4].get_output()[-1]

print(max_thrust)
