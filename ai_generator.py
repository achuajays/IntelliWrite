import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def add_ai_menu(menu, text_widget):
    ai_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="AI", menu=ai_menu)

    def generate_code():
        prompt = simpledialog.askstring("AI Code Generator", "Enter prompt:")
        if not prompt:
            return

        # Disable menu item while generating
        ai_menu.entryconfig("Generate Code", state="disabled")

        # Create a modal loading window
        loader = tk.Toplevel()
        loader.title("Loading...")
        loader.geometry("250x80")
        loader_label = tk.Label(loader, text="Generating AI code, please wait...")
        loader_label.pack(expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()  # modal window

        def run_generation():
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                # Insert the response in the main thread
                text_widget.after(0, lambda: text_widget.insert("end", f"\n\n# AI Code:\n{response.text.strip()}\n"))
            except Exception as e:
                text_widget.after(0, lambda: messagebox.showerror("AI Error", str(e)))
            finally:
                # Close loader and re-enable menu in main thread
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig("Generate Code", state="normal"))

        threading.Thread(target=run_generation, daemon=True).start()

    ai_menu.add_command(label="Generate Code", command=generate_code)
