import os
import json


def run_chatgpt_stage(user_task, session_dir):
    # Placeholder function
    print("Running ChatGPT stage...")
    result = {
        "summary": "This is a placeholder summary from ChatGPT.",
        "sources": [],
        "notes": {},
    }
    usage = {
        "used_k": 0.0,
        "max_k": 8.0,
    }

    # Create placeholder files
    raw_dir = os.path.join(session_dir, "01_raw")
    os.makedirs(raw_dir, exist_ok=True)

    with open(os.path.join(raw_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write(result["summary"])

    with open(os.path.join(raw_dir, "sources.json"), "w", encoding="utf-8") as f:
        json.dump(result["sources"], f, indent=2, ensure_ascii=False)

    notes_dir = os.path.join(raw_dir, "notes")
    os.makedirs(notes_dir, exist_ok=True)

    return result, usage
