from pathlib import Path
import secrets
import string

def get_root_dir() -> Path:
    return Path(__file__).parent.parent.parent


def generate_numeric_password(length: int = 20) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))
