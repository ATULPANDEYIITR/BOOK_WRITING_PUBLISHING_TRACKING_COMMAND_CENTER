from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

with TRACKER.open("r", encoding="utf-8-sig", newline="") as f:
    books = list(csv.DictReader(f))

book = next(b for b in books if b["Book ID"] == "IPS-003")

book_folder = (
    ROOT
    / "BOOKS"
    / book["Category"]
    / "IPS-003_FEDERALISM_AND_INDIAS_UNION_STRUCTURE"
)

chapters_folder = book_folder / "05_CHAPTERS"
chapters_folder.mkdir(parents=True, exist_ok=True)

chapter_count = int(book["Chapters Planned"])

for number in range(1, chapter_count + 1):
    chapter_folder = chapters_folder / f"CHAPTER_{number:02d}"
    chapter_folder.mkdir(parents=True, exist_ok=True)

    chapter_file = chapter_folder / f"CHAPTER_{number:02d}.md"

    if not chapter_file.exists():
        chapter_file.write_text(
            f"# Chapter {number}\n\n"
            "## Manuscript\n\n"
            "Chapter manuscript will be written here.\n\n"
            "## References\n\n"
            "References will be added during research.\n\n"
            "## Research notes\n\n"
            "Research notes will be added here.\n",
            encoding="utf-8"
        )

print("=" * 60)
print("IPS-003 CHAPTER STRUCTURE")
print("=" * 60)
print()
print(f"Book: {book['Book Title']}")
print(f"Chapter files created: {chapter_count}")
print(f"Location: {chapters_folder}")
print()
print("IPS-003 chapter structure created successfully.")
print("No other books were modified.")
