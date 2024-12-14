import os
import sys
import ctypes
from flask import Flask, request, Response
from flask_cors import CORS  # CORS for cross-origin requests
import subprocess

# Check and elevate privileges
def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    """Restart the script with admin privileges."""
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

# Call the function to ensure the script is running with admin privileges
elevate_privileges()

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from any domain

SECRET_TOKEN = "Roger"

@app.route('/', methods=['GET'])
def home():
    return '''
        <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        background-color: white;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        padding: 30px;
                        width: 400px;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                    }
                    input[type="text"] {
                        width: 100%;
                        padding: 10px;
                        margin: 10px 0;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        font-size: 16px;
                    }
                    input[type="submit"] {
                        width: 100%;
                        padding: 12px;
                        background-color: #007BFF;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        font-size: 16px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }
                    input[type="submit"]:hover {
                        background-color: #0056b3;
                    }
                    .footer {
                        margin-top: 20px;
                        font-size: 14px;
                        color: #888;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Enable Location Services</h1>
                    <form action="/enable_location" method="post">
                        <label for="token">Victus:</label>
                        <input type="text" name="token" id="token" required placeholder="Enter your token">
                        <input type="submit" value="Enable Location">
                    </form>
                    <div class="footer">
                        <p>Made by SEN</p>
                    </div>
                </div>
            </body>
        </html>
    '''



@app.route('/enable_location', methods=['POST'])
def enable_location():
    token = request.form.get('token')
    if token != SECRET_TOKEN:
        return "Unauthorized", 401

    # Here, you would enable the location services or any other logic
    try:
        powershell_script = """
        Set-Location -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location
        Set-ItemProperty . -Name Value -Value Allow
        """

        with open("enable_location.ps1", "w") as script_file:
            script_file.write(powershell_script)

             
        result = subprocess.run(
            [r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", "-NoProfile", "-File", "enable_location.ps1", "powershell",  r"C:\Users\SWAPNONEEL\Desktop\project\enable_location.ps1"], 
            check=True, 
            text=True, 
            capture_output=True
        )

        #Logs the powershell output for understanding

        print("Powershell Output: Successfully enabled Location", result.stdout)
        return Response("Location services enabled successfully.", status=200)
    except subprocess.CalledProcessError as e:
        print("Powershell Output: Failed to enable location", e.stderr)
        return Response(f"Failed to enable location services: {e.stderr}", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
