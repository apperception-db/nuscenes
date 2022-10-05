import json
import os
from typing import Callable, Dict, Set


def filter_road(path: str, tokens: "Set[str]") -> dict:
    val = validator(tokens)

    out = {}
    for k, v in val.items():
        with open(os.path.join(path, k + ".json"), "r") as f:
            content = json.load(f)
        print("Filtering", k)
        out[k] = [*filter(v, content)]

    return out


def validator(tokens: "Set[str]") -> "Dict[str, Callable[[dict], bool]]":
    def factory(**config) -> "Callable[[dict], bool]":
        def v(e: dict) -> bool:
            assert {*config.keys()} == {*e.keys()}
            values = (
                (e[k] if len(v) == 0 else e[k][:-len(v)]) in tokens
                for k, v in config.items()
                if v is not None and e[k] is not None
            )
            if all(values):
                return True
            elif all(not v for v in values):
                return False
            print(e)
            print(*config.items())
            raise Exception([(e[k], k, v) for k, v in config.items() if v is not None and e[k] is not None])

        return v
    
    def roadSection(e: dict) -> bool:
        assert {"id", "forwardLanes", "backwardLanes"} == {*e.keys()}
        values = (
            e["id"][:-len("_sec")] in tokens,
            *(l[:-len("_sec")] in tokens for l in e["forwardLanes"]),
            *(l[:-len("_sec")] in tokens for l in e["backwardLanes"]),
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
        "laneSection": factory(id="_sec", laneToLeft="_sec", laneToRight="_sec", fasterLane="_sec", slowerLane="_sec", isForward=None),
        "polygon": factory(id="", polygon=None),
        "road_laneGroup": factory(laneGroup="", road=""),
        "road_roadSec": factory(roadSec="_sec", road=""),
        "road": factory(id="", forwardLanes="", backwardLanes=""),
        "roadSec_laneSec": factory(laneSec="_sec", roadSec="_sec"),
        "roadSection": roadSection,
        "segment": factory(polygonId="", heading=None, end=None, start=None),
    }