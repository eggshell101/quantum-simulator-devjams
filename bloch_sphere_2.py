import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import Axes3D

def run_bloch_simulator():
# Qubit states
    states = {
        '|0⟩': np.array([[1], [0]], dtype=complex),
        '|1⟩': np.array([[0], [1]], dtype=complex),
        '|+⟩': (1 / np.sqrt(2)) * np.array([[1], [1]], dtype=complex),
        '|−⟩': (1 / np.sqrt(2)) * np.array([[1], [-1]], dtype=complex),
        '|i⟩': (1 / np.sqrt(2)) * np.array([[1], [1j]], dtype=complex),
        '|−i⟩': (1 / np.sqrt(2)) * np.array([[1], [-1j]], dtype=complex)
    }

    # Basic gates
    gates = {
        'X': np.array([[0, 1], [1, 0]], dtype=complex),
        'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
        'Z': np.array([[1, 0], [0, -1]], dtype=complex),
        'H': (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
    }

    current_state = states['|0⟩']


    # Compute Bloch vector
    def bloch_vector(state):
        alpha, beta = state[0, 0], state[1, 0]
        x = 2 * np.real(np.conj(alpha) * beta)
        y = 2 * np.imag(np.conj(alpha) * beta)
        z = np.abs(alpha) ** 2 - np.abs(beta) ** 2
        return np.array([x, y, z])


    # Draw Bloch Sphere
    def draw_bloch(state, ax):
        ax.clear()
        vec = bloch_vector(state)

        # Sphere grid
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 30)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones_like(u), np.cos(v))
        ax.plot_wireframe(x, y, z, color='c', alpha=0.3, linewidth=0.5)

        # Axes arrows
        ax.quiver(0, 0, 0, 1, 0, 0, color='r', arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 1, 0, color='g', arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 0, 1, color='b', arrow_length_ratio=0.1)

        # Axes labels
        ax.text(1.2, 0, 0, 'X', color='r', fontsize=12)
        ax.text(0, 1.1, 0, 'Y', color='g', fontsize=12)
        ax.text(0, 0, 1.1, 'Z', color='b', fontsize=12)

        # Basis labels
        ax.text(0, 0, 1.3, '|0⟩', color='b', fontsize=12)
        ax.text(0, 0, -1.3, '|1⟩', color='b', fontsize=12)

        # Bloch vector
        ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color='k', linewidth=2, arrow_length_ratio=0.2)
        ax.text(vec[0] * 1.5, vec[1] * 1.5, vec[2] * 1.5, 'Ψ', color='k', fontsize=12)

        ax.set_xlim([-1.2, 1.2]);
        ax.set_ylim([-1.2, 1.2]);
        ax.set_zlim([-1.2, 1.2])
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(30, 45)
        plt.draw()


    # Button callbacks
    def set_state(label):
        global current_state
        current_state = states[label]
        draw_bloch(current_state, ax)


    def apply_gate(label):
        global current_state
        current_state = np.dot(gates[label], current_state)
        draw_bloch(current_state, ax)


    # Create figure
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.35)

    # Initial draw
    draw_bloch(current_state, ax)

    # Add state buttons
    state_labels = list(states.keys())
    button_objects = []
    for i, label in enumerate(state_labels):
        ax_btn = plt.axes([0.1 + i * 0.13, 0.2, 0.12, 0.075], facecolor='#88c0d0')
        btn = Button(ax_btn, label, color='#88c0d0', hovercolor='#5e81ac')
        btn.on_clicked(lambda event, lbl=label: set_state(lbl))  # Correct binding
        button_objects.append(btn)

    # Add gate buttons
    gate_labels = list(gates.keys())
    for i, label in enumerate(gate_labels):
        ax_btn = plt.axes([0.1 + i * 0.13, 0.1, 0.12, 0.075], facecolor='#a3be8c')
        btn = Button(ax_btn, label, color='#a3be8c', hovercolor='#81a67f')
        btn.on_clicked(lambda event, lbl=label: apply_gate(lbl))  # Correct binding
        button_objects.append(btn)

    plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Bloch Sphere GUI")

    btn = tk.Button(root, text="Show Two Bloch Spheres", command=lambda: run_bloch_simulator)
    btn.pack(pady=20)

    root.mainloop()
