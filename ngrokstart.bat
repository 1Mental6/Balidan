@echo off
REM Start ngrok on port 5000 using the full path
start /B C:\Users\SWAPNONEEL\Desktop\ngrok-v3-stable-windows-amd64\ngrok.exe http 5000

REM Wait for ngrok to initialize (optional, adjust time as needed)
timeout /t 10

REM Start the Python script in the background (without command window)
start /B pythonw C:\Users\SWAPNONEEL\Desktop\project\main.py
