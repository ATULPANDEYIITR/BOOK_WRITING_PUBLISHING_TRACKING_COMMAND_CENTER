import csv
from pathlib import Path
from collections import Counter
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
DASHBOARD = ROOT / "BOOK_TRACKER" / "COMMAND_CENTER_DASHBOARD.md"

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

total_books = len(books)
total_planned_words = sum(int(b["Target Words"]) for b in books)
total_current_words = sum(int(b["Current Words"]) for b in books)
total_planned_chapters = sum(int(b["Chapters Planned"]) for b in books)
total_completed_chapters = sum(int(b["Chapters Completed"]) for b in books)

planned = sum(1 for b in books if b["Status"] == "Planned")
in_progress = sum(1 for b in books if b["Status"] == "In Progress")
completed = sum(1 for b in books if b["Status"] == "Completed")

word_completion = (
    total_current_words / total_planned_words * 100
    if total_planned_words else 0
)

chapter_completion = (
    total_completed_chapters / total_planned_chapters * 100
    if total_planned_chapters else 0
)

overall_completion = (word_completion + chapter_completion) / 2

categories = Counter(b["Category"] for b in books)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

lines = [
    "# Book Writing, Publishing & Tracking Command Center",
    "",
    f"**Last updated:** {now}",
    "",
    "## Portfolio overview",
    "",
    "| Metric | Value |",
    "|---|---:|",
    f"| Total books | {total_books:,} |",
    f"| Planned books | {planned:,} |",
    f"| Books in progress | {in_progress:,} |",
    f"| Completed books | {completed:,} |",
    f"| Planned words | {total_planned_words:,} |",
    f"| Written words | {total_current_words:,} |",
    f"| Planned chapters | {total_planned_chapters:,} |",
    f"| Completed chapters | {total_completed_chapters:,} |",
    f"| Word completion | {word_completion:.2f}% |",
    f"| Chapter completion | {chapter_completion:.2f}% |",
    f"| Overall writing completion | {overall_completion:.2f}% |",
    "",
    "## Books by category",
    "",
    "| Category | Books |",
    "|---|---:|"
]

for category, count in sorted(categories.items()):
    lines.append(f"| {category} | {count} |")

lines.extend([
    "",
    "## Status",
    "",
    "| Status | Books |",
    "|---|---:|",
    f"| Planned | {planned} |",
    f"| In Progress | {in_progress} |",
    f"| Completed | {completed} |",
    "",
    "## Source",
    "",
    "`BOOK_TRACKER/BOOK_MASTER_TRACKER.csv`",
    "",
    "This dashboard is generated automatically from the master tracker.",
])

DASHBOARD.write_text("\n".join(lines), encoding="utf-8")

print("Command-center dashboard created.")
print(f"Total books: {total_books}")
print(f"Planned words: {total_planned_words:,}")
print(f"Written words: {total_current_words:,}")
print(f"Planned chapters: {total_planned_chapters:,}")
print(f"Completed chapters: {total_completed_chapters:,}")
print(f"Overall completion: {overall_completion:.2f}%")
print(f"Dashboard: {DASHBOARD}")
