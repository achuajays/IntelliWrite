import subprocess
import platform
import tkinter as tk
from tkinter import scrolledtext, messagebox


def open_embedded_terminal(root):
    terminal_window = tk.Toplevel(root)
    terminal_window.title("Embedded Terminal")
    terminal_window.geometry("800x400")

    output_text = scrolledtext.ScrolledText(
        terminal_window, bg="black", fg="lime", insertbackground="white")
    output_text.pack(fill="both", expand=True)

    input_entry = tk.Entry(terminal_window, bg="black",
                           fg="white", insertbackground="white")
    input_entry.pack(fill="x")

    def run_command(event=None):
        cmd = input_entry.get()
        input_entry.delete(0, tk.END)
        if cmd.strip().lower() == "exit":
            terminal_window.destroy()
            return
        try:
            result = subprocess.check_output(
                cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = e.output
        output_text.insert(tk.END, f"> {cmd}\n{result}\n")
        output_text.see(tk.END)

    input_entry.bind("<Return>", run_command)
    input_entry.focus()


def open_system_terminal():
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.Popen("start cmd", shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Terminal"])
        else:
            subprocess.Popen(["gnome-terminal"])  # Linux
    except Exception as e:
        messagebox.showerror(
            "Terminal Error", f"Could not open terminal:\n{str(e)}")


def add_terminal_menu(menu, root):
    terminal_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Terminal", menu=terminal_menu)

    terminal_menu.add_command(
        label="Open Embedded Terminal", command=lambda: open_embedded_terminal(root))
    terminal_menu.add_command(
        label="Open System Terminal", command=open_system_terminal)
