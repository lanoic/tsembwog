from typing import Dict
from threading import RLock

# In-memory feature flags with defaults; could be moved to DB in production
_FLAGS: Dict[str, bool] = {
    "use_gb_rego_price_model": True,
    "enable_dsr_lp_optimizer": True,
    "enable_btm_mpc": True,
    "enable_ab_bucket": True,
    "expose_metrics": True,
}

_LOCK = RLock()

def get_flags() -> Dict[str, bool]:
    with _LOCK:
        return dict(_FLAGS)

def set_flag(key: str, value: bool):
    with _LOCK:
        if key not in _FLAGS:
            raise KeyError("Unknown flag")
        _FLAGS[key] = value
