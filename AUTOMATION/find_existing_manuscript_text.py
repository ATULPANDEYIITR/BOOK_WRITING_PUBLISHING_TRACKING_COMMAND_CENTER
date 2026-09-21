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

results = []

for book in books:
    folder = (
        ROOT
        / "BOOKS"
        / book["Category"]
        / f"{book['Book ID']}_{safe_name(book['Book Title'])}"
        / "05_CHAPTERS"
    )

    words = 0

    for chapter_file in folder.glob("CHAPTER_*/CHAPTER_*.md"):
        content = chapter_file.read_text(encoding="utf-8")

        if "## Manuscript" not in content:
            continue

        manuscript = content.split("## Manuscript", 1)[1]

        if "---" in manuscript:
            manuscript = manuscript.split("---", 1)[0]

        manuscript = manuscript.replace("<!-- Write the completed chapter manuscript here. -->", "").strip()

        words += len(manuscript.split())

    if words > 0:
        results.append((book["Book ID"], book["Book Title"], words))

print("=" * 60)
print("EXISTING MANUSCRIPT TEXT")
print("=" * 60)
print()
print(f"Books containing manuscript text: {len(results)}")
print()

for book_id, title, words in results:
    print(f"{book_id} | {words:,} words | {title}")

print()
print(f"TOTAL MANUSCRIPT WORDS: {sum(x[2] for x in results):,}")
