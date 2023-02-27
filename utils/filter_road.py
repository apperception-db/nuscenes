import json
import os
from typing import Callable, Dict, Set


def filter_road(path: str, tokens: "Set[str]", transform: "bool" = False) -> dict:
    val = validator(tokens)
    t = transformer()

    out = {}
    for k, v in val.items():
        with open(os.path.join(path, k + ".json"), "r") as f:
            content = json.load(f)
        print("Filtering", k)
        if transform:
            out[k] = [*map(t[k], filter(v, content))]
        else:
            out[k] = [*filter(v, content)]

    return out


def transformer() -> "Dict[str, Callable[[dict], dict]]":
    def factory(**config) -> "Callable[[dict], dict]":
        def v(e: dict) -> dict:
            assert {*config.keys()} == {*e.keys()}
            return {
                k: (None if (e[k] is None or v is None) else (e[k] if len(v) == 0 else e[k][: -len(v)]))
                for k, v in config.items()
            }

        return v

    def roadSection(e: dict) -> dict:
        assert {"id", "forwardLanes", "backwardLanes"} == {*e.keys()}
        return {
            'id': e['id'][: - len('_sec')],
            'forwardLanes': [lane[: -len("_sec")] for lane in e['forwardLanes']],
            'backwardLanes': [lane[: -len("_sec")] for lane in e['backwardLanes']]
        }

    return {
        "intersection": factory(id="_inter", road=""),
        "lane_LaneSec": factory(laneSec="_sec", lane=""),
        "lane": factory(id=""),
        "laneGroup_Lane": factory(laneGroup="", lane=""),
        "laneGroup_opposite": factory(lane="", opposite=""),
        "laneGroup": factory(id=""),
        "laneSection": factory(
            id="_sec",
            laneToLeft="_sec",
            laneToRight="_sec",
            fasterLane="_sec",
            slowerLane="_sec",
            isForward=None,
        ),
        "polygon": factory(id="", polygon=None),
        "road_laneGroup": factory(laneGroup="", road=""),
        "road_roadSec": factory(roadSec="_sec", road=""),
        "road": factory(id="", forwardLanes="", backwardLanes=""),
        "roadSec_laneSec": factory(laneSec="_sec", roadSec="_sec"),
        "roadSection": roadSection,
        "segment": factory(polygonId="", heading=None, end=None, start=None),
    }

def is_hex(h: 'str'):
    try:
        int(h, 16)
        return True
    except:
        return False

def is_token(token) -> "bool":
    if not isinstance(token, str):
        return False

    chunks = token.split('-')
    if len(chunks) != 5:
        return False
    
    if [len(c) for c in chunks] != [8, 4, 4, 4, 12]:
        return False
    
    return all(map(is_hex, chunks))


def get_token(token: 'str') -> 'str':
    token = token.split('_')[0]
    assert is_token(token), token
    return token


def validator(tokens: "Set[str]") -> "Dict[str, Callable[[dict], bool]]":
    def factory(**config) -> "Callable[[dict], bool]":
        def v(e: dict) -> bool:
            assert {*config.keys()} == {*e.keys()}
            values = (
                get_token(e[k]) in tokens
                for k, v in config.items()
                if v is not None and e[k] is not None
            )
            if all(values):
                return True
            elif all(not v for v in values):
                return False
            print(e)
            print(*config.items())
            raise Exception(
                [
                    (e[k], k, v)
                    for k, v in config.items()
                    if v is not None and e[k] is not None
                ]
            )

        return v

    def roadSection(e: dict) -> bool:
        assert {"id", "forwardLanes", "backwardLanes"} == {*e.keys()}
        values = (
            get_token(e["id"]) in tokens,
            *(get_token(lane) in tokens for lane in e["forwardLanes"]),
            *(get_token(lane) in tokens for lane in e["backwardLanes"]),
        )
        if all(values):
            return True
        elif all(not v for v in values):
            return False
        raise Exception()

    return {
        "intersection": factory(id="_inter", road=""),
        "lane_LaneSec": factory(laneSec="_sec", lane=""),
        "lane": factory(id=""),
        "laneGroup_Lane": factory(laneGroup="", lane=""),
        "laneGroup_opposite": factory(lane="", opposite=""),
        "laneGroup": factory(id=""),
        "laneSection": factory(
            id="_sec",
            laneToLeft="_sec",
            laneToRight="_sec",
            fasterLane="_sec",
            slowerLane="_sec",
            isForward=None,
        ),
        "polygon": factory(id="", polygon=None),
        "road_laneGroup": factory(laneGroup="", road=""),
        "road_roadSec": factory(roadSec="_sec", road=""),
        "road": factory(id="", forwardLanes="", backwardLanes=""),
        "roadSec_laneSec": factory(laneSec="_sec", roadSec="_sec"),
        "roadSection": roadSection,
        "segment": factory(polygonId="", heading=None, end=None, start=None),
    }
