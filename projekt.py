import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QColor, QTextDocument
import openai
import threading

openai.api_key = 'api-key'

class SecurityScannerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enterprise Code Security Scanner")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

        self.scan_results = ""

    def init_ui(self):
        main_widget = QWidget()

        vbox = QVBoxLayout()

        title_label = QLabel("Enterprise Code Security Scanner")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        vbox.addWidget(title_label)

        instructions_label = QLabel("Please enter the code you wish to scan or click 'Browse File' to select a file:")
        vbox.addWidget(instructions_label)

        self.code_text = QTextEdit()
        self.code_text.setLineWrapMode(QTextEdit.NoWrap)
        vbox.addWidget(self.code_text)

        browse_button = QPushButton("Browse File")
        browse_button.clicked.connect(self.browse_file)
        vbox.addWidget(browse_button)

        scan_button = QPushButton("Scan Code")
        scan_button.clicked.connect(self.scan_code)
        vbox.addWidget(scan_button)

        save_button = QPushButton("Save Results")
        save_button.clicked.connect(self.save_results)
        vbox.addWidget(save_button)

        load_button = QPushButton("Load Results")
        load_button.clicked.connect(self.load_results)
        vbox.addWidget(load_button)

        result_label = QLabel("Scan results and potential remediations will appear below:")
        vbox.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        vbox.addWidget(self.result_text)

        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File to Scan", "", "All Files (*)")
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_text.setPlainText(code)

    def scan_code(self):
        code = self.code_text.toPlainText().strip()
        if not code:
            self.result_text.append("No code provided. Please enter code or select a file to scan.")
            return

        self.result_text.append("Scanning code...")
        threading.Thread(target=self.perform_scan, args=(code,)).start()

    def perform_scan(self, code):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a comprehensive and driven Code Security Scanner familiar with all languages. My purpose is to detect and analyze potential security vulnerabilities in your code with precision and accuracy."},
                {"role": "user", "content": "Comprehensively evaluate the provided code for security vulnerabilities and provide detailed specific remediations on any potential weaknesses or flaws you discover, or explain a different method of writing the code:\n" + code}
            ]
        )
        vulnerabilities = response.choices[0].message['content']

        self.result_text.append("Potential vulnerabilities and remediations found within the code:")
        self.result_text.append(vulnerabilities)

        self.scan_results = vulnerabilities

    def save_results(self):
        if not self.scan_results:
            QMessageBox.information(self, "Save Results", "No scan results to save.")
            return

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Scan Results", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.scan_results)
                QMessageBox.information(self, "Save Results", "Scan results saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Save Results", f"Failed to save scan results.\nError: {str(e)}")

    def load_results(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Load Scan Results", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    scan_results = file.read()
                self.result_text.setPlainText(scan_results)
                self.scan_results = scan_results
                QMessageBox.information(self, "Load Results", "Scan results loaded successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Load Results", f"Failed to load scan results.\nError: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = SecurityScannerGUI()
    gui.show()
    sys.exit(app.exec_())
