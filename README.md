# imagekit-skills

Install [ImageKit](https://imagekit.io) Agent Skills and MCP configuration for your AI coding tools — **one command, zero config**.

Works with **GitHub Copilot**, **Claude Code**, **Cursor**, **Codex**, and any [Agent Skills](https://agentskills.io) compatible client.

---

## Quick Start

Run this in your project directory:

```bash
uvx imagekit-skills install
```

That's it. You now have ImageKit skills available in your AI coding tool.

---

## What Gets Installed

### Skills

| Skill | What it does |
|-------|-------------|
| `search-docs` | Search ImageKit documentation — ask about features, APIs, SDKs, transformations |
| `transformation-builder` | Build image/video transformation URLs from natural language |

### Where skills go

By default, skills are installed to `.agents/skills/` in your project — the universal [Agent Skills standard](https://agentskills.io/specification) directory recognized by all compatible clients.

---

## Installation Options

### Install with `uv` (recommended)

No install needed — just run:

```bash
uvx imagekit-skills install
```

Or install persistently:

```bash
uv pip install imagekit-skills
imagekit-skills install
```

### Install with `pip`

```bash
pip install imagekit-skills
imagekit-skills install
```

---

## Usage

### Basic usage

```bash
# Install skills to current project (.agents/skills/)
imagekit-skills install

# Install globally — available across all projects
imagekit-skills install --global
```

### Target a specific AI tool

If you want client-specific directories and MCP config:

```bash
imagekit-skills install --client copilot    # .github/skills/ + .vscode/mcp.json
imagekit-skills install --client claude     # .claude/skills/ + .claude/settings.json
imagekit-skills install --client cursor     # .cursor/skills/ + .cursor/mcp.json
imagekit-skills install --client codex      # .agents/skills/ + .codex/config.json
imagekit-skills install --client all        # all of the above
```

> When you use `--client`, the CLI also configures the [ImageKit MCP server](https://api-mcp.imagekit.in) in that client's config so your AI tool can call ImageKit APIs directly.

### Install a specific skill

```bash
imagekit-skills install search-docs
imagekit-skills install transformation-builder
```

### Preview before installing

```bash
imagekit-skills install --dry-run
```

### Other commands

```bash
imagekit-skills list                        # show available skills
imagekit-skills status                      # show what's installed where
imagekit-skills status --client claude      # check a specific client
imagekit-skills remove                      # remove all skills
imagekit-skills remove search-docs          # remove a specific skill
imagekit-skills --help                      # full help
```

---

## What Each Flag Does

| Flag | Description |
|------|-------------|
| `--global` | Install to your home directory (`~/`) instead of the current project |
| `--client <name>` | Target a specific client: `copilot`, `claude`, `cursor`, `codex`, or `all` |
| `--skills-only` | Install skills but skip MCP config |
| `--mcp-only` | Configure MCP but skip skills |
| `--dry-run` | Show what would happen without making changes |

---

## How It Works

```
imagekit-skills install
        │
        ▼
┌──────────────────────────┐
│ Copies SKILL.md files to │
│ .agents/skills/          │
└──────────────────────────┘
        │
        ▼
Your AI tool discovers the skills automatically
        │
        ▼
You type: "search ImageKit docs for overlay examples"
        │
        ▼
AI uses the search-docs skill → calls ImageKit MCP → returns answer
```

When you use `--client`, it also writes MCP server config so your AI tool knows how to reach the ImageKit API:

```json
{
  "imagekit_api": {
    "url": "https://api-mcp.imagekit.in/sse"
  }
}
```

---

## Examples

### "How do I resize images with ImageKit?"

After installing, just ask your AI tool naturally. The `search-docs` skill activates and searches ImageKit documentation for you.

### "Generate an ImageKit URL that crops to 400x300 with smart crop and converts to WebP"

The `transformation-builder` skill activates and uses the ImageKit MCP to build the transformation URL.

---

## Supported Clients

| Client | Skills Directory | MCP Config |
|--------|-----------------|------------|
| **GitHub Copilot** (VS Code) | `.github/skills/` | `.vscode/mcp.json` |
| **Claude Code** | `.claude/skills/` | `.claude/settings.json` |
| **Cursor** | `.cursor/skills/` | `.cursor/mcp.json` |
| **OpenAI Codex** | `.agents/skills/` | `.codex/config.json` |
| **Any Agent Skills client** | `.agents/skills/` | — |

---

## Uninstall

Remove skills from current project:

```bash
imagekit-skills remove
```

Remove globally:

```bash
imagekit-skills remove --global
```

Uninstall the CLI itself:

```bash
pip uninstall imagekit-skills
```
