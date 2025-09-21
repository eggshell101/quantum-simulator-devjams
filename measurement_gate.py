import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog
from Basic_1 import zero_state, apply_single_qubit_gate, cnot_on_n_qubits, toffoli_on_n_qubits, H, X, Y, Z
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

CELL_WIDTH = 80
CELL_HEIGHT = 50
GATE_COLOR = "#87CEFA"
CONTROL_COLOR = "#FF6347"
MEASURE_COLOR = "#90EE90"  # Light green for measurement
TEXT_COLOR = "black"
GATE_SPACING = 30


class Circuit:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.state = zero_state(n_qubits)
        self.diagram = []  # (gate, targets, controls)
        self.step_index = -1
        self.measurements = {}  # {qubit: result}

    def add_gate(self, gate, targets, controls=[]):
        self.diagram.append((gate, targets, controls))

    def apply_gate(self, index):
        if index >= len(self.diagram):
            return
        gate, targets, controls = self.diagram[index]

        if gate in ["H", "X", "Y", "Z"]:
            self.state = apply_single_qubit_gate(
                self.state, {"H": H, "X": X, "Y": Y, "Z": Z}[gate],
                targets[0], self.n
            )

        elif gate == "CNOT":
            self.state = cnot_on_n_qubits(
                control=controls[0], target=targets[0], n_qubits=self.n
            ) @ self.state

        elif gate == "TOFFOLI":
            self.state = toffoli_on_n_qubits(
                control1=controls[0], control2=controls[1],
                target=targets[0], n_qubits=self.n
            ) @ self.state

        elif gate == "MEASURE":
            q = targets[0]
            probs = np.abs(self.state.flatten())**2
            outcome = self.measure_qubit(probs, q)
            self.measurements[q] = outcome
            # collapse state
            self.state = self.collapse_state(q, outcome)

    def measure_qubit(self, probs, qubit):
        """Simulate measuring one qubit"""
        n = self.n
        outcome_probs = [0, 0]
        for i, p in enumerate(probs):
            bit = (i >> (n-1-qubit)) & 1
            outcome_probs[bit] += p
        return 0 if random.random() < outcome_probs[0] else 1

    def collapse_state(self, qubit, outcome):
        """Collapse state vector given a measurement result"""
        n = self.n
        new_state = self.state.copy()
        for i in range(len(new_state)):
            bit = (i >> (n-1-qubit)) & 1
            if bit != outcome:
                new_state[i] = 0
        norm = np.linalg.norm(new_state)
        return new_state / norm if norm > 0 else new_state

    def reset(self):
        self.state = zero_state(self.n)
        self.step_index = -1
        self.measurements = {}


class QuantumGUI:
    def __init__(self, root, circuit: Circuit):
        self.root = root
        self.circuit = circuit
        self.root.title("Quantum Circuit Simulator")
        self.scale = 1.0

        # Toolbox
        self.toolbox_frame = tk.Frame(root)
        self.toolbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.create_toolbox()

        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=circuit.n * CELL_HEIGHT + 100)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)

        # Controls
        self.control_frame = tk.Frame(root)
        self.control_frame.grid(row=2, column=0, pady=10, sticky="w")

        self.prev_button = tk.Button(self.control_frame, text="Previous Gate", command=self.prev_gate)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.control_frame, text="Next Gate", command=self.next_gate)
        self.next_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_circuit)
        self.reset_button.grid(row=0, column=2, padx=5)

        # Probabilities
        self.fig, self.ax = plt.subplots(figsize=(6, 2))
        self.prob_canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.prob_canvas.get_tk_widget().grid(row=3, column=0)

        # Measurement results
        self.measure_label = tk.Label(root, text="Measurements: None")
        self.measure_label.grid(row=4, column=0, pady=10)

        self.update_canvas()

    def create_toolbox(self):
        gates = ["H", "X", "Y", "Z", "CNOT", "TOFFOLI", "MEASURE"]
        for i, g in enumerate(gates):
            b = tk.Button(self.toolbox_frame, text=g, width=8,
                          command=lambda gate=g: self.add_gate_gui(gate))
            b.grid(row=0, column=i, padx=5)

    def add_gate_gui(self, gate):
        n = self.circuit.n
        if gate in ["H", "X", "Y", "Z", "MEASURE"]:
            target = self.ask_qubit(f"Select target qubit (0 to {n-1}) for {gate}:")
            if target is None: return
            self.circuit.add_gate(gate, targets=[target])
        elif gate == "CNOT":
            control = self.ask_qubit(f"Select control qubit (0 to {n-1}) for CNOT:")
            if control is None: return
            target = self.ask_qubit(f"Select target qubit (0 to {n-1}) for CNOT:")
            if target is None: return
            self.circuit.add_gate(gate, targets=[target], controls=[control])
        elif gate == "TOFFOLI":
            c1 = self.ask_qubit(f"Select first control qubit (0 to {n-1}) for TOFFOLI:")
            if c1 is None: return
            c2 = self.ask_qubit(f"Select second control qubit (0 to {n-1}) for TOFFOLI:")
            if c2 is None: return
            target = self.ask_qubit(f"Select target qubit (0 to {n-1}) for TOFFOLI:")
            if target is None: return
            self.circuit.add_gate(gate, targets=[target], controls=[c1, c2])
        self.update_canvas()

    def ask_qubit(self, prompt):
        answer = simpledialog.askinteger("Input", prompt)
        n = self.circuit.n
        if answer is None or not (0 <= answer < n):
            messagebox.showwarning("Invalid Input", f"Please enter a number between 0 and {n-1}")
            return None
        return answer

    def update_canvas(self):
        self.canvas.delete("all")
        n = self.circuit.n

        # Wires
        for i in range(n):
            y = 30 + i * CELL_HEIGHT
            self.canvas.create_line(50, y, 50 + len(self.circuit.diagram) * (CELL_WIDTH + GATE_SPACING), y, width=2)

        # Gates
        for col, (gate, targets, controls) in enumerate(self.circuit.diagram):
            x = 50 + col * (CELL_WIDTH + GATE_SPACING)
            for c in controls:
                y = 30 + c * CELL_HEIGHT
                self.canvas.create_oval(x+15, y-5, x+25, y+5, fill=CONTROL_COLOR)

            for t in targets:
                y = 30 + t * CELL_HEIGHT
                if gate == "MEASURE":
                    self.canvas.create_rectangle(x-15, y-15, x+45, y+15,
                                                 fill=MEASURE_COLOR, outline="black", width=2)
                    self.canvas.create_text(x+15, y, text="M", font=("Arial", 10, "bold"))
                else:
                    self.canvas.create_rectangle(x-15, y-15, x+45, y+15,
                                                 fill=GATE_COLOR, outline="black", width=2)
                    self.canvas.create_text(x+15, y, text=gate, font=("Arial", 10, "bold"))

        self.update_probabilities()
        self.update_measurements()

    def update_probabilities(self):
        self.ax.clear()
        probs = np.abs(self.circuit.state.flatten())**2
        self.ax.bar(range(len(probs)), probs)
        self.ax.set_ylim(0, 1)
        self.ax.set_ylabel("Probability")
        self.ax.set_xlabel("Basis state")
        self.prob_canvas.draw()

    def update_measurements(self):
        if self.circuit.measurements:
            text = ", ".join([f"q{q}={r}" for q, r in self.circuit.measurements.items()])
        else:
            text = "None"
        self.measure_label.config(text=f"Measurements: {text}")

    def next_gate(self):
        if self.circuit.step_index + 1 >= len(self.circuit.diagram):
            messagebox.showinfo("Info", "No more gates to apply.")
            return
        self.circuit.step_index += 1
        self.circuit.apply_gate(self.circuit.step_index)
        self.update_canvas()

    def prev_gate(self):
        if self.circuit.step_index < 0:
            messagebox.showinfo("Info", "At initial state.")
            return
        self.circuit.reset()
        for i in range(self.circuit.step_index):
            self.circuit.apply_gate(i)
        self.circuit.step_index -= 1
        self.update_canvas()

    def reset_circuit(self):
        self.circuit.reset()
        self.update_canvas()


if __name__ == "__main__":
    n = int(input("Enter number of qubits: "))
    circuit = Circuit(n)
    root = tk.Tk()
    gui = QuantumGUI(root, circuit)
    root.mainloop()
