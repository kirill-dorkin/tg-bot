# Integration Plan for Telegram Automation Toolkit

This document proposes a high‑level architecture for combining the following projects:

1. **Telegram-Members-Adder-main** – bulk member management using Telethon.
2. **telegram-reaction-bot-main** – Pyrogram based bot that reacts to posts from multiple sessions.
3. **tgcf-main** – configurable forwarding framework with a plugin system.

## 1. Unified Architecture Overview

- **Core Session Manager**
  - Central module responsible for creating and storing session files for all accounts.
  - Provides utilities to add/remove accounts and check for banned sessions (reuse logic from `manager.py`).
  - Handles conversion between Telethon and Pyrogram sessions using code from `telegram-reaction-bot-main/converters/`.

- **Configuration Layer**
  - Use `tgcf`'s `Config` model to store API credentials and plugin settings.
  - Extend this model to include options for member‑adding and reaction tasks.
  - Support reading from a single YAML/JSON file or MongoDB (as done in `tgcf.config`).

- **Command Interface**
  - Build a Typer CLI (based on `tgcf/cli.py`) exposing subcommands:
    - `forward` – existing tgcf live/past forwarding.
    - `react` – start the reaction bot using loaded sessions.
    - `bulk` – run member adding or other mass actions.
  - Optionally provide a bot interface later using tgcf's web UI components.

- **Plugin System**
  - Reuse the plugin framework in `tgcf/plugins` to allow custom behaviour.
  - New plugins can hook into events before sending messages, reacting, or joining groups.
  - This keeps extension mechanisms consistent across all features.

- **Task Coordination**
  - Asynchronous workers will share the core session pool so that accounts are not used simultaneously for conflicting actions.
  - Reaction and forwarding loops should respect rate limits and maintain separate queues.

## 2. Components to Reuse or Refactor

### From Telegram-Members-Adder-main
- Member management logic in `add.py` for joining, leaving and adding users.
- Account handling functions in `manager.py` (adding accounts, filtering banned ones). These will be moved to the central session manager.
- Replace hard‑coded API credentials with values from the unified config.

### From telegram-reaction-bot-main
- Session conversion utilities in `converters/` for handling `.session`, `.ini`, and TD data folders.
- Reaction sending flow from `reactionbot.py`, refactored to obtain sessions from the shared manager and to emit events that plugins can hook into.
- Configuration examples from `config.py` showing how per‑session parameters are loaded.

### From tgcf-main
- The `Config` model and persistence helpers in `tgcf/config.py` for storing all settings.
- Typer-based CLI entry points from `tgcf/cli.py`.
- The plugin loader and `TgcfPlugin` infrastructure from `tgcf/plugins/__init__.py` and `tgcf/plugin_models.py`.
- Forwarding mechanics from `live.py` and `past.py` remain largely unchanged but will use the new session manager.

## 3. Next Steps

1. Implement the core session manager module and migrate account data from `vars.txt` and `sessions/` folders into a single location.
2. Refactor the reaction bot and member adder scripts to consume sessions via the new manager and to read configuration from `tgcf`'s config file.
3. Expose initial CLI commands (`forward`, `react`, `bulk`) that invoke the respective modules.
4. Gradually integrate plugins so that reactions and member addition can be customized using the same mechanisms used by tgcf.
