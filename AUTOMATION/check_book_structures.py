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

missing = []

for book in books:
    book_folder = (
        BOOKS_DIR
        / book["Category"]
        / f'{book["Book ID"]}_{folder_name(book["Book Title"])}'
    )

    chapters_folder = book_folder / "05_CHAPTERS"

    if not chapters_folder.exists():
        missing.append(f'{book["Book ID"]} - {book["Book Title"]}')

print("Missing book structures:")

if missing:
    for item in missing:
        print(item)
else:
    print("None")

print()
print(f"Total missing: {len(missing)}")
