import os


def get_config(key: str, default: str | None = None) -> str | None:
    """Resolve a setting from environment variables, then Colab userdata, then the default."""
    value = os.getenv(key)
    if value is not None:
        return value

    try:
        from google.colab import userdata
        return userdata.get(key)
    except Exception:
        # Not running in Colab, or the secret doesn't exist / isn't accessible
        return default
