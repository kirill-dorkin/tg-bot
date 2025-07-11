"""Core session management utilities for Telethon and Pyrogram."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional

from telethon import TelegramClient
from telethon.errors import PhoneNumberBannedError
from telethon.sessions import StringSession

from telegram_reaction_bot_main.converters import SessionConvertor


class SessionManager:
    """Manage account sessions for Telethon and Pyrogram clients."""

    def __init__(self, work_dir: Path):
        self.work_dir = Path(work_dir)
        self.sessions_dir = self.work_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def list_sessions(self) -> List[Path]:
        """Return available Telethon session files."""
        return list(self.sessions_dir.glob("*.session"))

    async def add_account(
        self, phone: str, api_id: int, api_hash: str
    ) -> Path:
        """Interactively log in a new account and save the session."""
        session_path = self.sessions_dir / f"{phone}.session"
        client = TelegramClient(session_path.stem, api_id, api_hash)
        await client.start(phone=lambda: phone)
        await client.disconnect()
        return session_path

    async def remove_account(self, phone: str) -> None:
        """Delete session for the given phone number."""
        path = self.sessions_dir / f"{phone}.session"
        if path.exists():
            path.unlink()

    async def filter_banned(self, api_id: int, api_hash: str) -> List[str]:
        """Return list of banned accounts and delete their sessions."""
        banned = []
        for session_file in self.list_sessions():
            client = TelegramClient(session_file.stem, api_id, api_hash)
            await client.connect()
            try:
                await client.send_code_request(session_file.stem)
            except PhoneNumberBannedError:
                banned.append(session_file.stem)
                session_file.unlink()
            finally:
                await client.disconnect()
        return banned

    async def telethon_to_pyrogram(self, session_file: Path, api_id: int, api_hash: str) -> None:
        """Convert Telethon session to Pyrogram session."""
        convertor = SessionConvertor(session_file, {"api_id": api_id, "api_hash": api_hash}, self.work_dir)
        await convertor.convert()
