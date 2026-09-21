from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"


def safe_name(text):
    return (
        text.upper()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("?", "")
        .replace('"', "")
        .replace("'", "_")
    )


with TRACKER.open("r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))


total_planned = 0
total_files = 0
mismatches = []


for book in books:
    planned = int(book["Chapters Planned"])
    total_planned += planned

    book_folder = (
        ROOT
        / "BOOKS"
        / book["Category"]
        / f"{book['Book ID']}_{safe_name(book['Book Title'])}"
    )

    chapters_folder = book_folder / "05_CHAPTERS"

    chapter_files = list(
        chapters_folder.glob("CHAPTER_*/CHAPTER_*.md")
    )

    actual = len(chapter_files)
    total_files += actual

    if actual != planned:
        mismatches.append(
            (
                book["Book ID"],
                book["Book Title"],
                planned,
                actual
            )
        )


print("=" * 60)
print("CHAPTER FILE VERIFICATION")
print("=" * 60)
print()
print(f"Books: {len(books)}")
print(f"Planned chapters: {total_planned:,}")
print(f"Chapter files: {total_files:,}")
print(f"Books with chapter count mismatch: {len(mismatches)}")
print()

if mismatches:
    print("Mismatches:")
    for item in mismatches:
        print(
            f"{item[0]} | {item[1]} | "
            f"Planned: {item[2]} | Actual: {item[3]}"
        )
else:
    print("All books have the correct number of chapter files.")