# quantum_simulator.py
import numpy as np


n = int(input("Enter the number of qubits: "))
# Basic single-qubit states
zero = np.array([[1.0], [0.0]], dtype=complex)
one  = np.array([[0.0], [1.0]], dtype=complex)


def normalize(state):
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("Zero vector can't be normalized")
    return state / float(norm)
# Create an n-qubit zero state |00...0>
def zero_state(n):
    state = zero
    for _ in range(n-1):
        state = np.kron(state, zero)
    print(state)
    return state
zero_state(n)

# Tensor (Kronecker) product helper for lists
def kron_list(matrices):
    out = matrices[0]
    for m in matrices[1:]:
        out = np.kron(out, m)
    return out

# Common gates (single-qubit)
X = np.array([[0, 1],
              [1, 0]], dtype=complex) #state flip

Y = np.array([[0,-1j],
              [1j ,0]], dtype=complex) #pauli's y gate

Z = np.array([[1, 0],
              [0, -1]], dtype=complex) #phase flip

H = (1/np.sqrt(2)) * np.array([[1,  1],
                              [1, -1]], dtype=complex)