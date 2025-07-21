# agents/design_agent.py
from model_api import generate_text

def create_design(requirements: str, model_name: str) -> str:
    """
    Calls the Design Agent model with the given requirements.
    Returns a design specification (components, architecture, page structure, etc.).
    """
    system_msg = (
        "You are a Design agent. Using the provided requirements, "
        "produce a detailed design specification. "
        "Include components, file structure, data flow, and any necessary diagrams or descriptions."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": requirements}
    ]
    response = generate_text(messages, model_name)
    return response.strip()
