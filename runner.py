import subprocess
import sys

# Run main.py using uvicorn
uvicorn_process = subprocess.Popen(["uvicorn", "main:app", "--reload"])

# Open a new terminal and run User.py
if sys.platform == "win32":
    # For Windows
    subprocess.Popen(["start", "cmd", "/k", "streamlit run User.py"], shell=True)
else:
    # For Unix-like systems (Linux, macOS)
    subprocess.Popen(["gnome-terminal", "--", "streamlit", "run", "User.py"])

# Wait for uvicorn process to finish (Ctrl+C to stop both processes)
uvicorn_process.wait()
