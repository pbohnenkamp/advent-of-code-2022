from typing import Iterable, List


class ClockCircuitInstruction:
    cycles_to_complete: int = None


class NoOpInstruction(ClockCircuitInstruction):
    def __init__(self) -> None:
        self.cycles_to_complete = 1


class AddXRegisterInstruction(ClockCircuitInstruction):
    def __init__(self, add_value: int) -> None:
        self.cycles_to_complete = 2
        self.add_value = add_value


class ClockCircuit:
    def __init__(self, register_x_cycle_event_subscribers: List = None) -> None:
        self._register_x = 1
        if register_x_cycle_event_subscribers is None:
            register_x_cycle_event_subscribers = []
        self._register_x_cycle_event_subscribers = register_x_cycle_event_subscribers
        self._program: List[ClockCircuitInstruction] = []
        self._current_cycle_count = 0

    def load_instructions(self, instruction_strings: Iterable[str]):
        self._program = []
        for instruction_string in instruction_strings:
            instruction_parts = instruction_string.strip().split(' ')
            if instruction_parts[0] == 'noop':
                self._program.append(NoOpInstruction())
            elif instruction_parts[0] == 'addx':
                self._program.append(AddXRegisterInstruction(int(instruction_parts[1])))
            else:
                raise Exception(f'CompileError: {instruction_parts[0]} is an invalid instruction')

    def run_program(self):
        for instruction in self._program:
            self._run_instruction(instruction)

    def _run_instruction(self, instruction: ClockCircuitInstruction):
        for i in range(instruction.cycles_to_complete):
            self._cycle()
        if isinstance(instruction, AddXRegisterInstruction):
            self._register_x += instruction.add_value

    def _cycle(self):
        self._current_cycle_count += 1
        self._send_cycle_executing_events()

    def _send_cycle_executing_events(self):
        for subscriber in self._register_x_cycle_event_subscribers:
            subscriber.during_cycle_event(self._register_x)
