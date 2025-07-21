import os
import sys
import re
import subprocess
import tempfile
import shutil

def parse_code_blocks(text):
    """
    Parses fenced code blocks from the given text.
    Each code block is expected to have a file name in its info line, e.g. ```python main.py```.
    Returns a list of (filename, content) tuples.
    """
    code_blocks = []
    fence_pattern = re.compile(r'^```(.*)')
    lines = text.splitlines()
    in_block = False
    current_filename = None
    current_lines = []
    for line in lines:
        if not in_block:
            m = fence_pattern.match(line)
            if m:
                info = m.group(1).strip()
                parts = info.split()
                # Determine filename if present (has extension)
                if len(parts) > 1 and '.' in parts[-1]:
                    current_filename = parts[-1]
                elif len(parts) == 1 and '.' in parts[0]:
                    current_filename = parts[0]
                else:
                    current_filename = None
                in_block = True
                current_lines = []
        else:
            if line.strip() == "```":
                if current_filename:
                    content = "\n".join(current_lines).rstrip() + "\n"
                    code_blocks.append((current_filename, content))
                in_block = False
                current_filename = None
                current_lines = []
            else:
                current_lines.append(line)
    return code_blocks

def install_requirements(project_dir):
    """
    Installs dependencies for the project.
    If a requirements.txt is present, uses pip install -r requirements.txt.
    Otherwise, auto-detects imports in Python files and installs them.
    """
    req_path = os.path.join(project_dir, "requirements.txt")
    if os.path.isfile(req_path):
        print(f"Installing dependencies from requirements.txt...", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=project_dir, capture_output=True, text=True
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
        except Exception as e:
            print(f"Error installing requirements: {e}", file=sys.stderr)
    else:
        # Auto-detect imports in Python files
        print("No requirements.txt found; attempting auto-detection of imports.", flush=True)
        imports = set()
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8") as f:
                        for line in f:
                            m = re.match(r"^\s*(?:from\s+(\w+)|import\s+(\w+))", line)
                            if m:
                                pkg = m.group(1) or m.group(2)
                                # skip common built-in modules
                                if pkg and pkg not in ("os", "sys", "re", "math", "subprocess", "tempfile", "shutil", "builtins"):
                                    imports.add(pkg)
        if imports:
            print(f"Detected imports: {imports}. Installing...", flush=True)
            for pkg in sorted(imports):
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", pkg],
                        cwd=project_dir, capture_output=True, text=True
                    )
                    print(result.stdout)
                    if result.stderr:
                        print(result.stderr, file=sys.stderr)
                except Exception as e:
                    print(f"Error installing {pkg}: {e}", file=sys.stderr)
        else:
            print("No external imports detected.", flush=True)

def run_server(project_dir):
    """
    Detects the type of project and runs the appropriate server/app.
    Returns a tuple (url, process) where process is the subprocess.Popen instance.
    """
    # Check for Node.js files
    js_files = [f for f in os.listdir(project_dir) if f.endswith(".js")]
    if js_files:
        entry = "index.js" if "index.js" in js_files else ("server.js" if "server.js" in js_files else js_files[0])
        print(f"Running Node.js app: {entry}", flush=True)
        try:
            proc = subprocess.Popen(
                ["node", entry],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            url = None
        except FileNotFoundError:
            print("Node.js is not installed or not found in PATH.", file=sys.stderr)
            return None, None
        return None, proc

    # Check for static HTML (serving via Python HTTP server)
    if os.path.isfile(os.path.join(project_dir, "index.html")):
        print("Starting simple HTTP server on port 8000...", flush=True)
        try:
            proc = subprocess.Popen(
                [sys.executable, "-m", "http.server", "8000"],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            url = "http://localhost:8000"
        except Exception as e:
            print(f"Failed to start HTTP server: {e}", file=sys.stderr)
            return None, None
        return url, proc

    # Check for Streamlit app
    py_files = [f for f in os.listdir(project_dir) if f.endswith(".py")]
    streamlit_files = []
    flask_files = []
    for file in py_files:
        path = os.path.join(project_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if re.search(r"\bimport\s+streamlit\b", content) or re.search(r"\bstreamlit\.", content):
                streamlit_files.append(file)
            if re.search(r"\bimport\s+Flask\b", content) or re.search(r"Flask\(", content):
                flask_files.append(file)

    if streamlit_files:
        entry = streamlit_files[0]
        print(f"Running Streamlit app: {entry}", flush=True)
        try:
            proc = subprocess.Popen(
                ["streamlit", "run", entry, "--server.port=8502"],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            url = "http://localhost:8502"
        except FileNotFoundError:
            print("Streamlit is not installed or not found in PATH.", file=sys.stderr)
            return None, None
        return url, proc

    if flask_files:
        entry = flask_files[0]
        print(f"Running Flask app: {entry}", flush=True)
        try:
            proc = subprocess.Popen(
                [sys.executable, entry],
                cwd=project_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            url = "http://localhost:5000"
        except Exception as e:
            print(f"Failed to run Flask app: {e}", file=sys.stderr)
            return None, None
        return url, proc

    print("No recognized application entrypoint found.", flush=True)
    return None, None

def save_to_workspace(code_blocks, workspace_dir="deployed_app"):
    """
    Saves code blocks to the specified workspace directory.
    Args:
        code_blocks: List of (filename, content) tuples
        workspace_dir: Directory name within the workspace to save files
    Returns:
        Path to the workspace directory
    """
    # Create workspace directory if it doesn't exist
    os.makedirs(workspace_dir, exist_ok=True)
    print(f"Saving files to workspace directory: {workspace_dir}", flush=True)

    for filename, content in code_blocks:
        filepath = os.path.join(workspace_dir, filename)
        dirpath = os.path.dirname(filepath)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved file: {filepath}", flush=True)
    
    return workspace_dir

def main():
    # Read code blocks from stdin or a file argument
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("No input code provided.", file=sys.stderr)
        return

    # Parse code blocks
    code_blocks = parse_code_blocks(text)
    if not code_blocks:
        print("No code blocks with filenames found.", file=sys.stderr)
        return

    # Save files to workspace
    project_dir = save_to_workspace(code_blocks)
    print(f"Files saved to workspace directory: {project_dir}", flush=True)

    # Install dependencies
    install_requirements(project_dir)

    # Run the appropriate server/application
    url, proc = run_server(project_dir)
    if url:
        print(f"Application running at: {url}", flush=True)
    else:
        print("No application URL available.", file=sys.stderr)

    # Stream logs from the process
    if proc:
        try:
            for line in proc.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            print("Shutting down application.", flush=True)
        finally:
            proc.terminate()
            proc.wait()

if __name__ == "__main__":
    main()
