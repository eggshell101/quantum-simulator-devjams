import numpy as np
from Basic_1 import (
    zero_state,
    apply_single_qubit_gate,
    cnot_on_n_qubits,
    toffoli_on_n_qubits,
    H, X, Y, Z
)

class Circuit:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.state = zero_state(n_qubits)
        self.diagram = [[] for _ in range(n_qubits * 2)]  # extra blank line after each qubit

    def _extend_diagram(self):
        for wire in self.diagram:
            wire.append("───")

    def add_gate(self, gate, targets, controls=[]):
        self._extend_diagram()
        col = len(self.diagram[0]) - 1

        # Place gates and controls
        for i in range(self.n):
            main_line = i * 2
            blank_line = main_line + 1

            # default segments
            self.diagram[main_line][col] = "───"
            self.diagram[blank_line][col] = "   "  # blank for spacing / vertical lines

            # Place gate on main line
            if i in targets:
                if gate in ["H", "X", "Y", "Z"]:
                    self.diagram[main_line][col] = f"[{gate}]"
                elif gate in ["CNOT", "TOFFOLI"]:
                    self.diagram[main_line][col] = "⊕"
            # Place control
            if i in controls:
                self.diagram[main_line][col] = "●"

        # Draw vertical lines in the blank line for multi-qubit gates
        if controls and targets:
            min_qubit = min(controls + targets)
            max_qubit = max(controls + targets)
            for i in range(min_qubit + 1, max_qubit):
                blank_line = i * 2 + 1
                self.diagram[blank_line][col] = "│"

        # Apply gate to statevector
        if gate in ["H", "X", "Y", "Z"]:
            self.state = apply_single_qubit_gate(
                self.state, {"H": H, "X": X, "Y": Y, "Z": Z}[gate], targets[0], self.n
            )
        elif gate == "CNOT":
            self.state = cnot_on_n_qubits(
                control=controls[0], target=targets[0], n_qubits=self.n
            ) @ self.state
        elif gate == "TOFFOLI":
            self.state = toffoli_on_n_qubits(
                control1=controls[0], control2=controls[1], target=targets[0], n_qubits=self.n
            ) @ self.state

    def draw(self):
        for i in range(self.n):
            main_line = i * 2
            blank_line = main_line + 1
            print(f"q{i}: " + "".join(self.diagram[main_line]))
            print("    " + "".join(self.diagram[blank_line]))  # extra blank line with vertical connectors
        print()

    def print_state(self):
        state = self.state.flatten()
        print("\nStatevector (non-zero amplitudes):")
        for i, amp in enumerate(state):
            if abs(amp) > 1e-10:
                print(f"|{i:0{self.n}b}> : {amp}")
        print("\nProbabilities:")
        print(np.abs(state)**2)

    def measure(self):
        probs = np.abs(self.state.flatten())**2
        outcome_index = np.random.choice(len(probs), p=probs)
        new_state = np.zeros_like(self.state)
        new_state[outcome_index] = 1
        self.state = new_state
        return f"|{outcome_index:0{self.n}b}>"


def main():
    n = int(input("Enter number of qubits: "))
    circuit = Circuit(n)

    while True:
        gate = input("\nApply gate (H, X, Y, Z, CNOT, TOFFOLI) or Q to quit: ").strip().upper()
        if gate == "Q":
            break

        if gate in ["H", "X", "Y", "Z"]:
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            circuit.add_gate(gate, targets=[target])

        elif gate == "CNOT":
            control = int(input(f"Enter control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            circuit.add_gate(gate, targets=[target], controls=[control])

        elif gate == "TOFFOLI":
            if n < 3:
                print("TOFFOLI requires at least 3 qubits.")
                continue
            c1 = int(input(f"Enter first control qubit (0 to {n-1}): "))
            c2 = int(input(f"Enter second control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            circuit.add_gate(gate, targets=[target], controls=[c1, c2])

        show_state = input("Show current state vector? (y/n): ").strip().lower()
        if show_state == "y":
            circuit.print_state()
        
        draw = input("Draw circuit? (y/n): ").strip().lower()
        if draw == "y":
            print("\nCircuit diagram:")
            circuit.draw()

    print("\n=== Final Quantum Circuit ===")
    circuit.draw()
    print("\n=== Final State Vector & Probabilities ===")
    circuit.print_state()

    print("\n=== Measurement Simulation ===")
    outcome = circuit.measure()
    print(f"Measurement outcome: {outcome}")
    print("\nState after measurement (collapsed):")
    circuit.print_state()


if __name__ == "__main__":
    main()
