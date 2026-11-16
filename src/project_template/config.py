"""TOML configs with `base = "other.toml"` inheritance and `key.sub=value` overrides."""

import copy
import tomllib
from pathlib import Path


def deep_merge(a: dict, b: dict) -> dict:
    """b over a; nested tables merge key by key, everything else is replaced."""
    out = copy.deepcopy(a)
    for k, v in b.items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def load_config(path: Path, overrides: list[str] = ()) -> dict:
    """Read `path`, merge it over its `base` file (relative to it), then apply overrides."""
    cfg = tomllib.loads(path.read_text())
    if base := cfg.pop("base", None):
        cfg = deep_merge(load_config(path.parent / base), cfg)
    for item in overrides:
        key, sep, raw = item.partition("=")
        if not sep:
            raise ValueError(f"override {item!r} is not key=value")
        try:
            val = tomllib.loads(f"v = {raw}")["v"]  # numbers, bools, lists, quoted strings
        except tomllib.TOMLDecodeError:
            val = raw  # bare word: keep as a string
        *parents, leaf = key.strip().split(".")
        node = cfg
        for p in parents:
            node = node.get(p)
            if not isinstance(node, dict):
                raise KeyError(f"unknown config key {key!r}")
        if leaf not in node:
            raise KeyError(f"unknown config key {key!r}")  # a typo must not silently do nothing
        node[leaf] = val
    return cfg
