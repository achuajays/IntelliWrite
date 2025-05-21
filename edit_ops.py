import tkinter as tk
from tkinter import colorchooser

def add_edit_menu(menu, text_widget):
    edit_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=edit_menu)

    edit_menu.add_command(label="Cut", command=lambda: text_widget.event_generate("<<Cut>>"))
    edit_menu.add_command(label="Copy", command=lambda: text_widget.event_generate("<<Copy>>"))
    edit_menu.add_command(label="Paste", command=lambda: text_widget.event_generate("<<Paste>>"))

    def choose_font():
        # Simple font chooser (you can expand this with tkinter.font or tkfontchooser)
        text_widget.config(font=("Helvetica", 12))

    def choose_color():
        color = colorchooser.askcolor()
        if color[1]:
            text_widget.config(fg=color[1])

    edit_menu.add_command(label="Font", command=choose_font)
    edit_menu.add_command(label="Text Color", command=choose_color)
