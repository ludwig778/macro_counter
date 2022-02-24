from typing import Any


def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
