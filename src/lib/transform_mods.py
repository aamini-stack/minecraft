# pyright: basic
from typing import Any


def flatten_mods(data: Any) -> list[str]:
    mods: list[str] = []

    def recurse(obj) -> None:
        if isinstance(obj, dict):
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, str):
                    mods.append(item)
                recurse(item)

    recurse(data)
    return sorted(mods, key=lambda x: x.lower())
