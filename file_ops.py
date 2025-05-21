import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

current_open_file = None
current_directory = os.getcwd()
autosave_interval = 5000  # 5 seconds

def add_file_menu(menu, root, text_widget, file_listbox=None):
    global current_open_file, current_directory

    fmenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=fmenu)

    def refresh_file_list(listbox):
        listbox.delete(0, "end")
        try:
            files = os.listdir(current_directory)
            for f in files:
                full_path = os.path.join(current_directory, f)
                if os.path.isfile(full_path):
                    listbox.insert("end", f)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot list files in {current_directory}:\n{e}")

    def open_folder():
        global current_directory
        folder = filedialog.askdirectory()
        if folder:
            current_directory = folder
            refresh_file_list(file_listbox)
            root.title(f"WISDOM NOTEPAD - {current_directory}")

    def load_file_content(event=None):
        selected = file_listbox.curselection()
        if selected:
            filename = file_listbox.get(selected[0])
            full_path = os.path.join(current_directory, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                text_widget.delete(1.0, "end")
                text_widget.insert("end", content)
                root.title(f"{filename} - WISDOM NOTEPAD")
                global current_open_file
                current_open_file = full_path
            except Exception as e:
                messagebox.showerror("File Load Error", str(e))

    def new_file():
        global current_open_file
        filename = simpledialog.askstring("New File", "Enter new file name:")
        if filename:
            full_path = os.path.join(current_directory, filename)
            if os.path.exists(full_path):
                messagebox.showerror("Error", "File already exists!")
                return
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write("")  # create empty file
                current_open_file = full_path
                text_widget.delete(1.0, "end")
                root.title(f"{filename} - WISDOM NOTEPAD")
                if file_listbox:
                    refresh_file_list(file_listbox)
            except Exception as e:
                messagebox.showerror("File Creation Error", str(e))

    def open_file():
        global current_open_file
        filename = filedialog.askopenfilename(initialdir=current_directory)
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                current_open_file = filename
                text_widget.delete(1.0, "end")
                text_widget.insert("end", content)
                root.title(f"{os.path.basename(filename)} - WISDOM NOTEPAD")
                if file_listbox:
                    refresh_file_list(file_listbox)
            except Exception as e:
                messagebox.showerror("Open File Error", str(e))

    def save_file():
        global current_open_file
        if current_open_file and os.path.exists(current_open_file):
            try:
                content = text_widget.get(1.0, "end-1c")
                with open(current_open_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                messagebox.showerror("Save Error", str(e))
        else:
            save_as()

    def save_as():
        global current_open_file
        filename = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=current_directory)
        if filename:
            try:
                content = text_widget.get(1.0, "end-1c")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                current_open_file = filename
                root.title(f"{os.path.basename(filename)} - WISDOM NOTEPAD")
                if file_listbox:
                    refresh_file_list(file_listbox)
            except Exception as e:
                messagebox.showerror("Save As Error", str(e))

    fmenu.add_command(label="New", command=new_file)
    fmenu.add_command(label="Open", command=open_file)
    fmenu.add_command(label="Open Folder", command=open_folder)  # NEW
    fmenu.add_command(label="Save", command=save_file)
    fmenu.add_command(label="Save As", command=save_as)
    fmenu.add_separator()
    fmenu.add_command(label="Exit", command=root.quit)

    if file_listbox:
        file_listbox.bind("<<ListboxSelect>>", load_file_content)
        refresh_file_list(file_listbox)
