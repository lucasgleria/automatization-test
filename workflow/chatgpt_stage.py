import os


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
    with open(os.path.join(raw_dir, "summary.md"), "w") as f:
        f.write(result["summary"])

    return result, usage
