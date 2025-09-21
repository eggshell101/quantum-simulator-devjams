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
        # Initialize empty circuit diagram as list of lists
        self.diagram = [["───" for _ in range(0)] for _ in range(n_qubits)]
    
    def _extend_diagram(self):
        for wire in self.diagram:
            wire.append("───")

    def add_gate(self, gate, targets, controls=[]):
        self._extend_diagram()
        col = len(self.diagram[0])-1

        # Draw the gate
        for i in range(self.n):
            if i in targets:
                self.diagram[i][col] = f"-{gate}-"
            elif i in controls:
                self.diagram[i][col] = "●"
            else:
                self.diagram[i][col] = "───"
        
        # Draw vertical lines connecting controls to targets if multi-qubit
        if controls and targets:
            min_qubit = min(controls + targets)
            max_qubit = max(controls + targets)
            for i in range(min_qubit+1, max_qubit):
                if i not in targets + controls:
                    self.diagram[i][col] = "│"

        # Apply the gate to the state
        if gate in ["H", "X", "Y", "Z"]:
            self.state = apply_single_qubit_gate(self.state, 
                                                 {"H": H, "X": X, "Y": Y, "Z": Z}[gate], 
                                                 targets[0], self.n)
        elif gate == "CNOT":
            self.state = cnot_on_n_qubits(control=controls[0], target=targets[0], n_qubits=self.n) @ self.state
        elif gate == "TOFFOLI":
            self.state = toffoli_on_n_qubits(control1=controls[0], control2=controls[1], 
                                             target=targets[0], n_qubits=self.n) @ self.state

    def draw(self):
        for i in range(self.n):
            print(f"q{i}: "+"".join(self.diagram[i]))

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
            circuit.add_gate("+", targets=[target], controls=[control])

        elif gate == "TOFFOLI":
            c1 = int(input(f"Enter first control qubit (0 to {n-1}): "))
            c2 = int(input(f"Enter second control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            circuit.add_gate(gate, targets=[target], controls=[c1, c2])

        show_state = input("Show state vector? (y/n): ").strip().lower()
        if show_state == "y":
            print("\nState vector:\n", circuit.state)
            print("Probabilities:", np.abs(circuit.state.flatten())**2)
        
        draw = input("Draw circuit? (y/n): ").strip().lower()
        if draw == "y":
            print("\nCircuit diagram:")
            circuit.draw()

if __name__ == "__main__":
    main()
