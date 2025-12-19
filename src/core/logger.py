from __future__ import annotations
import logging, os, re
from typing import Iterable, List

DEFAULT_MASK_KEYS = ["token","authorization","password","secret","api_key"]

def _patterns(extra: Iterable[str] | None) -> List[re.Pattern]:
    ps: List[re.Pattern] = []
    for k in DEFAULT_MASK_KEYS:
        ps.append(re.compile(rf"({k}\s*[:=]\s*)([^\s,;]+)", re.IGNORECASE))
    if extra:
        for s in extra:
            if s:
                ps.append(re.compile(re.escape(s)))
    return ps

class MaskingFormatter(logging.Formatter):
    def __init__(self, fmt: str, extra_secrets: Iterable[str] | None = None):
        super().__init__(fmt)
        self.ps = _patterns(extra_secrets)

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        for p in self.ps:
            msg = p.sub(lambda m: m.group(1) + "***", msg) if p.groups >= 2 else p.sub("***", msg)
        return msg

def get_logger(name="securenetops"):
    lvl = os.getenv("LOG_LEVEL","INFO").upper()
    lg = logging.getLogger(name)
    if lg.handlers:
        return lg
    lg.setLevel(lvl)
    h = logging.StreamHandler()
    extra = [os.getenv("CONTROLLER_API_TOKEN","")]
    h.setFormatter(MaskingFormatter("%(asctime)s %(levelname)s %(name)s - %(message)s", extra))
    lg.addHandler(h)
    lg.propagate = False
    return lg
