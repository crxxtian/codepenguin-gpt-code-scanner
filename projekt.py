import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import threading
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

openai.api_key = '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'


class SecurityScannerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Enterprise Code Security Scanner")
        root.geometry("800x600")

        self.init_ui()

        self.scan_results = ""
        self.remediated_code = ""

    def init_ui(self):
        title_label = tk.Label(self.root, text="Enterprise Code Security Scanner", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        instructions_label = tk.Label(self.root, text="Please enter the code you wish to scan or click 'Browse File' to select a file:")
        instructions_label.pack()

        code_frame = tk.Frame(self.root)
        code_frame.pack(pady=10)

        code_scrollbar = tk.Scrollbar(code_frame)
        code_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.code_text = tk.Text(code_frame, height=10, width=50, wrap=tk.NONE, yscrollcommand=code_scrollbar.set)
        self.code_text.pack(side=tk.LEFT)

        code_scrollbar.config(command=self.code_text.yview)

        browse_button = tk.Button(self.root, text="Browse File", command=self.browse_file)
        browse_button.pack(pady=10)

        scan_button = tk.Button(self.root, text="Scan Code", command=self.scan_code)
        scan_button.pack()

        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10)

        vulnerabilities_label = tk.Label(result_frame, text="Potential Vulnerabilities:")
        vulnerabilities_label.pack(side=tk.LEFT)

        remediation_label = tk.Label(result_frame, text="Remediated Code:")
        remediation_label.pack(side=tk.LEFT, padx=10)

        vulnerabilities_scrollbar = tk.Scrollbar(self.root)
        vulnerabilities_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.vulnerabilities_text = tk.Text(self.root, height=20, width=40, wrap=tk.NONE, yscrollcommand=vulnerabilities_scrollbar.set)
        self.vulnerabilities_text.pack(side=tk.LEFT, padx=10)
        vulnerabilities_scrollbar.config(command=self.vulnerabilities_text.yview)

        remediation_scrollbar = tk.Scrollbar(self.root)
        remediation_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.remediation_text = tk.Text(self.root, height=20, width=40, wrap=tk.NONE, yscrollcommand=remediation_scrollbar.set)
        self.remediation_text.pack(side=tk.LEFT, padx=10)
        remediation_scrollbar.config(command=self.remediation_text.yview)

        save_button = tk.Button(self.root, text="Save Remediation", command=self.save_remediation)
        save_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Scan", filetypes=[("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert(tk.END, code)

    def scan_code(self):
        code = self.code_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Scan Code", "No code provided. Please enter code or select a file to scan.")
            return

        self.vulnerabilities_text.delete("1.0", tk.END)
        self.remediation_text.delete("1.0", tk.END)

        self.vulnerabilities_text.insert(tk.END, "Scanning code...\n")

        threading.Thread(target=self.perform_scan, args=(code,)).start()

    def perform_scan(self, code):
        lexer = get_lexer_by_name("cpp")
        formatter = HtmlFormatter(style="colorful")
        highlighted_code = highlight(code, lexer, formatter)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a comprehensive and driven Code Security Scanner familiar with all languages. My purpose is to detect and analyze potential security vulnerabilities in your code with precision and accuracy."},
                {"role": "user", "content": "Comprehensively evaluate the provided code for security vulnerabilities and provide detailed specific remediations on any potential weaknesses or flaws you discover, or explain a different method of writing the code:\n" + code}
            ]
        )
        vulnerabilities = response.choices[0].message['content']

        self.update_result_text(self.vulnerabilities_text, "Potential vulnerabilities and remediations found within the code:")
        self.append_syntax_highlighted_text(self.vulnerabilities_text, highlighted_code)
        self.update_result_text(self.vulnerabilities_text, vulnerabilities)

        self.scan_results = vulnerabilities
        self.remediated_code = code

    def update_result_text(self, text_widget, text):
        text_widget.insert(tk.END, text + "\n")
        text_widget.see(tk.END)

    def append_syntax_highlighted_text(self, text_widget, text):
        text_widget.insert(tk.END, text)
        text_widget.see(tk.END)

    def save_remediation(self):
        if not self.remediated_code:
            messagebox.showwarning("Save Remediation", "No remediation code available.")
            return

        file_path = filedialog.asksaveasfilename(title="Save Remediation", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.remediated_code)
                messagebox.showinfo("Save Remediation", "Remediation code saved successfully.")
            except Exception as e:
                messagebox.showwarning("Save Remediation", f"Failed to save remediation code.\nError: {str(e)}")


if __name__ == '__main__':
    root = tk.Tk()
    gui = SecurityScannerGUI(root)
    root.mainloop()
