import os
import json
from datetime import datetime
from workflow.chatgpt_stage import run_chatgpt_stage
from workflow.claude_stage import run_claude_stage


def create_session_id():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def create_session_dir(session_id):
    session_dir = os.path.join("data", "sessions", session_id)
    os.makedirs(session_dir, exist_ok=True)
    for sub_dir in ["01_raw", "02_processed", "03_final"]:
        os.makedirs(os.path.join(session_dir, sub_dir), exist_ok=True)
    return session_dir


def save_text(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def save_meta(session_dir, task, chatgpt_usage, claude_usage):
    meta_data = {
        "task": task,
        "chatgpt": chatgpt_usage,
        "claude": claude_usage,
    }
    with open(
        os.path.join(session_dir, "meta.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(meta_data, f, indent=2)


def run_pipeline(user_task):
    session_id = create_session_id()
    session_dir = create_session_dir(session_id)
    print(f"[OK] Sessão {session_id} criada.")

    save_text(os.path.join(session_dir, "task.txt"), user_task)

    chatgpt_result, chatgpt_usage = run_chatgpt_stage(user_task, session_dir)
    print(
        f"ChatGPT: {chatgpt_usage.get('used_k', 0):.1f}k tokens utilizados de "
        f"{chatgpt_usage.get('max_k', 0):.1f}k tokens"
    )
    print(
        f"[OK] Etapa 1 (ChatGPT) concluída. Arquivos em "
        f"{os.path.join(session_dir, '01_raw')}"
    )

    claude_result, claude_usage = run_claude_stage(
        user_task, session_dir, chatgpt_result
    )
    print(
        f"Claude: {claude_usage.get('used_k', 0):.1f}k tokens utilizados de "
        f"{claude_usage.get('max_k', 0):.1f}k tokens"
    )
    print(
        f"[OK] Etapa 2 (Claude) concluída. Estudo final em "
        f"{os.path.join(session_dir, '03_final', 'estudo_final.md')}"
    )

    save_meta(session_dir, user_task, chatgpt_usage, claude_usage)
