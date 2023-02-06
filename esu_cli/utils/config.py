"""
To read the configuration file containing values, passwords, tokens, etc.

These are used in various places throughout the project
"""
import os
from pathlib import Path

import yaml


def _get_config_env_var():
    _key = "ESU_CONFIG"
    file_path = os.environ[_key]
    if file_path is None:
        raise ValueError(f"The environment variable {_key} must be set")
    return file_path


def _verify_file(file: Path):
    if not file.suffix == ".yaml":
        raise ValueError("The configuration file must be a .yaml")
    if not file.exists():
        raise FileNotFoundError(
            f"The file {file} was not found. The config file "
            f"under the ESU_CONFIG environment variable"
        )


def get_config() -> dict:
    p_config = Path(_get_config_env_var()).absolute()
    _verify_file(p_config)
    with open(p_config) as f:
        return yaml.safe_load(f)
