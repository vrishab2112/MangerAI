# # agents/requirements_agent.py
# # from model_api import generate_text

# # def analyze_requirements(prompt: str, model_name: str) -> str:
# #     """
# #     Calls the Requirements Agent model to analyze the user prompt.
# #     Returns a detailed list of requirements (functional and non-functional).
# #     """
# #     system_msg = (
# #         "You are a Requirements Analysis agent. "
# #         "Extract all functional and non-functional requirements from the user's prompt. "
# #         "Be thorough and bullet-point them if possible."
# #     )
# #     messages = [
# #         {"role": "system", "content": system_msg},
# #         {"role": "user", "content": prompt}
# #     ]
# #     response = generate_text(messages, model_name)
# #     return response.strip()


# from langchain_community.tools.tavily_search import TavilySearchResults
# from model_api import generate_text

# def analyze_requirements(prompt: str, model_name: str) -> str:
#     # Step 1: Perform Tavily web search
#     search_tool = TavilySearchResults(k=3)
#     web_results = search_tool.run(prompt)

#     # Step 2: Build enhanced prompt with web context
#     system_msg = (
#         "You are a Requirements Analysis agent. "
#         "Use the user's prompt and the relevant web results provided to extract all functional and non-functional requirements. "
#         "Be thorough and bullet-point them if possible."
#     )

#     # Add web results to the user message
#     messages = [
#         {"role": "system", "content": system_msg},
#         {"role": "user", "content": f"Prompt: {prompt}\n\nWeb Context:\n{web_results}"}
#     ]

#     # Step 3: Call the LLM
#     response = generate_text(messages, model_name)
#     return response.strip()




# from langchain_community.tools.tavily_search import TavilySearchResults
# from model_api import generate_text

# def analyze_requirements(prompt: str, model_name: str) -> str:
#     # Step 1: Perform Tavily web search using `invoke` for structured results
#     search_tool = TavilySearchResults(k=3)
#     search_results = search_tool.invoke(prompt)

#     # Step 2: Format web results with source URLs
#     web_context = ""
#     for i, result in enumerate(search_results):
#         title = result.get("title", "No Title")
#         snippet = result.get("content", "No Content")
#         link = result.get("url", "")
#         web_context += f"{i+1}. {title}\n{snippet}\nSource: {link}\n\n"

#     # Step 3: Build messages for LLM
#     system_msg = (
#         "You are a Requirements Analysis agent. "
#         "Use the user's prompt and the web search results (with sources) to extract all functional and non-functional requirements. "
#         "Mention relevant references where needed. Be thorough and bullet-point them."
#     )

#     messages = [
#         {"role": "system", "content": system_msg},
#         {"role": "user", "content": f"Prompt: {prompt}\n\nWeb Search Results:\n{web_context}"}
#     ]

#     # Step 4: Call the LLM
#     response = generate_text(messages, model_name)
#     return response.strip()


# def format_response_with_sources(requirements_text: str, sources: list[str]) -> str:
#     # Remove all (Source: ...) from the text
#     import re
#     clean_text = re.sub(r"\(Source:.*?\)", "", requirements_text)

#     # Add a Sources section at the end
#     sources_section = "\n\n### 🔗 Sources Referenced\n" + "\n".join(f"- {src}" for src in set(sources))
#     return clean_text.strip() + sources_section



from langchain_community.tools.tavily_search import TavilySearchResults
from model_api import generate_text

# Initialize Tavily Search Tool
search_tool = TavilySearchResults(k=5)

def analyze_requirements(prompt: str, model_name: str) -> str:
    """
    Analyze requirements using LLM + Tavily Search, format results cleanly.
    """

    # Step 1: Perform web search to get reference URLs
    search_results = search_tool.invoke(prompt)
    urls = [item["url"] for item in search_results]

    # Step 2: Prepare prompt with system and user messages
    system_msg = (
        "You are a Requirements Analysis agent. "
        "Extract all functional and non-functional requirements from the user's prompt. "
        "Do NOT include URLs or sources inline. "
        "Present the output under clear headings: 'Functional Requirements' and 'Non-Functional Requirements'. "
        "Format it neatly using bullet points."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]

    # Step 3: Generate response using LLM
    raw_response = generate_text(messages, model_name).strip()

    # Step 4: Append sources at the end, nicely formatted
    source_block = "\n\n### 🔗 Sources Referenced\n" + "\n".join(f"- {url}" for url in set(urls))

    return raw_response + source_block
