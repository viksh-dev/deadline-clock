import sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel

console = Console()

COURTS = {
    "ГПК": {"апелляция": 1, "кассация": 3, "надзор": 3},
    "АПК": {"апелляция": 1, "кассация": 2, "надзор": 3},
    "КАС": {"апелляция": 1, "кассация": 6, "надзор": 3},
    "УПК": {"апелляция": 0, "кассация": 6, "надзор": 12},
}

STAGE_NAMES = {
    "апелляция": "Апелляция",
    "кассация": "Первая кассация",
    "надзор": "Вторая кассация / надзор",
}

def parse_date(raw):
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d %B %Y", "%d.%m.%y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Не пойму дату: {raw}")

def bar_style(left):
    if left < 0:
        return "red"
    if left <= 5:
        return "red"
    if left <= 14:
        return "yellow"
    return "green"

def status(left):
    if left < 0:
        return "[red]пропущен[/red]"
    if left <= 5:
        return "[bold red]горит![/bold red]"
    if left <= 14:
        return "[yellow]пора[/yellow]"
    return "[green]спокойно[/green]"

def main():
    if len(sys.argv) < 3:
        console.print("[red]Нужен кодекс и дата[/red]")
        console.print("Пример: python clock.py АПК 15.01.2025")
        return

    code = sys.argv[1].upper()

    if code not in COURTS:
        console.print(f"[red]{code} нет в списке. Доступно: {', '.join(COURTS)}[/red]")
        return

    try:
        event_date = parse_date(sys.argv[2])
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        return

    today = date.today()
    stages = []

    for stage, months in COURTS[code].items():
        if months == 0:
            continue
        due = event_date + relativedelta(months=months)
        left = (due - today).days
        stages.append((STAGE_NAMES[stage], due, left))

    table = Table(title=f"[bold]Дедлайны — {code}[/bold]")
    table.add_column("Стадия", style="cyan")
    table.add_column("Крайняя дата", style="yellow")
    table.add_column("Осталось", style="green")
    table.add_column("Статус")

    for name, due, left in stages:
        d = f"{left} дн." if left > 0 else "—"
        table.add_row(name, due.strftime("%d.%m.%Y"), d, status(left))

    console.print(table)
    console.print("\n[bold]Прогресс:[/bold]\n")

    for name, due, left in stages:
        total = (due - event_date).days
        gone = total - left
        pct = max(0, min(100, int(gone / total * 100))) if total > 0 else 100
        color = bar_style(left)

        console.print(f"  {name}: {due.strftime('%d.%m.%Y')}")
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=50, style=color),
            TextColumn("{task.percentage:.0f}%"),
            transient=True,
        ) as progress:
            progress.add_task(description="", total=100, completed=pct)

    active = [s for s in stages if s[2] >= 0]
    if active:
        next_one = min(active, key=lambda s: s[2])
        name, due, left = next_one
        color = bar_style(left)
        console.print()
        console.print(Panel(
            f"[bold]{name}[/bold]\nдо {due.strftime('%d.%m.%Y')} — {left} дней",
            border_style=color,
            title="Ближайший дедлайн",
        ))

    if __name__ == "__main__":
        main()
