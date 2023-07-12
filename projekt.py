import PySimpleGUI as sg
import openai

openai.api_key = ''

class SecurityScannerGUI:
    def __init__(self):
        sg.theme("DarkTeal10")
        self.layout = [
            [sg.Text("Enterprise Code Security Scanner", font=("Verdana", 20, "bold"))],
            [sg.Text("Please enter the code you wish to scan or click 'Browse File' to select a file:")],
            [sg.Multiline(size=(80, 10), key="-CODE-")],
            [sg.Button("Browse File"), sg.Button("Scan Code"), sg.Button("Save Output"),
             sg.Button("Save Remediation Report")],
            [sg.Text("Scan Results:")],
            [sg.Multiline(size=(80, 10), key="-RESULTS-", disabled=True)]
        ]
        self.window = sg.Window("Enterprise Code Security Scanner", self.layout, finalize=True)
        self.openai_key = "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"  # Replace with your actual OpenAI API key

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Browse File":
                self.browse_file()
            elif event == "Scan Code":
                self.scan_code(values["-CODE-"])
            elif event == "Save Output":
                self.save_output(values["-RESULTS-"])
            elif event == "Save Remediation Report":
                self.save_remediation_report(values["-CODE-"])

        self.window.close()

    def browse_file(self):
        file_path = sg.popup_get_file("Select File to Scan")
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.window["-CODE-"].update(code)

    def scan_code(self, code):
        if not code.strip():
            sg.popup_warning("Scan Code", "No code provided. Please enter code or select a file to scan.")
            return

        # Perform scan using OpenAI API
        vulnerabilities = self.perform_scan(code)

        # Display the scan results
        self.window["-RESULTS-"].update(vulnerabilities)

    def perform_scan(self, code):
        # Initialize OpenAI API client
        openai.api_key = self.openai_key

        # Call the OpenAI API to scan the code
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a code security scanner."},
                      {"role": "user", "content": code}]
        )

        # Extract the generated vulnerability report from the API response
        vulnerabilities = response.choices[0].message.content.strip()

        return vulnerabilities

    def save_output(self, output):
        if not output.strip():
            sg.popup_warning("Save Output", "No output available.")
            return

        file_path = sg.popup_get_file("Save Output", save_as=True, file_types=(("Text Files", "*.txt"),))
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(output)
                sg.popup("Save Output", "Output saved successfully.")
            except Exception as e:
                sg.popup_warning("Save Output", f"Failed to save output.\nError: {str(e)}")

    def save_remediation_report(self, code):
        if not code.strip():
            sg.popup_warning("Save Remediation Report",
                             "No code provided. Please enter code or select a file to scan.")
            return

        vulnerabilities = self.perform_scan(code)
        report = {
            "code": code,
            "vulnerabilities": vulnerabilities
        }

        file_path = sg.popup_get_file("Save Remediation Report", save_as=True, file_types=(("JSON Files", "*.json"),))
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(str(report))  # Convert report to string before writing
                sg.popup("Save Remediation Report", "Remediation report saved successfully.")
            except Exception as e:
                sg.popup_warning("Save Remediation Report", f"Failed to save remediation report.\nError: {str(e)}")


if __name__ == '__main__':
    gui = SecurityScannerGUI()
    gui.run()
