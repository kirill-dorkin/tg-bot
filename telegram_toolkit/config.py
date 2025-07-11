"""Configuration models for the unified toolkit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

from tgcf_main.tgcf.config import Config as TgcfConfig, detect_config_type, read_config, write_config


class MemberAdderSettings(BaseModel):
    enable: bool = False
    source_chat: str = ""
    target_chat: str = ""


class ReactionSettings(BaseModel):
    enable: bool = False
    channels: list[str] = []


class ToolkitConfig(TgcfConfig):
    member_adder: MemberAdderSettings = MemberAdderSettings()
    reaction: ReactionSettings = ReactionSettings()


DEFAULT_PATH = Path("toolkit_config.yaml")


def load_config(path: Optional[Path] = None) -> ToolkitConfig:
    """Load configuration from YAML/JSON file or MongoDB."""
    if path is None:
        path = DEFAULT_PATH

    if path.exists():
        if path.suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(path.read_text())
        else:
            data = json.loads(path.read_text())
        base = ToolkitConfig(**data)
        write_config(base)  # persist using tgcf helpers
        return base

    # fall back to tgcf's detection (supports MongoDB)
    return ToolkitConfig(**read_config().dict())
