# CodePenguin: A ChatGPT-based Comprehensive Code Vulnerability analysis program
# Capable of understanding 71 programming languages and their vulnerabilities in every use case. 

<img width="457" alt="1" src="https://github.com/crxxtian/codepenguin-gpt-code-scanner/assets/124479510/9d820a27-6088-451d-b218-634329e3791a">

-Started on 7/11/2023
=Built using Python and  OpenAI API

-Must have your own API key that you set as an environment variable for this to work. 

# Can use the following models:

"gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613", "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613"

<img width="456" alt="2" src="https://github.com/crxxtian/codepenguin-gpt-code-scanner/assets/124479510/3611517f-0a56-48ed-950f-4793bfa907bc">

-This is such a huge WIP and just something I have thrown together in 2 days! I hope to expand this project out immensely and eventually lead into a web app. Here are the current functionalities and possibilities it offers:

1. **Graphical User Interface (GUI)**: The code sets up a GUI using the PySimpleGUI library, allowing users to interact with the application through buttons and text fields.

2. **Code Input**: Users can enter or paste code into a multiline text field within the GUI. Alternatively, they can click the "Browse File" button to select a file containing the code.

3. **Scan Code**: By clicking the "Scan Code" button, the code provided in the input field will be sent to the OpenAI API for analysis. The application utilizes the OpenAI GPT-3.5 Turbo model to perform a language-based chat completion.

4. **Loading Screen**: During the code scanning process, a loading screen with a progress bar is displayed to provide visual feedback to the user.

5. **Scan Results**: The application retrieves the response from the OpenAI API, extracts the vulnerability report, and displays it in a multiline text field. This allows users to view the analysis and identified vulnerabilities.

<img width="457" alt="3" src="https://github.com/crxxtian/codepenguin-gpt-code-scanner/assets/124479510/faaef21d-307c-4eca-a461-efb0a58bd8e8">

7. **Save Output**: Users can save the scan results or any other text content from the GUI to a file by clicking the "Save Output" button. A file dialog prompts them to choose the location and filename for saving.

8. **Save Remediation Report**: Similarly, users can save the code and the associated vulnerability report as a JSON file by clicking the "Save Remediation Report" button. This option allows them to keep a record of the code and the identified vulnerabilities for further analysis or remediation.

9. **Settings**: The "Settings" button opens a settings menu where users can modify certain parameters, such as the OpenAI engine, temperature, and max tokens used in the chat completion. These settings are stored in a configuration file.

It's important to note that the current implementation relies on the OpenAI API and the capabilities of the GPT-3.5 Turbo model for code vulnerability analysis. The analysis and the accuracy of identified vulnerabilities heavily depend on the training data and the limitations of the language model. Further improvements and enhancements can be made based on specific requirements and integrating additional security analysis techniques or tools.

<img width="456" alt="4" src="https://github.com/crxxtian/codepenguin-gpt-code-scanner/assets/124479510/bbe1d6db-ef23-4a20-9017-877781e56df1">
<img width="455" alt="5" src="https://github.com/crxxtian/codepenguin-gpt-code-scanner/assets/124479510/93eda839-3300-473d-8d09-656e1739679e">

-Exhaustive list of languages that CodePenguin has knowledge on:
ABAP
ActionScript
Ada
ALGOL
Alice
Apex
APL
AppleScript
Assembly language
AWK
Bash
BASIC
C
C++
C#
COBOL
ColdFusion
Crystal
D
Dart
Delphi
Elixir
Elm
Erlang
F#
Fortran
Go
Groovy
Haskell
Haxe
HTML/CSS
IDL
Io
J
Java
JavaScript
Julia
Kotlin
LISP
Lua
MATLAB
Objective-C
OCaml
Pascal
Perl
PHP
PL/SQL
PowerShell
Prolog
Python
R
Ruby
Rust
SAS
Scala
Scheme
Scratch
Shell scripting
Smalltalk
SQL
Swift
Tcl
TypeScript
Vala
VBA
Verilog
VHDL
Visual Basic
WebAssembly
Wolfram Language
XSLT
