import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT / "AUTOMATION" / "BOOK_CONFIG.json"
TRACKER_FILE = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)

with open(TRACKER_FILE, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

print("BOOK WRITING COMMAND CENTER")
print("=" * 40)
print(f"Minimum pages: {config['minimum_pages']}")
print(f"Target words: {config['target_words']}")
print(f"Minimum chapters: {config['minimum_chapters']}")
print(f"Maximum chapters: {config['maximum_chapters']}")
print(f"Books in tracker: {len(books)}")
print()

if len(books) == 180:
    print("All 180 books loaded successfully.")
else:
    print(f"WARNING: Expected 180 books but found {len(books)}.")
