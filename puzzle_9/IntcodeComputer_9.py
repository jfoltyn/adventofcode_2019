from dataclasses import dataclass
from enum import Enum
from typing import Dict


class ParamMode(Enum):
    position_mode = '0'
    immediate_mode = '1'
    relative_mode = '2'


@dataclass
class Instruction:
    opcode: int
    params_modes : Dict[int, ParamMode]


class IntcodeComputer:
    def __init__(self):
        self.pc = 0
        self.instruction_registry = None
        self._relative_base = 0

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
            self.flag_waiting_for_input = False


    def continue_execution(self):
        while not (self.flag_halt or self.flag_waiting_for_input):
            self.instruction_registry = self._get_instruction()
            try:
                self._execute_instruction_from_instruction_registry()
            except IndexError:
                self._allocate_more_memory()


    def _execute_instruction_from_instruction_registry(self):
        opcode = self.instruction_registry.opcode
        if opcode == 99:
            self.flag_halt = True
        elif opcode == 1: # ADD x y result_memory_address
            x = self._get_value_from_param(1)
            y = self._get_value_from_param(2)
            result_memory_address = self._get_memory_address(3)
            self.memory[result_memory_address] = x + y
            self.pc += 4
        elif opcode == 2: # MULTIPLY x y result_pos
            x = self._get_value_from_param(1)
            y = self._get_value_from_param(2)
            result_memory_address = self._get_memory_address(3)
            self.memory[result_memory_address] = x * y
            self.pc += 4
        elif opcode == 3: # INPUT result_pos
            if self._input_register == None:
                self.flag_waiting_for_input = True
                return
            else:
                result_memory_address = self._get_memory_address(1)
                self.memory[result_memory_address] = self._input_register
                self._input_register = None
                self.pc += 2
        elif opcode == 4: # OUTPUT output
            output = self._get_value_from_param(1)
            self._output_register.append(output)
            self.pc += 2
        elif opcode == 5: # JUMP-IF-TRUE test_value pc_value
            test_value = self._get_value_from_param(1)
            pc_value = self._get_value_from_param(2)
            if test_value != 0:
                self.pc = pc_value
            else:
                self.pc += 3
        elif opcode == 6: # JUMP-IF-FALSE test_value pc_value
            test_value = self._get_value_from_param(1)
            pc_value = self._get_value_from_param(2)
            if test_value == 0:
                self.pc = pc_value
            else:
                self.pc += 3
        elif opcode == 7: # LESS-THAN x y result_pos 
            x = self._get_value_from_param(1)
            y = self._get_value_from_param(2)
            result_memory_address = self._get_memory_address(3)
            if x < y:
                self.memory[result_memory_address] = 1
            else:
                self.memory[result_memory_address] = 0
            self.pc += 4
        elif opcode == 8: # EQUALS x y result_pos 
            x = self._get_value_from_param(1)
            y = self._get_value_from_param(2)
            result_memory_address = self._get_memory_address(3)
            if x == y:
                self.memory[result_memory_address] = 1
            else:
                self.memory[result_memory_address] = 0
            self.pc += 4
        elif opcode == 9: # RELATIVE-BASE-OFFSET offset
            param_value = self._get_value_from_param(1)
            self._relative_base += param_value
            self.pc += 2


    def _get_value_from_param(self, param_pos):
        value_memory_address = self._get_memory_address(param_pos)
        return self.memory[value_memory_address]


    def _get_memory_address(self, param_pos):
        param_mode = self.instruction_registry.params_modes[param_pos]
        if param_mode == ParamMode.position_mode:
            return self.memory[self.pc + param_pos]
        if param_mode == ParamMode.immediate_mode:
            return self.pc + param_pos
        if param_mode == ParamMode.relative_mode:
            param_value = self.memory[self.pc + param_pos]
            return self._relative_base + param_value
        else:
            raise Exception('Unknown param mode')


    def _get_instruction(self):
        instruction = self.memory[self.pc]
        instruction = f'{instruction:05}'
        return Instruction(int(instruction[-2:]),
                           {
                               1: ParamMode(instruction[2]),
                               2: ParamMode(instruction[1]),
                               3: ParamMode(instruction[0])
                           })


    def _allocate_more_memory(self):
        '''Currently doubling memory size. Will optimize later if required'''
        current_memory_size = len(self.memory)
        self.memory.extend(0 for _ in range(current_memory_size))
