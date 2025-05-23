import os
import tkinter as tk
from tkinter import messagebox

from editor import create_editor
from file_ops import add_file_menu
from edit_ops import add_edit_menu
from ai_generator import add_ai_menu
from terminal_ops import add_terminal_menu

import tkinter as tk
from tkinter import ttk
import os


def create_file_listbox(root, text_widget):
    frame = tk.Frame(root)
    frame.pack(side="left", fill="y")

    label = tk.Label(frame, text="Files in current directory")
    label.pack(pady=5)

    listbox = tk.Listbox(frame, width=30)
    listbox.pack(fill="y", expand=True)

    def load_file_content(event=None):
        selected = listbox.curselection()
        if selected:
            filename = listbox.get(selected[0])
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                text_widget.delete(1.0, "end")
                text_widget.insert("end", content)
                root.title(f"{filename} - WISDOM NOTEPAD")
            except Exception as e:
                messagebox.showerror("File Load Error", str(e))

    listbox.bind("<<ListboxSelect>>", load_file_content)

    def refresh_file_list():
        listbox.delete(0, "end")
        for f in os.listdir():
            if os.path.isfile(f):
                listbox.insert("end", f)

    refresh_button = tk.Button(
        frame, text="Refresh", command=refresh_file_list)
    refresh_button.pack(pady=5)

    refresh_file_list()
    return frame, listbox


def create_folder_tree(root, text_widget):
    frame = tk.Frame(root)
    frame.pack(side="right", fill="y")

    label = tk.Label(frame, text="Folder Browser")
    label.pack(pady=5)

    tree = ttk.Treeview(frame)
    tree.pack(fill="y", expand=True)

    def insert_node(parent, path):
        try:
            for item in os.listdir(path):
                abs_path = os.path.join(path, item)
                isdir = os.path.isdir(abs_path)
                node = tree.insert(parent, "end", text=item,
                                   open=False, values=[abs_path])
                if isdir:
                    tree.insert(node, "end", text="Loading...")
        except PermissionError:
            pass

    # Add root node
    cwd = os.getcwd()
    root_node = tree.insert("", "end", text=cwd, open=True, values=[cwd])
    insert_node(root_node, cwd)

    def open_node(event):
        node = tree.focus()
        children = tree.get_children(node)
        # If first child is dummy, remove and populate real children
        if children:
            first_child_text = tree.item(children[0], "text")
            if first_child_text == "Loading...":
                tree.delete(children[0])
                path = tree.item(node, "values")[0]
                insert_node(node, path)

    def on_node_select(event):
        node = tree.focus()
        path = tree.item(node, "values")[0]
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                text_widget.delete(1.0, "end")
                text_widget.insert("end", content)
                root.title(f"{path} - WISDOM NOTEPAD")
                global current_open_file
                current_open_file = path
            except Exception as e:
                tk.messagebox.showerror("File Load Error", str(e))

    insert_node(root_node, os.path.abspath(os.sep))
    tree.bind("<<TreeviewOpen>>", open_node)
    tree.bind("<<TreeviewSelect>>", on_node_select)

    return frame


def main():
    root = tk.Tk()
    root.title("WISDOM NOTEPAD")
    root.geometry("1200x600")

    # Create text widget and file list
    text_widget = create_editor(root)
    file_frame, file_listbox = create_file_listbox(root, text_widget)

    file_frame.pack(side="left", fill="y")
    text_widget.pack(side="left", fill="both", expand=True)

    # Create folder tree on right
    folder_frame = create_folder_tree(root, text_widget)
    folder_frame.pack(side="right", fill="y")

    # 🔧 Define menubar before using it
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # ✅ These must come after menubar is created
    add_file_menu(menubar, root, text_widget, file_listbox)
    add_edit_menu(menubar, text_widget)
    add_ai_menu(menubar, text_widget)
    add_terminal_menu(menubar, root)  # This line now works correctly


    root.mainloop()


if __name__ == "__main__":
    main()
