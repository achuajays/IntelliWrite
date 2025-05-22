import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from google import genai
from config import GEMINI_API_KEY
import os
import webbrowser

client = genai.Client(api_key=GEMINI_API_KEY)


def add_ai_menu(menu, text_widget):
    ai_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="AI", menu=ai_menu)

    def generate_code():
        prompt = simpledialog.askstring("AI Code Generator", "Enter prompt:")
        if not prompt:
            return

        ai_menu.entryconfig("Generate Code", state="disabled")
        loader = tk.Toplevel()
        loader.title("Loading...")
        loader.geometry("250x80")
        tk.Label(loader, text="Generating AI code, please wait...").pack(
            expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_generation():
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                text_widget.after(0, lambda: text_widget.insert(
                    "end", f"\n\n# AI Code:\n{response.text.strip()}\n"))
            except Exception as e:
                text_widget.after(
                    0, lambda: messagebox.showerror("AI Error", str(e)))
            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig(
                    "Generate Code", state="normal"))

        threading.Thread(target=run_generation, daemon=True).start()

    def review_code():
        code = text_widget.get("1.0", "end").strip()
        if not code:
            messagebox.showinfo("Code Review", "The editor is empty.")
            return

        ai_menu.entryconfig("Review Code", state="disabled")
        loader = tk.Toplevel()
        loader.title("Reviewing...")
        loader.geometry("250x80")
        tk.Label(loader, text="Reviewing code, please wait...").pack(
            expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_review():
            try:
                prompt = f"Please review the following code and provide suggestions for improvements, errors, or optimizations:\n\n{code}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                review = response.text.strip()

                def show_review():
                    review_window = tk.Toplevel()
                    review_window.title("AI Code Review")
                    review_window.geometry("600x400")

                    review_text = tk.Text(review_window, wrap="word")
                    review_text.insert("1.0", review)
                    review_text.config(state="disabled")
                    review_text.pack(fill="both", expand=True)

                text_widget.after(0, show_review)
            except Exception as e:
                text_widget.after(0, lambda err=e: messagebox.showerror(
                    "AI Review Error", str(err)))

            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig(
                    "Review Code", state="normal"))

        threading.Thread(target=run_review, daemon=True).start()

    def generate_learning_roadmap():
        topic = simpledialog.askstring(
            "Learning Roadmap", "Enter a topic to generate a roadmap:")
        if not topic:
            return

        ai_menu.entryconfig("Generate Learning Roadmap", state="disabled")
        loader = tk.Toplevel()
        loader.title("Generating Roadmap...")
        loader.geometry("300x80")
        tk.Label(loader, text="Please wait while the roadmap is being generated...").pack(
            expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_roadmap():
            try:
                prompt = f"Create a detailed, structured learning roadmap to master the topic: '{topic}'. Include stages, key concepts, tools, and timeframes."
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                roadmap = response.text.strip()

                # Save to file
                file_path = os.path.join(os.getcwd(), "readme_roadmap.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(roadmap)

                # Notify user
                text_widget.after(0, lambda: messagebox.showinfo(
                    "Roadmap Saved", f"Roadmap saved to:\n{file_path}"))
            except Exception as e:
                text_widget.after(0, lambda err=e: messagebox.showerror(
                    "AI Roadmap Error", str(err)))
            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig(
                    "Generate Learning Roadmap", state="normal"))

        threading.Thread(target=run_roadmap, daemon=True).start()

    def search_topic_in_chrome():
        topic = simpledialog.askstring(
            "Search Topic", "Enter a topic to search in Chrome:")
        if topic:
            query = topic.replace(" ", "+")
            url = f"https://www.google.com/search?q={query}"
            try:
                # You can specify Chrome directly if needed:
                # webbrowser.get("chrome").open(url)
                webbrowser.open(url)
            except webbrowser.Error:
                messagebox.showerror(
                    "Error", "Could not open Chrome. Make sure it is installed and accessible.")

    ai_menu.add_command(label="Generate Code", command=generate_code)
    ai_menu.add_command(label="Review Code", command=review_code)
    ai_menu.add_command(label="Generate Learning Roadmap",
                        command=generate_learning_roadmap)
    ai_menu.add_command(label="Search Topic in Chrome",
                        command=search_topic_in_chrome)  # 🌐 New
