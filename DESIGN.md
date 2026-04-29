# ImageKit Skills Installer — Design Document

## 1. Overview

A CLI tool that installs ImageKit Agent Skills and MCP server configuration with a single command. Users run one command and get:

1. **Skills** — `SKILL.md` files placed in the correct directories
2. **MCP config** — ImageKit MCP server registered in the client's config

The CLI follows the open [Agent Skills standard](https://agentskills.io/specification) so skills work across **VS Code (Copilot)**, **Claude Code**, **Cursor**, and **Codex**.

---

## 2. User Journey

### Simplest case (install everything)
```bash
uvx imagekit-skills install
```

Or if installed as a persistent tool:
```bash
uv pip install imagekit-skills
imagekit-skills install
```

### Install for a specific client only
```bash
imagekit-skills install --client copilot
imagekit-skills install --client claude
imagekit-skills install --client cursor
imagekit-skills install --client codex
```

### Install globally (available across all projects)
```bash
imagekit-skills install --global
imagekit-skills install --global --client claude
```

### List available skills
```bash
imagekit-skills list
```

### Install a specific skill only
```bash
imagekit-skills install search-docs
imagekit-skills install transformation-builder
```

### Remove skills
```bash
imagekit-skills remove
imagekit-skills remove search-docs
```

---

## 3. CLI Commands

| Command | Description |
|---------|-------------|
| `imagekit-skills install [skill-name]` | Install all (or specific) skills + MCP config |
| `imagekit-skills install --global` | Install to user-level directories |
| `imagekit-skills install --client <name>` | Install only for a specific client |
| `imagekit-skills list` | Show available skills and their status |
| `imagekit-skills remove [skill-name]` | Remove installed skills |
| `imagekit-skills status` | Show what's installed and where |

### Flags

| Flag | Description |
|------|-------------|
| `--global` | Install to `~/` (user-level) instead of project-level |
| `--client` | Target a specific client: `copilot`, `claude`, `cursor`, `codex`, `all` (default) |
| `--skills-only` | Skip MCP config, only install skills |
| `--mcp-only` | Skip skills, only install MCP config |
| `--dry-run` | Show what would be installed without making changes |

---

## 4. Available Skills

### Skill 1: `search-docs`
- **Tool**: `search_docs` (from ImageKit MCP)
- **Purpose**: Search ImageKit documentation with AI understanding
- **Use case**: "How do I use overlays in ImageKit?" / "Find docs about video transformations"

### Skill 2: `transformation-builder`
- **Tool**: `transformation_builder` (from ImageKit MCP)
- **Purpose**: Build image/video transformation URLs from natural language
- **Use case**: "Resize this image to 300x200 with smart crop" / "Add a watermark overlay"

---

## 5. Skill Installation Paths

### Project-level (default: `imagekit-skills install`)

Skills are installed into the **current working directory**.

| Client | Skills Path |
|--------|-------------|
| **VS Code / Copilot** | `.github/skills/<skill-name>/SKILL.md` |
| **Claude Code** | `.claude/skills/<skill-name>/SKILL.md` |
| **Cursor** | `.cursor/skills/<skill-name>/SKILL.md` |
| **Codex** | `.agents/skills/<skill-name>/SKILL.md` |
| **Universal** | `.agents/skills/<skill-name>/SKILL.md` |

> **Note**: `.agents/skills/` is recognized by VS Code/Copilot, Codex, and most Agent Skills-compatible clients. When `--client all` is used, the CLI writes to **all** client-specific paths to maximize compatibility.

### User-level (`--global`)

| Client | Skills Path |
|--------|-------------|
| **VS Code / Copilot** | `~/.copilot/skills/<skill-name>/SKILL.md` |
| **Claude Code** | `~/.claude/skills/<skill-name>/SKILL.md` |
| **Cursor** | `~/.cursor/skills/<skill-name>/SKILL.md` |
| **Codex** | `~/.agents/skills/<skill-name>/SKILL.md` |
| **Universal** | `~/.agents/skills/<skill-name>/SKILL.md` |

---

## 6. MCP Server Configuration

ImageKit MCP is a **hosted remote server** — nothing is installed locally. The CLI just writes a config entry pointing to `https://api-mcp.imagekit.in/sse` so the client knows how to connect.

### How MCP Connection Works

```
[AI Client (Copilot/Claude/Cursor/Codex)]
    ↓ reads config
[Config file tells client: "connect to https://api-mcp.imagekit.in/sse"]
    ↓ SSE or stdio bridge
[ImageKit Hosted MCP Server]
    ↓ exposes tools
[search_docs, transformation_builder, + 40 other tools]
```

### Config Format Per Client

**Modern clients with native SSE/URL support** (preferred, no Node.js needed):

```json
{
  "imagekit_api": {
    "url": "https://api-mcp.imagekit.in/sse"
  }
}
```

**Clients requiring stdio transport** (needs Node.js + `npx`):

```json
{
  "imagekit_api": {
    "command": "npx",
    "args": ["-y", "mcp-remote@latest", "https://api-mcp.imagekit.in/sse"]
  }
}
```

> `mcp-remote` is a thin bridge that translates stdio ↔ SSE. It's only needed when the client doesn't support remote URLs natively.

### Client Support Matrix

| Client | Native URL/SSE? | Config Format |
|--------|----------------|---------------|
| **VS Code / Copilot** | Yes | `"url": "https://..."` |
| **Claude Code** | Yes | `"url": "https://..."` |
| **Cursor** | Yes | `"url": "https://..."` |
| **Codex** | Depends on version | Falls back to `npx mcp-remote` |

The CLI auto-detects the best format for each client.

### MCP Config Locations

| Client | Config File | Key Path |
|--------|-------------|----------|
| **VS Code / Copilot** (project) | `.vscode/mcp.json` | `servers.imagekit_api` |
| **VS Code / Copilot** (global) | `~/.vscode/mcp.json` | `servers.imagekit_api` |
| **Claude Code** (project) | `.claude/settings.json` | `mcpServers.imagekit_api` |
| **Claude Code** (global) | `~/.claude/settings.json` | `mcpServers.imagekit_api` |
| **Cursor** (project) | `.cursor/mcp.json` | `mcpServers.imagekit_api` |
| **Cursor** (global) | `~/.cursor/mcp.json` | `mcpServers.imagekit_api` |
| **Codex** | `~/.codex/config.json` | `mcpServers.imagekit_api` |

### MCP Config Merge Strategy

- If config file **doesn't exist** → create it with the ImageKit entry
- If config file **exists but no `imagekit_api`** → merge the entry in
- If config file **exists and has `imagekit_api`** → skip (don't overwrite), print message
- **Never delete** other entries in the config file

---

## 7. SKILL.md Templates

### `search-docs/SKILL.md`

```markdown
---
name: search-docs
description: >
  Search ImageKit documentation to find guides, API references, and examples.
  Use when the user asks about ImageKit features, APIs, SDKs, transformations,
  configuration, or troubleshooting. Also use when the user needs to look up
  specific parameters, supported formats, or integration guides.
---

# ImageKit Documentation Search

When the user asks about ImageKit features, APIs, or how to do something with ImageKit:

1. Use the `search_docs` MCP tool to find relevant documentation
2. Pass the user's query as the search term
3. Review the returned results and synthesize a clear answer
4. Include code examples when the docs provide them
5. Link to relevant documentation sections for further reading

## When to Use

- User asks "How do I..." related to ImageKit
- User needs API reference information
- User wants to understand ImageKit features or pricing
- User is troubleshooting an ImageKit integration
- User asks about supported formats, limits, or configuration

## Example Queries

- "How do I add a watermark to images in ImageKit?"
- "What are the supported image formats?"
- "How to set up ImageKit with Next.js?"
- "What URL parameters control image quality?"

## Tips

- Be specific with search queries for better results
- If the first search doesn't return relevant results, try rephrasing
- Combine multiple search results to give comprehensive answers
```

### `transformation-builder/SKILL.md`

```markdown
---
name: transformation-builder
description: >
  Build ImageKit image and video transformation URLs from natural language
  descriptions. Use when the user wants to resize, crop, overlay, format,
  optimize, or apply any visual transformation to images or videos using
  ImageKit. Also use when the user provides an ImageKit URL and wants to
  modify its transformations.
---

# ImageKit Transformation Builder

When the user wants to transform an image or video:

1. Use the `transformation_builder` MCP tool
2. Pass the user's natural language description of the desired transformation
3. Return the generated transformation URL or parameters
4. Explain what each transformation parameter does

## When to Use

- User wants to resize, crop, or reformat an image
- User wants to add overlays, watermarks, or text
- User wants to optimize images for web performance
- User wants to apply effects (blur, grayscale, contrast, etc.)
- User provides an ImageKit URL and wants modifications
- User asks to generate a transformation URL

## Example Requests

- "Resize this image to 400x300 with smart crop"
- "Add a watermark in the bottom-right corner"
- "Convert this to WebP with 80% quality"
- "Create a 200x200 thumbnail with face detection"
- "Apply a blur effect with radius 10"

## Tips

- Ask for the source image URL if not provided
- Suggest optimization parameters (format auto, quality auto) when appropriate
- Explain the transformation chain so users can modify it later
- For complex transformations, break them down step by step
```

---

## 8. Installation Flow (What Happens)

### `imagekit-skills install` (project-level, all clients)

```
1. Detect which clients are present in the project
   - .vscode/ exists → Copilot
   - .claude/ exists → Claude Code
   - .cursor/ exists → Cursor
   
2. Install skills
   For each detected client (or all if none detected):
   ├── Create .github/skills/search-docs/SKILL.md
   ├── Create .github/skills/transformation-builder/SKILL.md
   ├── Create .claude/skills/search-docs/SKILL.md
   ├── Create .claude/skills/transformation-builder/SKILL.md
   ├── Create .agents/skills/search-docs/SKILL.md
   └── Create .agents/skills/transformation-builder/SKILL.md

3. Install MCP config
   For each detected client:
   ├── Merge into .vscode/mcp.json
   ├── Merge into .claude/settings.json
   └── Merge into .cursor/mcp.json

4. Print summary
   ✓ Installed 2 skills for Copilot (.github/skills/)
   ✓ Installed 2 skills for Claude Code (.claude/skills/)
   ✓ Installed 2 skills for all clients (.agents/skills/)
   ✓ Configured ImageKit MCP in .vscode/mcp.json
   ✓ Configured ImageKit MCP in .claude/settings.json
```

### `imagekit-skills install --global --client claude`

```
1. Install skills
   ├── Create ~/.claude/skills/search-docs/SKILL.md
   └── Create ~/.claude/skills/transformation-builder/SKILL.md

2. Install MCP config
   └── Merge into ~/.claude/settings.json

3. Print summary
   ✓ Installed 2 skills globally for Claude Code
   ✓ Configured ImageKit MCP in ~/.claude/settings.json
```

---

## 9. Project Structure

```
imagekit-skills/
├── src/
│   └── imagekit_skills/
│       ├── __init__.py
│       ├── cli.py              # CLI entry point (click/typer)
│       ├── installer.py        # Core installation logic
│       ├── mcp_config.py       # MCP config merge logic
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── base.py         # Base client class
│       │   ├── copilot.py      # VS Code / Copilot paths & config
│       │   ├── claude.py       # Claude Code paths & config
│       │   ├── cursor.py       # Cursor paths & config
│       │   └── codex.py        # Codex paths & config
│       └── skills/
│           ├── __init__.py
│           ├── search-docs/
│           │   └── SKILL.md
│           └── transformation-builder/
│               └── SKILL.md
├── pyproject.toml
├── README.md
└── tests/
    ├── test_installer.py
    └── test_mcp_config.py
```

---

## 10. Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python | User preference |
| CLI framework | `click` | Lightweight, well-documented |
| Package manager | `uv` | Fast, modern Python tooling |
| Package format | PyPI (`uvx imagekit-skills` or `uv pip install imagekit-skills`) | Universal Python distribution |
| Config parsing | `json` (stdlib) | All config files are JSON |
| File ops | `pathlib` (stdlib) | Cross-platform path handling |
| Testing | `pytest` | Standard Python testing |
| MCP server | **Hosted** (no local install) | Zero dependency for end users |

---

## 11. Edge Cases & Safety

| Scenario | Behavior |
|----------|----------|
| Config file exists with `imagekit_api` | Skip, print "already configured" |
| Config file exists with other servers | Merge, preserve existing entries |
| Config file is malformed JSON | Print error, skip config, don't corrupt |
| Skills directory already has skill | Overwrite with latest version, print "updated" |
| No write permission | Print error with `sudo` suggestion (or use `--global`) |
| `npx` not installed | Use native URL config; only warn if client needs stdio bridge |
| Offline / no network | Skills install fine (bundled), MCP config is just JSON (server is remote) |

---

## 12. Future Enhancements

- [ ] `imagekit-skills update` — Update skills to latest version
- [ ] Interactive mode with prompts (which client? which skills?)
