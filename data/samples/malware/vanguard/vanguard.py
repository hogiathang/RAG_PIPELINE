#!/usr/bin/env python3
"""
The Vanguard: Scout Swarm Protocol

Uses Claude Code CLI agents directly - no API key needed.
"""

import asyncio
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

console = Console()

# --- SCOUT VECTORS (Deliberately Divergent) ---
SCOUT_VECTORS = [
    ("Contrarian", "You are a CONTRARIAN SCOUT. Assume the mainstream consensus on this topic is WRONG. Search for evidence that contradicts the conventional wisdom. What are experts missing?"),
    ("Failure Hunter", "You are a FAILURE HUNTER. Search ONLY for failures, disasters, and negative examples related to this topic. What has gone wrong? What are the cautionary tales?"),
    ("Dissenting Expert", "You are searching for DISSENTING EXPERTS. Find credible voices who disagree with the mainstream view. Who are the qualified skeptics and what do they say?"),
    ("Global Lens", "You are a GLOBAL SCOUT. Search for perspectives from non-Western, non-English sources. What do experts in Asia, Africa, South America, or Europe say that Anglophone sources miss?"),
    ("Historical", "You are a HISTORICAL SCOUT. Search for historical parallels and precedents. What similar situations existed in the past? What can we learn from history?"),
    ("Edge Cases", "You are an EDGE CASE HUNTER. Find the unusual situations, exceptions, and boundary conditions. What are the weird cases that don't fit the normal pattern?"),
    ("Critic", "You are a PROFESSIONAL CRITIC. What would a hostile, well-informed critic say about this topic? What are the strongest arguments against?"),
    ("Academic", "You are an ACADEMIC SCOUT. Search for peer-reviewed research, technical papers, and scholarly analysis. What does rigorous research say vs popular commentary?"),
    ("Recent", "You are a RECENCY SCOUT. Focus ONLY on developments from the last 6 months. What's new? What has changed recently that might not be widely known?"),
    ("Blindspot", "You are a BLINDSPOT HUNTER. What is everyone missing? What questions aren't being asked? What's hiding in plain sight?"),
]

async def run_claude_agent(prompt: str, content: str) -> str:
    """Spawns a Claude Code agent via CLI.

    Uses stdin to pass prompts (avoids Windows 8,191 char cmd limit).
    """
    import shutil
    import platform
    full_prompt = f"{prompt}\n\n---\n\n{content}"

    if platform.system() == "Windows":
        claude_cmd = shutil.which("claude.cmd") or shutil.which("claude.exe") or "claude.cmd"
    else:
        claude_cmd = shutil.which("claude") or "claude"

    # Use stdin instead of -p argument to avoid command-line length limits
    proc = await asyncio.create_subprocess_exec(
        claude_cmd, "--print",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate(input=full_prompt.encode())

    if proc.returncode != 0:
        error_msg = stderr.decode() if stderr else "Unknown error"
        return f"Error: {error_msg}"

    return stdout.decode().strip()

async def run_scout(name: str, prompt: str, query: str) -> tuple:
    """Runs a single scout."""
    console.log(f"[bold blue]Scout {name}[/] deployed...")
    result = await run_claude_agent(prompt, f"Domain to scout: {query}")
    console.log(f"[bold green]Scout {name}[/] returned!")
    return (name, result)

async def main(query: str, num_scouts: int = 10):
    console.rule("[bold purple]The Vanguard: Scout Swarm Deployed")
    console.print(f"Target Domain: [italic]{query}[/italic]")
    console.print(f"Deploying {num_scouts} scouts with divergent search vectors\n")

    # Select scouts
    scouts = SCOUT_VECTORS[:num_scouts]

    # Deploy all scouts in parallel
    console.log(f"[bold]Scattering {num_scouts} scouts across the territory...[/]")
    tasks = [run_scout(name, prompt, query) for name, prompt in scouts]
    results = await asyncio.gather(*tasks)

    # Display results as a menu (NOT synthesized)
    console.rule("[bold purple]Scout Reports (Deliberately Unsynthesized)")
    console.print("[dim]Note: These reports are intentionally NOT merged to preserve outliers and edge cases.[/]\n")

    for name, report in results:
        console.print(Panel(
            Markdown(report),
            title=f"[bold]{name} Scout[/]",
            border_style="blue"
        ))
        console.print("")

    # Summary table
    table = Table(title="Scout Coverage Summary")
    table.add_column("Scout", style="cyan")
    table.add_column("Key Finding", style="green")

    for name, report in results:
        # Extract first line as key finding
        first_line = report.split('\n')[0][:80] if report else "No data"
        table.add_row(name, first_line + "...")

    console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Vanguard: Scout Swarm Protocol")
    parser.add_argument("query", help="The domain to scout")
    parser.add_argument("--scouts", type=int, default=10, help="Number of scouts (default: 10, max: 10)")

    args = parser.parse_args()
    num = min(args.scouts, 10)
    asyncio.run(main(args.query, num))
