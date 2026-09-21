import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"

def folder_name(title):
    return re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

created = 0

for book in books:
    book_id = book["Book ID"]
    category = book["Category"]
    title = book["Book Title"]
    chapters = int(book["Chapters Planned"])

    book_folder = (
        BOOKS_DIR
        / category
        / f"{book_id}_{folder_name(title)}"
    )

    chapters_folder = book_folder / "05_CHAPTERS"
    plan_file = book_folder / "BOOK_CHAPTER_PLAN.md"

    lines = [
        f"# Chapter Plan: {title}",
        "",
        f"**Book ID:** {book_id}",
        f"**Category:** {category}",
        f"**Planned chapters:** {chapters}",
        "",
        "---",
        "",
        "## Chapter planning framework",
        "",
        "Each chapter should develop a distinct part of the book's central subject.",
        "Chapter titles and subjects should be specific to the book rather than generic placeholders.",
        "",
        "## Planned chapters",
        ""
    ]

    for number in range(1, chapters + 1):
        chapter_file = (
            chapters_folder
            / f"CHAPTER_{number:02d}"
            / f"CHAPTER_{number:02d}.md"
        )

        lines.extend([
            f"### Chapter {number}",
            "",
            f"**File:** `05_CHAPTERS/CHAPTER_{number:02d}/CHAPTER_{number:02d}.md`",
            "",
            "**Chapter title:** [To be developed]",
            "",
            "**Central question:** [What important question does this chapter answer?]",
            "",
            "**Major concepts:**",
            "- [Concept 1]",
            "- [Concept 2]",
            "- [Concept 3]",
            "",
            "**Research requirements:**",
            "- [Source or evidence requirement]",
            "- [Source or evidence requirement]",
            "",
            "**Expected contribution to the book:**",
            "[Explain how this chapter advances the overall subject of the book.]",
            "",
            "---",
            ""
        ])

    plan_file.write_text("\n".join(lines), encoding="utf-8")
    created += 1

print(f"Chapter plans created for {created} books.")
print("Every book now has a dedicated BOOK_CHAPTER_PLAN.md file.")
