import numpy as np
import tkinter as tk
from tkinter import scrolledtext
from Basic_1 import zero_state, apply_single_qubit_gate, cnot_on_n_qubits, toffoli_on_n_qubits, H, X, Y, Z

class Circuit:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.state = zero_state(n_qubits)
        self.diagram = [[] for _ in range(n_qubits)]  # list of lists for each qubit line
    
    def _extend_diagram(self):
        # Add default line spacing for next gate
        for wire in self.diagram:
            wire.append("───")  

    def add_gate(self, gate, targets, controls=[]):
        self._extend_diagram()
        col = len(self.diagram[0]) - 1

        for i in range(self.n):
            if i in targets:
                self.diagram[i][col] = f"[{gate}]"
            elif i in controls:
                self.diagram[i][col] = "●"
            else:
                self.diagram[i][col] = "───"

        # Draw vertical lines connecting controls to targets
        if controls and targets:
            min_q = min(controls + targets)
            max_q = max(controls + targets)
            for i in range(min_q + 1, max_q):
                if i not in targets + controls:
                    self.diagram[i][col] = "│"

        # Apply the gate to the state
        if gate in ["H", "X", "Y", "Z"]:
            self.state = apply_single_qubit_gate(
                self.state, {"H": H, "X": X, "Y": Y, "Z": Z}[gate], targets[0], self.n)
        elif gate == "CNOT":
            self.state = cnot_on_n_qubits(control=controls[0], target=targets[0], n_qubits=self.n) @ self.state
        elif gate == "TOFFOLI":
            self.state = toffoli_on_n_qubits(control1=controls[0], control2=controls[1], 
                                             target=targets[0], n_qubits=self.n) @ self.state

    def draw(self):
        # Convert the diagram to string with adequate spacing
        diagram_lines = []
        for i in range(self.n):
            diagram_lines.append(f"q{i}: " + " ".join(self.diagram[i]))
        return "\n".join(diagram_lines)

# Tkinter GUI to show circuit and state
def show_results(circuit: Circuit):
    root = tk.Tk()
    root.title("Quantum Circuit Results")

    # Circuit diagram
    tk.Label(root, text="Quantum Circuit Diagram:").pack(pady=5)
    diagram_box = scrolledtext.ScrolledText(root, width=100, height=20)
    diagram_box.pack(pady=5)
    diagram_box.insert(tk.END, circuit.draw())
    diagram_box.config(state="disabled")

    # State vector
    tk.Label(root, text="Final State Vector:").pack(pady=5)
    state_box = scrolledtext.ScrolledText(root, width=100, height=8)
    state_box.pack(pady=5)
    state_box.insert(tk.END, str(circuit.state))
    state_box.config(state="disabled")

    # Probabilities
    tk.Label(root, text="Probabilities of all basis states:").pack(pady=5)
    prob_box = scrolledtext.ScrolledText(root, width=100, height=8)
    prob_box.pack(pady=5)
    probabilities = np.abs(circuit.state.flatten())**2
    prob_box.insert(tk.END, str(probabilities))
    prob_box.config(state="disabled")

    root.mainloop()

# Main input loop
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
            c1 = int(input(f"Enter first control qubit (0 to {n-1}): "))
            c2 = int(input(f"Enter second control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            circuit.add_gate(gate, targets=[target], controls=[c1, c2])

        show_state = input("Show current state vector? (y/n): ").strip().lower()
        if show_state == "y":
            print("\nCurrent state vector:\n", circuit.state)
            print("Probabilities:", np.abs(circuit.state.flatten())**2)
        
        draw = input("Draw circuit? (y/n): ").strip().lower()
        if draw == "y":
            print("\nCircuit diagram:")
            print(circuit.draw())

    # Show Tkinter GUI after quitting
    show_results(circuit)

if __name__ == "__main__":
    main()
