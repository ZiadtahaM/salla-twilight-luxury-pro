"""
Determinism helpers — make everything *around* the LLM deterministic.

LLM calls stay non-deterministic. Tools, I/O, time, randomness — all tighten up.
"""

from __future__ import annotations
import functools
import random
import hashlib
import json
import os
from typing import Any


def seed_everything(seed: int = 42) -> None:
    random.seed(seed)
    # numpy / torch if present
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
    os.environ["PYTHONHASHSEED"] = str(seed)


def deterministic(fn):
    """Decorator: cache the result of a pure function on its arguments."""
    cache: dict[tuple, Any] = {}
    misses = {"n": 0, "hits": 0}

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = _hash_args(args, kwargs)
        if key in cache:
            misses["hits"] += 1
            return cache[key]
        misses["n"] += 1
        result = fn(*args, **kwargs)
        cache[key] = result
        return result

    wrapper.cache = cache  # type: ignore
    wrapper.stats = misses  # type: ignore
    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


def _hash_args(args: tuple, kwargs: dict) -> str:
    raw = json.dumps({"a": list(args), "k": kwargs}, default=str, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def snapshot(value: Any, label: str = "snap") -> str:
    """Return a stable string fingerprint of `value`. Use as a golden test."""
    raw = json.dumps(value, default=str, sort_keys=True)
    return f"{label}:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"
