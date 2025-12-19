from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional
import os, yaml

class ConfigError(RuntimeError): ...

def load_yaml(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"Config file not found: {p}")
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    return data or {}

def env(name: str, default: Optional[str] = None) -> str:
    v = os.getenv(name, default)
    if v is None:
        raise ConfigError(f"Missing env var: {name}")
    return v
