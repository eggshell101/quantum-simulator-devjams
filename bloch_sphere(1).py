import tkinter as tk
from tkinter import Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Function to draw Bloch sphere
def draw_bloch(ax, vector, title):
    # Sphere surface
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:20j]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color="skyblue", alpha=0.1, edgecolor="gray")

    # Axes with labels
    ax.quiver(0,0,0,1,0,0,color="purple",linewidth=1.5)  # X
    ax.quiver(0,0,0,0,1,0,color="green",linewidth=1.5)  # Y
    ax.quiver(0,0,0,0,0,1,color="red",linewidth=1.5)    # Z
    ax.text(1.1,0,0,'X', color='purple', fontsize=12)
    ax.text(0,1.1,0,'Y', color='green', fontsize=12)
    ax.text(0,0,1.1,'Z', color='red', fontsize=12)

    # State vector
    ax.quiver(0,0,0,vector[0],vector[1],vector[2],color="black",linewidth=2)

    # Formatting
    ax.set_xlim([-1,1]); ax.set_ylim([-1,1]); ax.set_zlim([-1,1])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_box_aspect([1,1,1])

    # Remove background planes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Label at the bottom
    ax.text2D(0.5, -0.05, "Black arrow = state vector", transform=ax.transAxes, 
              ha="center", fontsize=10)

# Function to show Bloch sphere for a gate or qubit state
def show_bloch(name):
    new_win = Toplevel(root)
    new_win.title(f"{name} - Bloch Sphere")

    fig = plt.Figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')

    # Define vectors
    if name == "Qubit - |0>":
        vec = np.array([0,0,1])
        title = "|0> Qubit State"
    elif name == "Qubit - |1>":
        vec = np.array([0,0,-1])
        title = "|1> Qubit State"
    else:
        gate_vectors = {
            "Hadamard": np.array([1,0,0]),
            "Pauli-X": np.array([0,0,-1]),
            "Pauli-Y": np.array([0,1,0]),
            "Pauli-Z": np.array([0,0,1])
        }
        vec = gate_vectors[name]
        title = name

    draw_bloch(ax, vec, title)
    ax.set_title(title, fontsize=14, pad=20)

    canvas = FigureCanvasTkAgg(fig, master=new_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Tkinter main window
root = tk.Tk()
root.title("Quantum Gates - Bloch Sphere Viewer")
root.geometry("400x400")

tk.Label(root, text="Select a Quantum Gate / Qubit", font=("Arial", 16)).pack(pady=20)

# Buttons for gates and qubits
for name in ["Hadamard", "Pauli-X", "Pauli-Y", "Pauli-Z", "Qubit - |0>", "Qubit - |1>"]:
    btn = tk.Button(root, text=name, font=("Arial",14), width=20,
                    command=lambda n=name: show_bloch(n))
    btn.pack(pady=5)

root.mainloop()
