# import os
# import re

# def parse_and_save_coder_output(coded_string, base_dir="C:\\Users\\shreya1\\Desktop\\college\\multiagentapp\\deployed_app"):
#     os.makedirs(base_dir, exist_ok=True)

#     # Find all file blocks using regex
#     pattern = r"---\s*(.*?)\s*---\n(.*?)(?=(\n---|$))"
#     matches = re.findall(pattern, coded_string, re.DOTALL)

#     for filename, content, _ in matches:
#         file_path = os.path.join(base_dir, filename.strip())
#         os.makedirs(os.path.dirname(file_path), exist_ok=True)

#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(content.strip())

#     print(f"✅ Saved {len(matches)} files to '{base_dir}'")




import os
import re
import subprocess
import sys

def run_server(project_dir):
    """
    Detects the type of project and runs the appropriate server/app.
    Returns a tuple (url, process) where process is the subprocess.Popen instance.
    """
    # Check for Node.js files
    js_files = [f for f in os.listdir(project_dir) if f.endswith(".js")]
    if js_files:
        entry = "index.js" if "index.js" in js_files else ("server.js" if "server.js" in js_files else js_files[0])
        print(f"Running Node.js app: {entry}")
        try:
            proc = subprocess.Popen(
                ["node", entry],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return "http://localhost:3000", proc
        except FileNotFoundError:
            print("Node.js is not installed or not found in PATH.")
            return None, None

    # Check for static HTML (serving via Python HTTP server)
    if os.path.isfile(os.path.join(project_dir, "index.html")):
        print("Starting simple HTTP server on port 8000...")
        try:
            proc = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8000"],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return "http://localhost:8000", proc
        except Exception as e:
            print(f"Failed to start HTTP server: {e}")
            return None, None

    # Check for Flask app
    py_files = [f for f in os.listdir(project_dir) if f.endswith(".py")]
    flask_files = []
    for file in py_files:
        path = os.path.join(project_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if "from flask import" in content or "import flask" in content:
                flask_files.append(file)

    if flask_files:
        entry = flask_files[0]
        print(f"Running Flask app: {entry}")
        try:
            proc = subprocess.Popen(
                [sys.executable, entry],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            return "http://localhost:5000", proc
        except Exception as e:
            print(f"Failed to run Flask app: {e}")
            return None, None

    print("No recognized application entrypoint found.")
    return None, None

def parse_and_save_coder_output(coded_string, base_dir="deployed_app", auto_launch=True):
    """
    Parses code blocks and saves them to files.
    Expected format:
    ```filename.ext
    content
    ```
    If auto_launch is True, attempts to run the application after saving.
    """
    # Create the base directory relative to the current working directory
    base_dir = os.path.abspath(base_dir)
    os.makedirs(base_dir, exist_ok=True)

    # Match code blocks with filenames
    pattern = r"```(.*?)\n(.*?)```"
    matches = re.findall(pattern, coded_string, re.DOTALL)

    if not matches:
        print("⚠️ No files found in code output. Check the format:")
        print("✉️ CODE SAMPLE START:")
        print(coded_string[:500])  # show first 500 characters for debug
        print("✉️ CODE SAMPLE END")
        return None, None

    saved_files = []
    for filename, content in matches:
        # Clean up filename and content
        filename = filename.strip()
        content = content.strip()
        
        if not filename:  # Skip if no filename
            continue

        file_path = os.path.join(base_dir, filename)
        dir_path = os.path.dirname(file_path)
        
        # Create subdirectories if needed
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)

        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        saved_files.append(filename)

    if saved_files:
        print(f"✅ Saved {len(saved_files)} file(s) to '{base_dir}':")
        for f in saved_files:
            print(f"  - {f}")
        
        # Auto-launch the application if requested
        if auto_launch:
            url, proc = run_server(base_dir)
            return url, proc
    else:
        print("❌ No valid files were found to save")
    
    return None, None
