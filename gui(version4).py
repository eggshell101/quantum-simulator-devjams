import numpy as np
import tkinter as tk
from Basic_1 import zero_state, apply_single_qubit_gate, cnot_on_n_qubits, toffoli_on_n_qubits, H, X, Y, Z

CELL_WIDTH = 60
CELL_HEIGHT = 40
GATE_COLOR = "#87CEFA"  # Light blue
CONTROL_COLOR = "#FF6347"  # Tomato red
TEXT_COLOR = "black"

class Circuit:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.state = zero_state(n_qubits)
        self.diagram = [[] for _ in range(n_qubits)]  # list of gate info tuples

    def add_gate(self, gate, targets, controls=[]):
        self.diagram.append((gate, targets, controls))
        # Apply gate to state
        if gate in ["H", "X", "Y", "Z"]:
            self.state = apply_single_qubit_gate(
                self.state, {"H": H, "X": X, "Y": Y, "Z": Z}[gate], targets[0], self.n)
        elif gate == "CNOT":
            self.state = cnot_on_n_qubits(control=controls[0], target=targets[0], n_qubits=self.n) @ self.state
        elif gate == "TOFFOLI":
            self.state = toffoli_on_n_qubits(control1=controls[0], control2=controls[1], 
                                             target=targets[0], n_qubits=self.n) @ self.state

def draw_circuit(circuit: Circuit):
    rows = circuit.n
    cols = len(circuit.diagram)
    gate_spacing = 20  # extra space between consecutive gates

    root = tk.Tk()
    root.title("Quantum Circuit")

    # Compute canvas width including spacing
    canvas_width = max(cols * (CELL_WIDTH + gate_spacing) + 100, 300)
    canvas_height = rows * CELL_HEIGHT + 100
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.grid(row=0, column=0, padx=10, pady=10)

    # Draw horizontal wires
    for i in range(rows):
        y = 30 + i * CELL_HEIGHT
        canvas.create_line(50, y, canvas_width-50, y, width=2)

    # Draw gates with spacing
    for col, gate_info in enumerate(circuit.diagram):
        if not gate_info:
            continue
        gate, targets, controls = gate_info
        x = 50 + col * (CELL_WIDTH + gate_spacing)  # add extra spacing

        # Draw control dots
        for c in controls:
            y = 30 + c * CELL_HEIGHT
            canvas.create_oval(x+15, y-5, x+25, y+5, fill=CONTROL_COLOR)

        # Draw vertical line connecting controls and targets
        if controls and targets:
            y1 = 30 + min(controls + targets) * CELL_HEIGHT
            y2 = 30 + max(controls + targets) * CELL_HEIGHT
            canvas.create_line(x+20, y1, x+20, y2, width=2)

        # Draw target gates
        for t in targets:
            y = 30 + t * CELL_HEIGHT
            canvas.create_rectangle(x-15, y-15, x+45, y+15, fill=GATE_COLOR, outline="black", width=2)
            canvas.create_text(x+15, y, text=gate, fill=TEXT_COLOR, font=("Arial", 10, "bold"))

    # Frame for state vector and probabilities
    info_frame = tk.Frame(root)
    info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    tk.Label(info_frame, text="Final State Vector:").grid(row=0, column=0, sticky="w")
    state_text = tk.Text(info_frame, height=2, width=80)
    state_text.grid(row=1, column=0, pady=5)
    state_text.insert(tk.END, str(circuit.state))
    state_text.config(state="disabled")

    tk.Label(info_frame, text="Probabilities of all basis states:").grid(row=2, column=0, sticky="w", pady=(10,0))
    prob_text = tk.Text(info_frame, height=2, width=80)
    prob_text.grid(row=3, column=0, pady=5)
    probabilities = np.abs(circuit.state.flatten())**2
    prob_text.insert(tk.END, str(probabilities))
    prob_text.config(state="disabled")

    root.mainloop()




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

    draw_circuit(circuit)

if __name__ == "__main__":
    main()
