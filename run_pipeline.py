import argparse
from workflow.orchestrator import run_pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the AI workflow pipeline."
    )
    parser.add_argument(
        "task", type=str, help="The main task or question for the pipeline."
    )
    args = parser.parse_args()
    run_pipeline(args.task)
