"""Persistence helpers for mechanism objects.

Provides:
- save_mechanisms(mechanisms, path='mechanisms.npy', fmt=None, overwrite=False)
- load_mechanisms(path)

Supports .npy (numpy binary with pickling) and .json (human-readable) formats.
"""
from typing import List
import os
import json
import numpy as np


def _to_jsonable(obj):
    """Recursively convert numpy arrays and numpy scalars to Python lists and scalars for JSON serialization."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    return obj


def _maybe_restore_array(value):
    """Try to convert lists back to numpy arrays when it makes sense (numeric lists)."""
    if isinstance(value, list):
        if len(value) == 0:
            return np.array(value)
        # homogeneous numeric list
        if all(isinstance(x, (int, float, bool)) for x in value):
            return np.array(value)
        # list of lists of numbers -> 2D array
        if all(isinstance(x, list) and len(x) > 0 and all(isinstance(y, (int, float, bool)) for y in x) for x in value):
            return np.array(value)
    return value


def save_mechanisms(mechanisms: List[dict], path: str = 'mechanisms.npy', fmt: str = None, overwrite: bool = False):
    """Save a list of mechanisms to disk.

    Parameters
    - mechanisms: list of mechanism dicts (each mechanism uses numpy arrays for x0, edges, ...)
    - path: target filename (can include directory). Extension determines format if `fmt` is None.
    - fmt: 'npy' or 'json'. When None, inferred from path extension (default .npy).
    - overwrite: if False and file exists, raises a ValueError.
    """
    if fmt is None:
        _, ext = os.path.splitext(path)
        fmt = ext.lstrip('.').lower() or 'npy'
    fmt = fmt.lower()

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    if os.path.exists(path) and not overwrite:
        raise ValueError(f"File {path} already exists. Set overwrite=True to replace it.")

    if fmt == 'npy':
        # Use numpy's binary format with pickling to preserve types
        np.save(path, mechanisms, allow_pickle=True)
        print(f"Saved {len(mechanisms)} mechanisms to (npy): {os.path.abspath(path)}")
    elif fmt == 'json':
        jsonable = _to_jsonable(mechanisms)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(jsonable, f, indent=2)
        print(f"Saved {len(mechanisms)} mechanisms to (json): {os.path.abspath(path)}")
    else:
        raise ValueError("Unsupported format. Use 'npy' or 'json'.")


def load_mechanisms(path: str):
    """Load mechanisms previously saved by `save_mechanisms`.

    Automatically detects .npy or .json based on extension. Returns the mechanisms in the same structure
    as originally (numpy arrays for numeric fields when loading from JSON).
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    _, ext = os.path.splitext(path)
    ext = ext.lstrip('.').lower()

    if ext in ('npy', 'npz', ''):
        loaded = np.load(path, allow_pickle=True)
        try:
            if isinstance(loaded, np.ndarray) and loaded.dtype == object:
                return loaded.tolist()
            else:
                return loaded
        except Exception:
            return loaded

    elif ext == 'json':
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            restored = []
            for mech in data:
                if isinstance(mech, dict):
                    mech2 = {}
                    for k, v in mech.items():
                        mech2[k] = _maybe_restore_array(v)
                    restored.append(mech2)
                else:
                    restored.append(_maybe_restore_array(mech))
            return restored
        else:
            return _maybe_restore_array(data)
    else:
        raise ValueError('Unsupported file extension for loading mechanisms. Use .npy or .json')
