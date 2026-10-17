from pathlib import Path
from pydantic import BaseModel

def get_project_root() -> Path:
    # Risale le cartelle finché non trova il file di controllo del progetto
    for p in Path(__file__).parents:
        if (p / ".git").exists() or (p / "requirements.txt").exists():
            return p
    return Path(__file__).parent # Fallback se non trova nulla

def _merge_models[T: BaseModel](current: T, new: T) -> T:
    merged: dict = {}
    for field in type(current).model_fields:
        old_val, new_val = getattr(current, field), getattr(new, field)
        if isinstance(old_val, BaseModel) and isinstance(new_val, BaseModel):
            merged[field] = _merge_models(old_val, new_val)
        else:
            merged[field] = old_val if new_val is None else new_val
    return type(current).model_validate(merged)