from typing import List


def unique(data: "List[dict]", key: str = "token") -> "set":
    return {d[key] for d in data}
