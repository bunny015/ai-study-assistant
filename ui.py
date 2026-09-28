import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

from app import StudyAssistant
from chatbot.commands import parse_command, help_text


class StudyAssistantUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced AI Study Assistant")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg="#0f172a")

        self.bot = None
        self._busy = False

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("TLabel", background="#0f172a", foreground="#e2e8f0")
        self.style.configure("TButton", padding=(14, 8), font=("Segoe UI", 10, "bold"))
        self.style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff")
        self.style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        self.style.configure("TEntry", fieldbackground="#111827", foreground="#e2e8f0")

        self.status_var = tk.StringVar(value="Starting assistant...")
        self.create_widgets()
        self.bind("<Return>", self.on_send)
        self.bind("<Escape>", lambda event: self.destroy())

        self.after(200, self.start_assistant)

    def create_widgets(self):
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 12))

        title = ttk.Label(header, text="AI Study Assistant", font=("Segoe UI", 20, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Ask, explain, quiz, summarize, or use study commands.",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        status_bar = ttk.Frame(root)
        status_bar.pack(fill="x", pady=(0, 10))

        status_label = ttk.Label(status_bar, text="Status:", font=("Segoe UI", 10, "bold"))
        status_label.pack(side="left")

        status_value = ttk.Label(status_bar, textvariable=self.status_var, font=("Segoe UI", 10))
        status_value.pack(side="left", padx=(8, 0))

        chat_container = ttk.Frame(root)
        chat_container.pack(fill="both", expand=True)

        self.chat_box = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            state="disabled",
            bg="#111827",
            fg="#e2e8f0",
            insertbackground="#f8fafc",
            font=("Segoe UI", 11),
            padx=12,
            pady=10,
        )
        self.chat_box.pack(fill="both", expand=True)

        controls = ttk.Frame(root)
        controls.pack(fill="x", pady=(10, 0))

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            controls,
            textvariable=self.input_var,
            font=("Segoe UI", 11),
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.focus_set()

        send_button = ttk.Button(controls, text="Send", style="Accent.TButton", command=self.on_send_click)
        send_button.pack(side="left", padx=(10, 0))

        clear_button = ttk.Button(controls, text="Clear chat", command=self.clear_chat)
        clear_button.pack(side="left", padx=(10, 0))

        help_hint = ttk.Label(
            root,
            text="Quick commands: /help, /clear, /explain <topic>, /quiz <topic>, /summary <text>, /sources",
            font=("Segoe UI", 9),
            foreground="#93c5fd",
        )
        help_hint.pack(anchor="w", pady=(10, 0))

    def append_message(self, sender, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert(tk.END, f"{sender}:\n{message}\n\n")
        self.chat_box.see(tk.END)
        self.chat_box.configure(state="disabled")

    def clear_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", tk.END)
        self.chat_box.configure(state="disabled")
        if self.bot is not None:
            self.bot.memory.clear()
            self.append_message("Assistant", "Conversation memory cleared. Ready for the next question.")

    def start_assistant(self):
        def load_bot():
            try:
                self.bot = StudyAssistant()
                self.status_var.set("Ready")
                self.after(0, self.append_message, "Assistant", "Hello! I am ready to help with AI, Python, and study questions.")
            except Exception as exc:
                self.status_var.set("Startup failed")
                self.after(0, self.handle_startup_error, exc)

        thread = threading.Thread(target=load_bot, daemon=True)
        thread.start()

    def handle_startup_error(self, exc):
        self.input_entry.configure(state="disabled")
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "Setup error")
        messagebox.showerror("Assistant startup failed", str(exc))
        self.append_message("Assistant", f"Unable to start the assistant.\nError: {exc}\nCheck your OPENROUTER_API_KEY and project setup.")

    def on_send_click(self):
        self.on_send(None)

    def on_send(self, event):
        if self._busy:
            return

        text = self.input_var.get().strip()
        if not text:
            return

        self.input_var.set("")
        self.append_message("You", text)

        if self.bot is None:
            self.append_message("Assistant", "The assistant is still loading. Please wait a moment.")
            return

        self._busy = True
        self.status_var.set("Processing request...")

        def run_request():
            try:
                command, argument = parse_command(text)

                if command == "/exit":
                    response = "Goodbye!"
                elif command == "/help":
                    response = help_text()
                elif command == "/clear":
                    self.bot.memory.clear()
                    response = "Conversation memory cleared."
                elif command == "/sources":
                    response = self.bot.sources()
                elif command == "/explain":
                    response = self.bot.explain(argument)
                elif command == "/quiz":
                    response = self.bot.quiz(argument)
                elif command == "/summary":
                    response = self.bot.summary(argument)
                elif command:
                    response = "Unknown command. Type /help to see valid commands."
                else:
                    response = self.bot.normal_question(text)

                self.after(0, self.append_message, "Assistant", response)
            except Exception as exc:
                self.after(0, self.append_message, "Assistant", f"I could not complete that request.\n\n{exc}")
            finally:
                self._busy = False
                self.status_var.set("Ready")
                self.after(0, self.input_entry.focus_set)

        thread = threading.Thread(target=run_request, daemon=True)
        thread.start()


def main():
    app = StudyAssistantUI()
    app.mainloop()


if __name__ == "__main__":
    main()
