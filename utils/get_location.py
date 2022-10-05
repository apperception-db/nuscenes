from typing import Dict


def get_location(data: Dict[str, Dict[str, dict]], scene: str) -> str:
    log = data["log"]
    scenes = data["scene"]
    for token, s in scenes.items():
        if token == scene or s == scene:
            return log[s["log_token"]]
    raise Exception()
