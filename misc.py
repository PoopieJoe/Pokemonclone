from __future__ import annotations

def slicedict(dictionary:dict,keys:list[str]) -> dict:
    "Returns a dictionary subset of dictionary consisting of given keys"
    return {key:dictionary[key] for key in keys if key in dictionary}
