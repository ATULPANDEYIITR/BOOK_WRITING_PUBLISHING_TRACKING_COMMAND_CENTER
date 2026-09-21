from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

with TRACKER.open("r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

for book in books:
    book["Current Words"] = "0"
    book["Chapters Completed"] = "0"
    book["Completion %"] = "0"
    book["Status"] = "Planned"
    book["Writing Status"] = "Not Started"
    book["Editing Status"] = "Not Started"
    book["Publishing Status"] = "Not Started"
    book["Last Updated"] = ""

with TRACKER.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print("=" * 60)
print("TRACKER RESET")
print("=" * 60)
print()
print(f"Books reset: {len(books)}")
print("Current Words: 0")
print("Chapters Completed: 0")
print("Completion: 0%")
print("Status: Planned")
print()
print("Book content and chapter structures were not modified.")
