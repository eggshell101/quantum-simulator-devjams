# quantum_simulator.py
import numpy as np

print("Enter: ", end="")
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
              [1, 0]], dtype=complex) #state flip or bit flip or not gate for qubit

Y = np.array([[0,-1j],
              [1j ,0]], dtype=complex) #pauli's y gate

Z = np.array([[1, 0],
              [0, -1]], dtype=complex) #phase flip

H = (1/np.sqrt(2)) * np.array([[1,  1],
                              [1, -1]], dtype=complex)

I = np.eye(2, dtype=complex)

# Build an n-qubit operator that applies `gate` to target_qubit (0 = leftmost / most significant)
def gate_on_n_qubits(gate, target_qubit, n_qubits):
    ops = []
    for i in range(n_qubits):
        if i == target_qubit:
            ops.append(gate)
        else:
            ops.append(I)
    return kron_list(ops)

# Apply a single-qubit gate to the state (returns new state)
def apply_single_qubit_gate(state, gate, target_qubit, n_qubits):
    U = gate_on_n_qubits(gate, target_qubit, n_qubits)
    return U @ state

# Controlled-NOT (control, target are indices; control=0 is leftmost qubit)
def cnot_on_n_qubits(control, target, n_qubits):
    dim = 2**n_qubits
    U = np.zeros((dim, dim), dtype=complex)
    # loop over basis states
    for i in range(dim):
        b = format(i, f'0{n_qubits}b')  # bitstring, leftmost is qubit 0
        bits = list(map(int, b))
        if bits[control] == 1:
            # flip target bit
            bits[target] ^= 1
        j = int(''.join(map(str, bits)), 2)
        U[j, i] = 1
    return U
def toffoli_on_n_qubits(control1, control2, target, n_qubits):
    dim = 2**n_qubits
    U = np.zeros((dim, dim), dtype=complex)
    # loop over basis states
    for i in range(dim):
        b = format(i, f'0{n_qubits}b')  # bitstring, leftmost is qubit 0
        bits = list(map(int, b))
        if bits[control1] == 1 and bits[control2] == 1:
            # flip target bit
            bits[target] ^= 1
        j = int(''.join(map(str, bits)), 2)
        U[j, i] = 1
    return U

# Measurement: returns (outcome_string, collapsed_state)
def measure(state, n_shots=1):
    """
    Perform projective measurement in computational basis.
    - If n_shots==1: returns (outcome, collapsed_state)
    - If n_shots>1: returns dict counts of outcomes
    """
    probs = np.abs(state.flatten())**2
    dim = probs.size
    outcomes = [format(i, f'0{int(np.log2(dim))}b') for i in range(dim)]
    if n_shots == 1:
        idx = np.random.choice(dim, p=probs)
        outcome = outcomes[idx]
        # collapsed state is basis vector
        collapsed = np.zeros_like(state)
        collapsed[idx, 0] = 1.0
        return outcome, collapsed
    else:
        choices = np.random.choice(outcomes, size=n_shots, p=probs)
        counts = {}
        for c in choices:
            counts[c] = counts.get(c, 0) + 1
        return counts

# Small demo: create Bell state
if __name__ == "__main__":

    # start |00>
    s = zero_state(n)
    # Apply H to qubit 0 (leftmost)
    s = apply_single_qubit_gate(s, H, target_qubit=0, n_qubits=n)
    # Apply CNOT with control 0 and target 1
    for i in range(1,n):
        U_cnot = cnot_on_n_qubits(control=0, target=i, n_qubits=n)
        s = U_cnot @ s
    s = normalize(s)
    print("Bell state vector:\n", s)
    print("Probabilities:", np.abs(s.flatten())**2)
    # Measure once
    outcome, collapsed = measure(s)
    print("Measurement outcome:", outcome)
    
U_cnot = cnot_on_n_qubits(control=0, target=2, n_qubits=n)
print(U_cnot )