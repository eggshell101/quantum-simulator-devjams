import numpy as np
from Basic_1 import (
    zero_state,
    apply_single_qubit_gate,
    cnot_on_n_qubits,
    toffoli_on_n_qubits,
    H, X, Y, Z,
    n
)

def main():
    gates = ["H", "X", "Y", "Z", "CNOT", "TOFFOLI"]
    print('hello from meow meow quantum')
    # initialize |00...0⟩
    s = zero_state(n)

    while True:
        gate = input("Apply gate (H, X, Y, Z, CNOT, TOFFOLI) or Q to quit: ").strip().upper()
        if gate == "Q":
            break
        elif gate not in gates:
            print(f"Invalid gate: {gate}")
            continue

        if gate in ["H", "X", "Y", "Z"]:
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            if gate == "H":
                s = apply_single_qubit_gate(s, H, target, n)
            elif gate == "X":
                s = apply_single_qubit_gate(s, X, target, n)
            elif gate == "Y":
                s = apply_single_qubit_gate(s, Y, target, n)
            elif gate == "Z":
                s = apply_single_qubit_gate(s, Z, target, n)

        elif gate == "CNOT":
            control = int(input(f"Enter control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            U = cnot_on_n_qubits(control, target, n)
            s = U @ s

        elif gate == "TOFFOLI":
            c1 = int(input(f"Enter first control qubit (0 to {n-1}): "))
            c2 = int(input(f"Enter second control qubit (0 to {n-1}): "))
            target = int(input(f"Enter target qubit (0 to {n-1}): "))
            U = toffoli_on_n_qubits(c1, c2, target, n)
            s = U @ s

        show = input("Show state? (y/n): ").strip().lower()
        if show == "y":
            print("Current state vector:\n", s)
            probs = np.abs(s.flatten())**2
            print("Probabilities:", probs)

if __name__ == "__main__":
    main()