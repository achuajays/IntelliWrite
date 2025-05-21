import tkinter as tk

def create_editor(root):
    text = tk.Text(root, undo=True, wrap="word", bg="aqua", fg="black")
    text.pack(fill="both", expand=1)
    return text
