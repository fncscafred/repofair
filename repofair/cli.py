"""
Command-line interface for repofair.

Run:  python -m repofair.cli [repo_path] [--json]
"""

import argparse
import json
import sys

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from .scorer import score_repo

console = Console()

_FAIR_COLORS = {
    "F": "bright_cyan",
    "A": "bright_green",
    "I": "bright_yellow",
    "R": "bright_magenta",
}


def _fair_markup(fair_str: str) -> str:
    parts = fair_str.split("+")
    colored = []
    for p in parts:
        color = _FAIR_COLORS.get(p.strip(), "white")
        colored.append(f"[{color}]{p.strip()}[/{color}]")
    return "+".join(colored)


def _score_bar(percentage: float, width: int = 38) -> str:
    filled = int(width * percentage / 100)
    empty = width - filled
    return f"{'█' * filled}{'░' * empty}"


def render_report(report: dict) -> None:
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]repofair[/bold cyan]  ·  FAIR Repository Audit",
            subtitle=f"[dim]{report['repo_path']}[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    table = Table(
        show_header=True,
        header_style="bold white on grey23",
        box=box.ROUNDED,
        border_style="dim",
        expand=False,
        padding=(0, 1),
    )
    table.add_column("Check", style="bold", min_width=16)
    table.add_column("FAIR", justify="center", min_width=7)
    table.add_column("Status", justify="center", min_width=10)
    table.add_column("Score", justify="right", min_width=7)
    table.add_column("Details")

    for check in report["checks"]:
        if check["passed"]:
            status = "[bold green]✓ PASS[/bold green]"
            score_cell = f"[green]{check['score']}/{check['max_score']}[/green]"
        else:
            status = "[bold red]✗ FAIL[/bold red]"
            score_cell = f"[red]{check['score']}/{check['max_score']}[/red]"

        table.add_row(
            check["check"],
            _fair_markup(check["fair"]),
            status,
            score_cell,
            f"[dim]{check['message']}[/dim]",
        )

    console.print(table)
    console.print()

    pct = report["percentage"]
    total = report["total_score"]
    max_s = report["max_score"]

    if pct >= 80:
        bar_color, grade, grade_style = "green", "Excellent", "bold green"
    elif pct >= 60:
        bar_color, grade, grade_style = "yellow", "Good", "bold yellow"
    elif pct >= 40:
        bar_color, grade, grade_style = "dark_orange", "Fair", "bold dark_orange"
    else:
        bar_color, grade, grade_style = "red", "Needs Work", "bold red"

    bar = _score_bar(pct)
    score_line = (
        f"  [{bar_color}]{bar}[/{bar_color}]  "
        f"[{grade_style}]{pct:.1f}%[/{grade_style}]  "
        f"[dim]({total}/{max_s} pts)[/dim]  "
        f"[{grade_style}]{grade}[/{grade_style}]"
    )

    console.print(
        Panel(
            score_line,
            title="[bold]FAIR Score[/bold]",
            border_style=bar_color,
        )
    )

    console.print()
    console.print(
        "[dim]FAIR key: "
        "[bright_cyan]F[/bright_cyan]=Findable  "
        "[bright_green]A[/bright_green]=Accessible  "
        "[bright_yellow]I[/bright_yellow]=Interoperable  "
        "[bright_magenta]R[/bright_magenta]=Reusable[/dim]"
    )
    console.print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="repofair",
        description="Audit a Git repository for FAIR Open Science compliance.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  repofair .\n"
            "  repofair /path/to/repo\n"
            "  repofair . --json\n"
        ),
    )
    parser.add_argument(
        "repo_path",
        nargs="?",
        default=".",
        help="Path to the local repository (default: current directory)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON (for CI pipelines)",
    )

    args = parser.parse_args()
    report = score_repo(args.repo_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        render_report(report)

    if report["percentage"] < 50:
        sys.exit(1)


if __name__ == "__main__":
    main()
