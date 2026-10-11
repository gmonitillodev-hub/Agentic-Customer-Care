from pathlib import Path

def get_project_root() -> Path:
    # Risale le cartelle finché non trova il file di controllo del progetto
    for p in Path(__file__).parents:
        if (p / ".git").exists() or (p / "requirements.txt").exists():
            return p
    return Path(__file__).parent # Fallback se non trova nulla