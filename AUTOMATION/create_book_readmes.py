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
    target_pages = int(book["Target Pages"])
    target_words = int(book["Target Words"])

    book_folder = (
        BOOKS_DIR
        / category
        / f"{book_id}_{folder_name(title)}"
    )

    readme = book_folder / "README.md"

    content = f"""# {title}

**Book ID:** {book_id}  
**Category:** {category}  
**Status:** {book["Status"]}  

---

## Book profile

| Field | Target |
|---|---:|
| Minimum pages | {target_pages:,} |
| Target words | {target_words:,} |
| Planned chapters | {chapters} |
| Current pages | {book["Current Pages"]} |
| Current words | {book["Current Words"]} |
| Chapters completed | {book["Chapters Completed"]} |
| Completion | {book["Completion %"]}% |

## Purpose

This workspace contains the complete development environment for **{title}**.

The book will be developed through research, planning, writing, revision, editing, formatting, publication preparation, and progress tracking.

## Book structure

- `01_FRONT_MATTER` - Title page, copyright, dedication, acknowledgements and related material.
- `02_TABLE_OF_CONTENTS` - Automatically maintained table of contents.
- `03_PREFACE` - Author's preface.
- `04_INTRODUCTION` - Introduction to the book.
- `05_CHAPTERS` - Individual chapter workspaces.
- `06_CASE_STUDIES` - Case studies and detailed examples.
- `07_TABLES_AND_FIGURES` - Tables, charts, diagrams and figures.
- `08_RESEARCH_NOTES` - Research material and working notes.
- `09_SOURCES` - Source material.
- `10_REFERENCES` - References and bibliography.
- `11_GLOSSARY` - Important terms and definitions.
- `12_INDEX` - Index preparation.
- `13_PUBLISHING` - Publishing and distribution material.
- `14_PROGRESS` - Writing, editing and publication progress.

## Chapter system

This book contains **{chapters} planned chapters**.

Each chapter has its own folder and Markdown file so that chapters can be written, edited, reviewed and tracked independently.

## Writing target

The overall target is approximately **{target_words:,} words** and at least **{target_pages:,} pages**.

The final page count will be calculated during manuscript compilation rather than manually entered.

## Workflow

Research ? Planning ? Writing ? Review ? Editing ? Formatting ? Publication

## Progress tracking

Progress for this book will be synchronized with:

`BOOK_TRACKER/BOOK_MASTER_TRACKER.csv`

## Manuscript

The final manuscript will be assembled automatically from the individual chapter files.

## Publication

Publication preparation will include manuscript formatting, metadata, references, front matter, back matter, final quality checks and publication records.

---

**Repository:** BOOK_WRITING_PUBLISHING_TRACKING_COMMAND_CENTER
"""

    readme.write_text(content, encoding="utf-8")
    created += 1

print(f"Book README files created for {created} books.")
