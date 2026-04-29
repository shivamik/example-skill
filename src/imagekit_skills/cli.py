from __future__ import annotations

import click

from .clients import VALID_CLIENT_CHOICES
from .installer import get_available_skills, get_status, install_skills, remove_skills


@click.group()
@click.version_option(package_name="imagekit-skills")
def cli():
    """ImageKit Skills — install Agent Skills & MCP config for AI coding tools."""


@cli.command()
@click.argument("skill_name", required=False, default=None)
@click.option(
    "--global", "global_install", is_flag=True, help="Install to user-level (~/)"
)
@click.option(
    "--client",
    type=click.Choice(VALID_CLIENT_CHOICES, case_sensitive=False),
    default=None,
    help="Target client (default: universal .agents/skills/)",
)
@click.option("--skills-only", is_flag=True, help="Skip MCP config")
@click.option("--mcp-only", is_flag=True, help="Skip skills, only configure MCP")
@click.option("--dry-run", is_flag=True, help="Preview without making changes")
def install(skill_name, global_install, client, skills_only, mcp_only, dry_run):
    """Install skills and MCP config.

    Optionally pass a SKILL_NAME to install a single skill.
    """
    skill_names = [skill_name] if skill_name else None
    scope = "globally" if global_install else f"in {click.format_filename('.')}"

    if dry_run:
        click.echo(f"\n🔍 Dry run — previewing install {scope}:\n")
    else:
        click.echo(f"\n📦 Installing ImageKit skills {scope}...\n")

    messages = install_skills(
        skill_names=skill_names,
        client=client,
        global_install=global_install,
        skills_only=skills_only,
        mcp_only=mcp_only,
        dry_run=dry_run,
    )

    for msg in messages:
        click.echo(msg)

    if not dry_run:
        click.echo("\n✅ Done!\n")


@cli.command("list")
def list_skills():
    """Show available skills."""
    skills = get_available_skills()
    click.echo(f"\n📋 Available skills ({len(skills)}):\n")
    for name in skills:
        click.echo(f"  • {name}")
    click.echo()


@cli.command()
@click.argument("skill_name", required=False, default=None)
@click.option(
    "--global", "global_install", is_flag=True, help="Remove from user-level (~/)"
)
@click.option(
    "--client",
    type=click.Choice(VALID_CLIENT_CHOICES, case_sensitive=False),
    default=None,
    help="Target client (default: universal .agents/skills/)",
)
def remove(skill_name, global_install, client):
    """Remove installed skills."""
    skill_names = [skill_name] if skill_name else None
    scope = "globally" if global_install else f"from {click.format_filename('.')}"

    click.echo(f"\n🗑  Removing ImageKit skills {scope}...\n")

    messages = remove_skills(
        skill_names=skill_names,
        client=client,
        global_install=global_install,
    )

    for msg in messages:
        click.echo(msg)

    click.echo("\n✅ Done!\n")


@cli.command()
@click.option("--global", "global_install", is_flag=True, help="Check user-level (~/)")
@click.option(
    "--client",
    type=click.Choice(VALID_CLIENT_CHOICES, case_sensitive=False),
    default=None,
    help="Target client (default: universal .agents/skills/)",
)
def status(global_install, client):
    """Show what's installed and where."""
    scope = "global" if global_install else "project"
    click.echo(f"\n📊 ImageKit Skills status ({scope}):")

    messages = get_status(client=client, global_install=global_install)

    for msg in messages:
        click.echo(msg)

    click.echo()
