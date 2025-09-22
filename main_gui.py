import tkinter as tk
from tkinter import messagebox
from gui_version6 import start_quantum_gui, start_quantum_gui_with_bell_state
from bloch_sphere_2 import run_bloch_simulator

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quantum Simulator")
        self.geometry("400x300")

        self.n_qubits = None

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.welcome_frame = tk.Frame(self)
        self.welcome_frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = tk.Label(self.welcome_frame, text="Quantum Simulator", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(10, 0))

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to the quantum simulator.")
        welcome_label.pack(pady=(0, 20))

        label = tk.Label(self.welcome_frame, text="Enter the number of qubits:")
        label.pack(pady=5)

        self.qubit_entry = tk.Entry(self.welcome_frame)
        self.qubit_entry.pack(pady=5)

        init_button = tk.Button(self.welcome_frame, text="Initialise Qbits", command=self.finalize_qubits)
        init_button.pack(pady=10)

    def finalize_qubits(self):
        try:
            n_qubits = int(self.qubit_entry.get())
            if n_qubits <= 0:
                raise ValueError
            self.n_qubits = n_qubits
            self.welcome_frame.destroy()
            self.show_main_menu()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid positive integer for the number of qubits.")

    def show_main_menu(self):
        self.main_menu_frame = tk.Frame(self)
        self.main_menu_frame.pack(pady=20)

        operations_button = tk.Button(self.main_menu_frame, text="Operations on qbits", command=self.open_operations)
        operations_button.pack(pady=10)

        bloch_sphere_button = tk.Button(self.main_menu_frame, text="View Bloch's Sphere", command=self.open_bloch_sphere)
        bloch_sphere_button.pack(pady=10)

        bell_state_button = tk.Button(self.main_menu_frame, text="Bell State", command=self.open_bell_state)
        bell_state_button.pack(pady=10)

        bell_state_button = tk.Button(self.main_menu_frame, text="All gates used", command=self.open_gates_used)
        bell_state_button.pack(pady=10)

    def open_operations(self):
        start_quantum_gui(self, self.n_qubits)

    def open_bloch_sphere(self):
        run_bloch_simulator() 

    def open_bell_state(self):
        if self.n_qubits < 2:
            messagebox.showerror("Error", "Bell state requires at least 2 qubits.")
        else:
            start_quantum_gui_with_bell_state(self, self.n_qubits)
        
    def open_gates_used(self):
        from Basic_1 import cnot_on_n_qubits, toffoli_on_n_qubits, H, X, Y, Z

        # New window
        gate_window = tk.Toplevel(self)
        gate_window.title("Quantum Gates")
        gate_window.geometry("600x600")

        text_widget = tk.Text(gate_window, wrap="word", font=("Courier", 10))
        text_widget.pack(fill="both", expand=True)

        def matrix_to_string(mat):
            return "\n".join(["  ".join([f"{val.real:.2f}{val.imag:+.2f}j" if isinstance(val, complex) else str(val)
                                         for val in row]) for row in mat])

        # Add gates one by one
        text_widget.insert("end", "Hadamard (H):\n")
        text_widget.insert("end", matrix_to_string(H) + "\n\n")

        text_widget.insert("end", "Pauli-X (X):\n")
        text_widget.insert("end", matrix_to_string(X) + "\n\n")

        text_widget.insert("end", "Pauli-Y (Y):\n")
        text_widget.insert("end", matrix_to_string(Y) + "\n\n")

        text_widget.insert("end", "Pauli-Z (Z):\n")
        text_widget.insert("end", matrix_to_string(Z) + "\n\n")

        text_widget.insert("end", "CNOT (2 qubits, control=0, target=1):\n")
        text_widget.insert("end", matrix_to_string(cnot_on_n_qubits(0, 1, 2)) + "\n\n")

        text_widget.insert("end", "Toffoli (3 qubits, controls=0,1 target=2):\n")
        text_widget.insert("end", matrix_to_string(toffoli_on_n_qubits(0, 1, 2, 3)) + "\n\n")

        text_widget.config(state="disabled")  # make read-only




if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
