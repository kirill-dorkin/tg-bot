"""Command line interface for the unified toolkit."""

from __future__ import annotations

import asyncio
import typer

from tgcf_main.tgcf.cli import verbosity_callback, version_callback
from tgcf_main.tgcf.live import start_sync
from tgcf_main.tgcf.past import forward_job

from .config import load_config
from .session_manager import SessionManager

app = typer.Typer(add_completion=False)


@app.command()
def forward(loud: bool = typer.Option(False, "--loud", "-l", callback=verbosity_callback)):
    """Run tgcf forwarding using unified config."""
    load_config()
    asyncio.run(start_sync())


@app.command()
def react():
    """Start reaction bot with loaded sessions."""
    # Placeholder for future reaction integration
    typer.echo("Reaction bot not yet implemented")


@app.command()
def bulk():
    """Run member adding and other bulk actions."""
    typer.echo("Bulk actions not yet implemented")


if __name__ == "__main__":
    app()
