def readable_memory(memory: int) -> str:
    if memory >= 1024 ** 3:
        return f"{round(memory / 1024 ** 3, 2)} GB"
    elif memory >= 1024 ** 2:
        return f"{round(memory / 1024 ** 2, 2)} MB"
    elif memory >= 1024:
        return f"{round(memory / 1024, 2)} KB"
    return f"{memory} B"
