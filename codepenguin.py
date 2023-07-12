import os
import json
import PySimpleGUI as sg
import openai
import threading
import time

class SecurityScannerGUI:
    def __init__(self):
        sg.theme("DarkTeal10")

        # Load saved settings
        self.load_settings()

        self.layout = [
            [sg.Text("CodePenguin Security Scanner", font=("Verdana", 20, "bold"))],
            [sg.Text("Please enter the code you wish to scan or click 'Browse File' to select a file:")],
            [sg.Multiline(size=(80, 10), key="-CODE-")],
            [sg.Button("Browse File"), sg.Button("Scan Code"), sg.Button("Save Output"),
             sg.Button("Save Remediation Report"), sg.Button("Settings")],
            [sg.Text("Scan Results:")],
            [sg.Multiline(size=(80, 10), key="-RESULTS-", disabled=True)]
        ]
        self.window = sg.Window("CodePenguin Security Scanner", self.layout, finalize=True)
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.rate_limit_duration = 60  # Duration in seconds to wait before making subsequent API calls
        self.last_api_call_time = 0  # Time of the last API call
        self.loading_screen = None
        self.progress_bar = None

    def load_settings(self):
        # Default settings
        self.settings = {
            "engine": "davinci",
            "temperature": 0.3,
            "max_tokens": 100
        }

        # Load settings from file
        try:
            with open("config.json", "r") as file:
                self.settings = json.load(file)
        except Exception:
            pass

    def save_settings(self):
        # Save settings to file
        try:
            with open("config.json", "w") as file:
                json.dump(self.settings, file)
        except Exception:
            pass

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
            elif event == "Settings":
                self.show_settings()

        self.window.close()

    def browse_file(self):
        file_path = sg.popup_get_file("Select File to Scan")
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.window["-CODE-"].update(code)

    def scan_code(self, code):
        if not code.strip():
            sg.popup("Scan Code", "No code provided. Please enter code or select a file to scan.", title="Warning")
            return

        # Perform scan using OpenAI API in a separate thread
        threading.Thread(target=self.perform_scan, args=(code,), daemon=True).start()

        # Display the loading screen
        self.show_loading_screen()

    def perform_scan(self, code):
        if not self.openai_key:
            sg.popup("API Key Missing", "Please set the OPENAI_API_KEY environment variable.", title="Warning")
            return ""

        # Check if enough time has passed since the last API call
        current_time = time.time()
        time_diff = current_time - self.last_api_call_time
        if time_diff < self.rate_limit_duration:
            time_to_wait = self.rate_limit_duration - time_diff
            sg.popup("Rate Limit Exceeded",
                     f"Please wait for {int(time_to_wait)} seconds before making another API call.",
                     title="Warning")
            return ""

        # Initialize OpenAI API client
        openai.api_key = self.openai_key

        prompt = """
        You are a comprehensive code security scanner. Scan the following code for vulnerabilities and provide a detailed report:

        === CODE START ===
        {code}
        === CODE END ===

        Instructions:
        1. Identify and report any potential security vulnerabilities present in the code, and identify the programming language, and give a brief description of the code.
        2. Provide a detailed analysis of each vulnerability, including the type, severity, and potential impact.
        3. Recommend remediation steps to address each identified vulnerability.
        4. Ensure that the report is well-structured, organized, and easy to understand.
        5. Pay attention and recognize common security vulnerabilities.
        6. Consider any specific security requirements or standards relevant to the code, such as OWASP Top 10 or specific compliance frameworks.

        Please provide a comprehensive vulnerability report for the given code.
        """.format(code=code)

        # Call the OpenAI API to scan the code
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code security scanner."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the vulnerability report from the API response
        vulnerabilities = response.choices[0].message.content.strip()

        # Update the last API call time
        self.last_api_call_time = time.time()

        # Update the scan results in the GUI
        self.window["-RESULTS-"].update(vulnerabilities)

        # Hide the loading screen
        self.hide_loading_screen()

        return vulnerabilities

    def show_loading_screen(self):
        loading_layout = [
            [sg.Text("Performing Code Scan", font=("Verdana", 18))],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROGRESS-', bar_color=('blue', 'white'),
                            style='indeterminate')]
        ]
        self.loading_screen = sg.Window("Loading", loading_layout, finalize=True, no_titlebar=True, keep_on_top=True)
        self.progress_bar = self.loading_screen['-PROGRESS-']
        self.progress_bar.update(0)

        # Update the progress bar in a loop
        for i in range(200):  # Increase the range to slow down the progress bar
            if self.loading_screen:  # Check if the window has not been closed
                event, values = self.loading_screen.read(timeout=35)  # Increase timeout to slow down the progress bar
                if event == sg.WINDOW_CLOSED or event is None:
                    break
                self.progress_bar.update(i / 2)  # Divide by 2 to match the increased range

    def hide_loading_screen(self):
        if self.loading_screen:
            self.loading_screen.close()
            self.loading_screen = None
            self.progress_bar = None

    def save_output(self, output):
        if not output.strip():
            sg.popup("Save Output", "No output available.", title="Warning")
            return

        file_path = sg.popup_get_file("Save Output", save_as=True, file_types=(("Text Files", "*.txt"),))
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(output)
                sg.popup("Save Output", "Output saved successfully.")
            except Exception as e:
                sg.popup("Save Output", f"Failed to save output.\nError: {str(e)}", title="Warning")

    def save_remediation_report(self, code):
        if not code.strip():
            sg.popup("Save Remediation Report", "No code provided. Please enter code or select a file to scan.",
                     title="Warning")
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
                    file.write(json.dumps(report))  # Write report as JSON string
                sg.popup("Save Remediation Report", "Remediation report saved successfully.")
            except Exception as e:
                sg.popup("Save Remediation Report", f"Failed to save remediation report.\nError: {str(e)}",
                         title="Warning")

    def show_settings(self):
        # Settings layout
        settings_layout = [
            [sg.Text("Engine:"), sg.InputCombo(["gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"], default_value=self.settings["engine"], key="-ENGINE-")],
            [sg.Text("Temperature:"), sg.Input(self.settings["temperature"], key="-TEMPERATURE-")],
            [sg.Text("Max Tokens:"), sg.Input(self.settings["max_tokens"], key="-MAX_TOKENS-")],
            [sg.Button("Save"), sg.Button("Cancel")]
        ]
        settings_window = sg.Window("Settings", settings_layout)

        while True:
            event, values = settings_window.read()
            if event == sg.WINDOW_CLOSED or event == "Cancel":
                break
            elif event == "Save":
                self.settings["engine"] = values["-ENGINE-"]
                self.settings["temperature"] = float(values["-TEMPERATURE-"])
                self.settings["max_tokens"] = int(values["-MAX_TOKENS-"])
                self.save_settings()
                break

        settings_window.close()


if __name__ == '__main__':
    gui = SecurityScannerGUI()
    gui.run()
