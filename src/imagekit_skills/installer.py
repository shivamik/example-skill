from __future__ import annotations

import importlib.resources
import shutil
from pathlib import Path

from .clients import ClientConfig, CLIENTS, ALL_CLIENT_NAMES, UNIVERSAL
from .mcp_config import merge_mcp_config


def _skills_package_dir() -> Path:
    """Return the path to the bundled skills/ directory inside this package."""
    ref = importlib.resources.files("imagekit_skills") / "skills"
    # Traversable → concrete Path
    return Path(str(ref))


def get_available_skills() -> list[str]:
    """List skill names bundled with this package."""
    skills_dir = _skills_package_dir()
    return sorted(
        d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    )


def _resolve_clients(client: str | None) -> list[ClientConfig]:
    """Resolve client flag to list of ClientConfig.

    None  -> universal (.agents/skills/) — default
    'all' -> every client-specific directory
    name  -> single client
    """
    if client is None:
        return [UNIVERSAL]
    if client == "all":
        return list(CLIENTS.values())
    if client in CLIENTS:
        return [CLIENTS[client]]
    raise ValueError(
        f"Unknown client: {client!r}. Choose from: {', '.join(ALL_CLIENT_NAMES)}"
    )


def install_skills(
    *,
    skill_names: list[str] | None = None,
    client: str | None = None,
    global_install: bool = False,
    skills_only: bool = False,
    mcp_only: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """Install skills and/or MCP config. Returns list of status messages."""
    messages: list[str] = []
    clients = _resolve_clients(client)

    available = get_available_skills()
    if skill_names:
        for name in skill_names:
            if name not in available:
                messages.append(
                    f"  ✗ Unknown skill: {name!r}. Available: {', '.join(available)}"
                )
                return messages
        skills_to_install = skill_names
    else:
        skills_to_install = available

    skills_src = _skills_package_dir()

    # Install skills
    if not mcp_only:
        for cc in clients:
            base = cc.skill_base(global_install=global_install)
            for skill_name in skills_to_install:
                src = skills_src / skill_name
                dest = base / skill_name
                if dry_run:
                    messages.append(f"  → Would install {skill_name} to {dest}")
                    continue
                dest.mkdir(parents=True, exist_ok=True)
                # Copy all files in the skill directory
                for src_file in src.iterdir():
                    shutil.copy2(src_file, dest / src_file.name)
                action = (
                    "Updated" if (dest / "SKILL.md").stat().st_size > 0 else "Installed"
                )
                messages.append(f"  ✓ Installed {skill_name} → {dest}")

    # Install MCP config
    if not skills_only:
        for cc in clients:
            if not cc.project_mcp_file:  # universal has no MCP file
                continue
            msg = merge_mcp_config(cc, global_install=global_install, dry_run=dry_run)
            if msg:
                messages.append(msg)

    return messages


def remove_skills(
    *,
    skill_names: list[str] | None = None,
    client: str | None = None,
    global_install: bool = False,
) -> list[str]:
    """Remove installed skills. Returns list of status messages."""
    messages: list[str] = []
    clients = _resolve_clients(client)

    available = get_available_skills()
    skills_to_remove = skill_names if skill_names else available

    for cc in clients:
        base = cc.skill_base(global_install=global_install)
        for skill_name in skills_to_remove:
            dest = base / skill_name
            if dest.exists():
                shutil.rmtree(dest)
                messages.append(f"  ✓ Removed {skill_name} from {dest}")
            else:
                messages.append(f"  • {skill_name} not found in {dest}")

    return messages


def get_status(*, client: str | None = None, global_install: bool = False) -> list[str]:
    """Check what's installed. Returns list of status messages."""
    messages: list[str] = []
    clients = _resolve_clients(client)
    available = get_available_skills()

    for cc in clients:
        messages.append(f"\n  {cc.name}:")
        base = cc.skill_base(global_install=global_install)
        for skill_name in available:
            dest = base / skill_name / "SKILL.md"
            if dest.exists():
                messages.append(f"    ✓ {skill_name} installed at {dest.parent}")
            else:
                messages.append(f"    ✗ {skill_name} not installed")

        if not cc.project_mcp_file:  # universal has no MCP file
            continue
        config_path = cc.mcp_file(global_install=global_install)
        if config_path.exists():
            try:
                import json

                config = json.loads(config_path.read_text())
                servers = config.get(cc.mcp_servers_key, {})
                if "imagekit_api" in servers:
                    messages.append(f"    ✓ MCP configured in {config_path}")
                else:
                    messages.append(f"    ✗ MCP not configured in {config_path}")
            except (json.JSONDecodeError, ValueError):
                messages.append(f"    ✗ {config_path} is malformed")
        else:
            messages.append(f"    ✗ MCP config not found ({config_path})")

    return messages
