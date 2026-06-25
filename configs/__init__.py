from pathlib import Path

import yaml

DEFAULT_CONFIG = Path(__file__).parent / "default.yaml"


def load_config(path=None):
    """load a YAML config file and return the parsed nested dict."""
    path = Path(path) if path is not None else DEFAULT_CONFIG
    with open(path) as f:
        return yaml.safe_load(f)


def apply_overrides(cfg, overrides):
    """apply dotted-key=value CLI overrides to a config dict in place"""
    for ov in overrides:
        if "=" not in ov:
            raise ValueError(f'override "{ov}" must be of the form key.subkey=value')
        key, raw_val = ov.split("=", 1)
        try:
            val = yaml.safe_load(raw_val)
        except yaml.YAMLError:
            val = raw_val
        keys = key.split(".")
        node = cfg
        for k in keys[:-1]:
            if k not in node or not isinstance(node[k], dict):
                node[k] = {}
            node = node[k]
        node[keys[-1]] = val
    return cfg
