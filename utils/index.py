from typing import Dict, List


def index(data: "List[dict]", key: str = "token") -> "Dict[str, dict]":
    return {d[key]: d for d in data}
