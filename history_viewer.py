import tkinter as tk
from tkinter import scrolledtext

BG_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
FONT_FAMILY = "Consolas"
FONT_SIZE_NORMAL = 12

def show_history(root, circuit):
    """Open a scrollable history viewer for gate applications."""
    if not circuit.history:
        tk.messagebox.showinfo("Info", "No history yet. Apply some gates first.")
        return

    hist_window = tk.Toplevel(root)
    hist_window.title("History of Probabilities")
    hist_window.configure(bg=BG_COLOR)

    text_area = scrolledtext.ScrolledText(
        hist_window, wrap=tk.WORD, width=80, height=25,
        bg=BG_COLOR, fg=FG_COLOR, font=(FONT_FAMILY, FONT_SIZE_NORMAL)
    )
    text_area.pack(padx=10, pady=10, fill="both", expand=True)

    for step, (gate, probs, targets, controls) in enumerate(circuit.history):
        n = circuit.n
        labels = [format(i, f'0{n}b') for i in range(len(probs))]
        text_area.insert(tk.END, f"Step {step+1}: Gate {gate}, Targets={targets}, Controls={controls}\n")
        for l, p in zip(labels, probs):
            if p > 1e-6:  # only show significant probabilities
                text_area.insert(tk.END, f"   |{l}> : {p:.4f}\n")
        text_area.insert(tk.END, "\n")

    text_area.configure(state="disabled")
