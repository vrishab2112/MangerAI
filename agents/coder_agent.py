# agents/coder_agent.py
from model_api import generate_text

def generate_code(design: str, model_name: str) -> str:
    """
    Calls the Coder Agent model with the design specification.
    Returns the generated code (e.g. HTML/CSS/JS or Python code).
    """
    system_msg = (
        """You are a coding agent. Given the following design specification, generate all required code files (e.g., HTML, CSS, JS).
Format your response using code blocks with filenames in the following format EXACTLY:

```index.html
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="styles/styles.css" /></head>
<body>
  <header>My Header</header>
</body>
</html>
```

```styles/styles.css
body { 
    font-family: sans-serif; 
}
```

```scripts/header.component.js
console.log("Header loaded");
```

IMPORTANT:
1. Each file must be in a code block starting with ```filename
2. Do not include any other text or explanations between code blocks
3. Make sure to include all necessary files for the application to run
4. Include proper file extensions in the filenames
"""    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": design}
    ]
    response = generate_text(messages, model_name)
    return response
