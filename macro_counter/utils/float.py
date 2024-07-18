def format_compact_float(num: float, digits: int = 1) -> str:
    q = 10 ** digits

    return f"{num * q // 1 / q:.{digits}f}".rstrip("0").rstrip(".")
