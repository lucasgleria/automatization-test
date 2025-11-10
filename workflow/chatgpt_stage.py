import os
import json
import yaml
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def load_prompt(filepath):
    """Loads a prompt from a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Prompt file not found at {filepath}")
        return ""

def run_chatgpt_stage(user_task, session_dir):
    """
    Runs the ChatGPT stage to collect and organize information.
    """
    print("Running ChatGPT stage...")

    # 1. Load configuration
    with open("config/chatgpt_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 2. Load prompts and construct the system prompt
    system_rules = load_prompt("prompts/chatgpt_system.md")
    sources_rules = load_prompt("prompts/chatgpt_sources.md")
    trusted_sources = load_prompt("prompts/fontes_confiaveis.md")

    json_format_instruction = """
IMPORTANT: Your final output MUST be a single, valid JSON object. Do not add any text before or after the JSON.
The JSON object must have the following structure:
{
  "summary": "A detailed summary of the findings based on the provided sources...",
  "sources": [
    {
      "url": "https://example.com/source1",
      "title": "Title of the article or document",
      "author": "Author Name(s)",
      "publication_date": "YYYY-MM-DD",
      "summary": "A brief summary of the key points from this specific source."
    }
  ],
  "notes": {
    "key_topic_1": "Detailed notes about the first key topic discovered...",
    "key_topic_2": "Detailed notes about the second key topic..."
  }
}
"""

    system_prompt = (
        f"{system_rules}\\n\\n"
        f"{sources_rules}\\n\\n"
        "LISTA DE FONTES CONFIÁVEIS (USO OBRIGATÓRIO):\\n"
        f"{trusted_sources}\\n\\n"
        f"{json_format_instruction}"
    )

    # 3. Initialize the client and call the OpenAI API
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    result = {}
    usage = {}

    try:
        response = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_task}
            ],
            temperature=config["temperature"],
            response_format={"type": "json_object"},
        )

        response_content = response.choices[0].message.content
        result = json.loads(response_content)

        usage = {
            "model": config["model"],
            "used_k": response.usage.total_tokens / 1000,
            "max_k": config["max_context_tokens"] / 1000,
            "used_tokens": response.usage.total_tokens,
            "max_context_tokens": config["max_context_tokens"],
        }

    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        result = {
            "summary": "Error: Could not retrieve data from OpenAI API.",
            "sources": [],
            "notes": {},
        }
        usage = {
            "model": config.get("model", "unknown"),
            "used_k": 0,
            "max_k": config.get("max_context_tokens", 0) / 1000,
            "used_tokens": 0,
            "max_context_tokens": config.get("max_context_tokens", 0),
        }

    # 4. Save the output files
    raw_dir = os.path.join(session_dir, "01_raw")
    os.makedirs(raw_dir, exist_ok=True)

    with open(os.path.join(raw_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(result.get("summary", "No summary generated."))

    with open(os.path.join(raw_dir, "sources.json"), "w", encoding="utf-8") as f:
        json.dump(result.get("sources", []), f, indent=2, ensure_ascii=False)

    notes_dir = os.path.join(raw_dir, "notes")
    os.makedirs(notes_dir, exist_ok=True)
    notes_content = result.get("notes", {})
    if isinstance(notes_content, dict):
        for topic, content in notes_content.items():
            filename = f"{topic.replace(' ', '_').lower()}.md"
            with open(os.path.join(notes_dir, filename), "w", encoding="utf-8") as f:
                f.write(content)

    return result, usage
