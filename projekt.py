import os
import PySimpleGUI as sg
import openai


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
        self.openai_key = os.getenv("OPENAI_API_KEY")

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
            sg.popup("Scan Code", "No code provided. Please enter code or select a file to scan.")
            return

        # Perform scan using OpenAI API
        vulnerabilities = self.perform_scan(code)

        # Display the scan results
        self.window["-RESULTS-"].update(vulnerabilities)

    def perform_scan(self, code):
        if not self.openai_key:
            sg.popup("API Key Missing", "Please set the OPENAI_API_KEY environment variable.")
            return

        # Initialize OpenAI API client
        openai.api_key = self.openai_key

        prompt = """
        You are a comprehensive code security scanner. Scan the following code for vulnerabilities and provide a detailed report:

        === CODE START ===
        {code}
        === CODE END ===

        Instructions:
        1. Identify and report any potential security vulnerabilities present in the code.
        2. Provide a detailed analysis of each vulnerability, including the type, severity, and potential impact.
        3. Recommend remediation steps to address each identified vulnerability.
        4. Ensure that the report is well-structured, organized, and easy to understand.
        5. Pay attention to common security vulnerabilities such as:
           - Injection attacks (SQL, command, etc.)
           - Cross-Site Scripting (XSS)
           - Cross-Site Request Forgery (CSRF)
           - Authentication and authorization issues
           - Information leakage
           - Insecure direct object references
           - Insecure deserialization
           - Secure coding best practices (input validation, output encoding, etc.)
        6. Consider any specific security requirements or standards relevant to the code, such as OWASP Top 10 or specific compliance frameworks.

        Please provide a comprehensive vulnerability report for the given code.
        """.format(code=code)

        # Call the OpenAI API to scan the code
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.3,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )

        # Extract the vulnerability report from the API response
        vulnerabilities = response.choices[0].text.strip()

        return vulnerabilities

    def save_output(self, output):
        if not output.strip():
            sg.popup("Save Output", "No output available.")
            return

        file_path = sg.popup_get_file("Save Output", save_as=True, file_types=(("Text Files", "*.txt"),))
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(output)
                sg.popup("Save Output", "Output saved successfully.")
            except Exception as e:
                sg.popup("Save Output", f"Failed to save output.\nError: {str(e)}")

    def save_remediation_report(self, code):
        if not code.strip():
            sg.popup("Save Remediation Report",
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
                sg.popup("Save Remediation Report", f"Failed to save remediation report.\nError: {str(e)}")


if __name__ == '__main__':
    gui = SecurityScannerGUI()
    gui.run()
