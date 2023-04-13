from pathlib import Path


def get_project_absolute_path() -> str:
    return Path(__file__).parent.parent.resolve()
