from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


MCP_URL = "https://api-mcp.imagekit.in/sse"
MCP_SERVER_KEY = "imagekit_api"


@dataclass
class ClientConfig:
    name: str
    # Skill paths (relative to project root or ~)
    project_skills_dir: str
    global_skills_dir: str
    # MCP config
    project_mcp_file: str
    global_mcp_file: str
    mcp_servers_key: str  # "servers" for Copilot, "mcpServers" for others
    supports_url: bool = True  # native SSE/URL support

    def skill_base(self, *, global_install: bool) -> Path:
        if global_install:
            return Path.home() / self.global_skills_dir
        return Path.cwd() / self.project_skills_dir

    def mcp_file(self, *, global_install: bool) -> Path:
        if global_install:
            return Path.home() / self.global_mcp_file
        return Path.cwd() / self.project_mcp_file

    def mcp_entry(self) -> dict:
        if self.supports_url:
            return {"url": MCP_URL}
        return {
            "command": "npx",
            "args": ["-y", "mcp-remote@latest", MCP_URL],
        }


# Universal path — works across all Agent Skills-compatible clients
UNIVERSAL = ClientConfig(
    name="Universal (all clients)",
    project_skills_dir=".agents/skills",
    global_skills_dir=".agents/skills",
    project_mcp_file="",  # no single MCP file for universal
    global_mcp_file="",
    mcp_servers_key="",
    supports_url=True,
)

CLIENTS: dict[str, ClientConfig] = {
    "copilot": ClientConfig(
        name="VS Code / Copilot",
        project_skills_dir=".github/skills",
        global_skills_dir=".copilot/skills",
        project_mcp_file=".vscode/mcp.json",
        global_mcp_file=".vscode/mcp.json",
        mcp_servers_key="servers",
        supports_url=True,
    ),
    "claude": ClientConfig(
        name="Claude Code",
        project_skills_dir=".claude/skills",
        global_skills_dir=".claude/skills",
        project_mcp_file=".claude/settings.json",
        global_mcp_file=".claude/settings.json",
        mcp_servers_key="mcpServers",
        supports_url=True,
    ),
    "cursor": ClientConfig(
        name="Cursor",
        project_skills_dir=".cursor/skills",
        global_skills_dir=".cursor/skills",
        project_mcp_file=".cursor/mcp.json",
        global_mcp_file=".cursor/mcp.json",
        mcp_servers_key="mcpServers",
        supports_url=True,
    ),
    "codex": ClientConfig(
        name="Codex",
        project_skills_dir=".agents/skills",
        global_skills_dir=".agents/skills",
        project_mcp_file=".codex/config.json",
        global_mcp_file=".codex/config.json",
        mcp_servers_key="mcpServers",
        supports_url=False,
    ),
}

ALL_CLIENT_NAMES = list(CLIENTS.keys())
VALID_CLIENT_CHOICES = ["all"] + ALL_CLIENT_NAMES
