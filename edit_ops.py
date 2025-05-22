import tkinter as tk
from tkinter import colorchooser

# Global font size tracker
current_font_size = 12  # Default font size


def add_edit_menu(menu, text_widget):
    edit_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Edit", menu=edit_menu)

    edit_menu.add_command(
        label="Cut", command=lambda: text_widget.event_generate("<<Cut>>"))
    edit_menu.add_command(
        label="Copy", command=lambda: text_widget.event_generate("<<Copy>>"))
    edit_menu.add_command(
        label="Paste", command=lambda: text_widget.event_generate("<<Paste>>"))

    def choose_font():
        text_widget.config(font=("Helvetica", current_font_size))

    def choose_text_color():
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:
            text_widget.config(fg=color[1])

    def choose_background_color():
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            text_widget.config(bg=color[1])

    def increase_font_size():
        global current_font_size
        current_font_size += 2
        text_widget.config(font=("Helvetica", current_font_size))

    def decrease_font_size():
        global current_font_size
        if current_font_size > 6:  # Prevent it from becoming unreadable
            current_font_size -= 2
            text_widget.config(font=("Helvetica", current_font_size))

    edit_menu.add_command(label="Font", command=choose_font)
    edit_menu.add_command(label="Text Color", command=choose_text_color)
    edit_menu.add_command(label="Background Color",
                          command=choose_background_color)
    edit_menu.add_separator()
    edit_menu.add_command(label="Increase Text Size",
                          command=increase_font_size)  # 🔺
    edit_menu.add_command(label="Decrease Text Size",
                          command=decrease_font_size)  # 🔻
