"""The module responsible for making data readable."""


def readable_memory(memory: int) -> str:
    """Convert the amount of memory to a readable format."""
    if memory >= 1024**3:
        return f"{round(memory / 1024 ** 3, 2)} GB"
    elif memory >= 1024**2:
        return f"{round(memory / 1024 ** 2, 2)} MB"
    elif memory >= 1024:
        return f"{round(memory / 1024, 2)} KB"
    return f"{memory} B"
