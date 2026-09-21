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
    category = book["Category"]
    title = book["Book Title"]
    book_id = book["Book ID"]
    chapter_count = int(book["Chapters Planned"])

    book_folder = BOOKS_DIR / category / f"{book_id}_{folder_name(title)}"
    chapters_folder = book_folder / "05_CHAPTERS"

    chapters_folder.mkdir(parents=True, exist_ok=True)

    placeholder = chapters_folder / "CHAPTER_PLACEHOLDER"
    if placeholder.exists():
        placeholder.unlink()

    for number in range(1, chapter_count + 1):
        chapter_folder = chapters_folder / f"CHAPTER_{number:02d}"
        chapter_folder.mkdir(exist_ok=True)

        chapter_file = chapter_folder / f"CHAPTER_{number:02d}.md"

        if not chapter_file.exists():
            chapter_file.write_text(
                f"# Chapter {number}\n\n"
                f"## Chapter Overview\n\n"
                f"Chapter {number} of **{title}**.\n\n"
                f"## Content\n\n"
                f"Write the chapter content here.\n\n"
                f"## Key Concepts\n\n"
                f"- Concept 1\n"
                f"- Concept 2\n"
                f"- Concept 3\n\n"
                f"## Examples and Case Studies\n\n"
                f"Add relevant examples and case studies here.\n\n"
                f"## Chapter Summary\n\n"
                f"Summarize the major ideas covered in this chapter.\n\n"
                f"## References\n\n"
                f"Add chapter-specific references here.\n",
                encoding="utf-8"
            )

    created += 1

print(f"Chapter structures created for {created} books.")
print("Each book now has its assigned number of chapter folders.")
