import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
from google import genai
from config import GEMINI_API_KEY
import os
import webbrowser
import difflib

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
                webbrowser.open(url)
            except webbrowser.Error:
                messagebox.showerror(
                    "Error", "Could not open browser. Ensure it's installed.")

    def generate_unit_tests():
        code = text_widget.get("1.0", "end").strip()
        if not code:
            messagebox.showinfo("Generate Tests", "No code to test.")
            return
        ai_menu.entryconfig("Generate Unit Tests", state="disabled")
        loader = tk.Toplevel()
        loader.title("Generating Tests...")
        loader.geometry("250x80")
        tk.Label(loader, text="Generating test cases...").pack(
            expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_tests():
            try:
                prompt = f"Write Python unittests for the following code using unittest or pytest:\n\n{code}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                tests = response.text.strip()
                tests_file = os.path.join(os.getcwd(), "test_generated.py")
                with open(tests_file, "a", encoding="utf-8") as f:
                    f.write("\n\n" + tests + "\n")
                text_widget.after(0, lambda: messagebox.showinfo(
                    "Tests Generated", f"Test cases appended to {tests_file}"))
            except Exception as e:
                text_widget.after(0, lambda err=e: messagebox.showerror(
                    "Test Generation Error", str(err)))
            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig(
                    "Generate Unit Tests", state="normal"))

        threading.Thread(target=run_tests, daemon=True).start()

    def analyze_and_fix_code():
        original = text_widget.get("1.0", "end").strip()
        if not original:
            messagebox.showinfo("Analyze & Fix", "Editor is empty.")
            return
        ai_menu.entryconfig("Analyze & Auto-Fix Code", state="disabled")
        loader = tk.Toplevel()
        loader.title("Analyzing...")
        loader.geometry("250x80")
        tk.Label(loader, text="Analyzing and fixing code...").pack(
            expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_fix():
            try:
                prompt = f"Find bugs or inefficiencies in this Python code and correct them:\n\n{original}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                fixed = response.text.strip()
                diff = "\n".join(difflib.unified_diff(
                    original.splitlines(), fixed.splitlines(), lineterm=""))

                def show_diff():
                    diff_win = tk.Toplevel()
                    diff_win.title("Code Diff Preview")
                    diff_win.geometry("600x400")
                    diff_text = tk.Text(diff_win, wrap="none")
                    diff_text.insert("1.0", diff)
                    diff_text.config(state="disabled")
                    diff_text.pack(fill="both", expand=True)
                    # Optionally apply fix
                    def apply_fix():
                        text_widget.delete("1.0", "end")
                        text_widget.insert("end", fixed)
                        diff_win.destroy()
                    tk.Button(diff_win, text="Apply Fix", command=apply_fix).pack(pady=5)

                text_widget.after(0, show_diff)
            except Exception as e:
                text_widget.after(0, lambda err=e: messagebox.showerror(
                    "Fix Error", str(err)))
            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig(
                    "Analyze & Auto-Fix Code", state="normal"))

        threading.Thread(target=run_fix, daemon=True).start()

    def explain_selected_code():
        try:
            # get the selected code range
            start = text_widget.index(tk.SEL_FIRST)
            end = text_widget.index(tk.SEL_LAST)
            code = text_widget.get(start, end).strip()
        except tk.TclError:
            messagebox.showinfo("Explain Code", "No code selected.")
            return

        ai_menu.entryconfig("Explain Selected Code", state="disabled")
        loader = tk.Toplevel()
        loader.title("Explaining...")
        loader.geometry("250x80")
        tk.Label(loader, text="Generating explanation...").pack(expand=True, padx=20, pady=20)
        loader.transient(text_widget.winfo_toplevel())
        loader.grab_set()

        def run_explain():
            try:
                prompt = f"Explain the following Python code step-by-step:\n\n{code}"
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                explanation = response.text.strip().splitlines()
                # prefix each line with '# '
                comments = "\n".join(f"# {line}" for line in explanation) + "\n"
                # insert comments right before the selected block
                text_widget.after(0, lambda: text_widget.insert(start, comments))
            except Exception as e:
                text_widget.after(0, lambda: messagebox.showerror("Explain Error", str(e)))
            finally:
                text_widget.after(0, loader.destroy)
                text_widget.after(0, lambda: ai_menu.entryconfig("Explain Selected Code", state="normal"))

        threading.Thread(target=run_explain, daemon=True).start()

    ai_menu.add_command(label="Generate Code", command=generate_code)
    ai_menu.add_command(label="Review Code", command=review_code)
    ai_menu.add_command(label="Generate Learning Roadmap", command=generate_learning_roadmap)
    ai_menu.add_command(label="Search Topic in Chrome", command=search_topic_in_chrome)
    ai_menu.add_separator()
    ai_menu.add_command(label="Generate Unit Tests", command=generate_unit_tests)
    ai_menu.add_command(label="Analyze & Auto-Fix Code", command=analyze_and_fix_code)
    ai_menu.add_command(label="Explain Selected Code", command=explain_selected_code)
