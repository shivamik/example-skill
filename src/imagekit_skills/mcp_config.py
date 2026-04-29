from __future__ import annotations

import json
from pathlib import Path

from .clients import ClientConfig, MCP_SERVER_KEY


def merge_mcp_config(
    client: ClientConfig, *, global_install: bool, dry_run: bool = False
) -> str | None:
    """Merge ImageKit MCP entry into a client's config file.

    Returns a status message, or None if nothing was done.
    """
    config_path = client.mcp_file(global_install=global_install)
    servers_key = client.mcp_servers_key
    entry = client.mcp_entry()

    # Load existing config or start fresh
    config: dict = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except (json.JSONDecodeError, ValueError):
            return f"  ✗ {config_path} is malformed JSON — skipped (won't corrupt)"

    # Ensure servers section exists
    if servers_key not in config:
        config[servers_key] = {}

    # Check if already configured
    if MCP_SERVER_KEY in config[servers_key]:
        return f"  • {config_path} already has {MCP_SERVER_KEY} — skipped"

    if dry_run:
        return f"  → Would add {MCP_SERVER_KEY} to {config_path}"

    # Merge and write
    config[servers_key][MCP_SERVER_KEY] = entry
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(config, indent=2) + "\n")
    return f"  ✓ Configured MCP in {config_path}"
