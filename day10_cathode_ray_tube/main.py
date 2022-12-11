from sys import stdin

from src.ClockCircuit import ClockCircuit
from src.CrtDrawingObserver import CrtDrawingObserver
from src.SignalStrengthObserver import SignalStrengthObserver

if __name__ == '__main__':
    signal_strength_observer = SignalStrengthObserver()
    crt_drawing_observer = CrtDrawingObserver()
    clock_circuit = ClockCircuit([signal_strength_observer, crt_drawing_observer])
    clock_circuit.load_instructions(stdin)
    clock_circuit.run_program()

    print(f'Sum of the relevant signal strengths is {signal_strength_observer.signal_strength_sum()}')
    print(crt_drawing_observer.get_screen_output())
