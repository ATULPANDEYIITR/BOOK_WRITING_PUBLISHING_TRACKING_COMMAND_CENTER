from pathlib import Path
import csv
import re

ROOT = Path.cwd()
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

def tracker_name(text):
    return re.sub(r"[^A-Z0-9]+", "_", text.upper()).strip("_")

books = list(csv.DictReader(TRACKER.open(encoding="utf-8-sig")))

print("=" * 70)
print("BOOK WRITING COMMAND CENTER - COMPLETE SYSTEM AUDIT")
print("=" * 70)
print()

print("TRACKER")
print("-" * 70)
print(f"Books in tracker: {len(books)}")
print(f"Planned chapters: {sum(int(b['Chapters Planned']) for b in books):,}")
print(f"Target words: {sum(int(b['Target Words']) for b in books):,}")
print(f"Current words in tracker: {sum(int(b['Current Words'] or 0) for b in books):,}")
print(f"Completed chapters in tracker: {sum(int(b['Chapters Completed'] or 0) for b in books):,}")
print()

missing_books = []
chapter_mismatches = []
manuscript_missing = []
manuscript_words = 0
physical_chapters = 0
physical_book_folders = 0

for book in books:
    book_id = book["Book ID"]
    title = book["Book Title"]
    category = book["Category"]

    folder = ROOT / "BOOKS" / category / f"{book_id}_{safe_name(title)}"

    if not folder.exists():
        alternate = ROOT / "BOOKS" / category / f"{book_id}_{tracker_name(title)}"
        if alternate.exists():
            folder = alternate
        else:
            missing_books.append((book_id, title))
            continue

    physical_book_folders += 1

    chapters_folder = folder / "05_CHAPTERS"
    expected = int(book["Chapters Planned"])

    files = list(chapters_folder.glob("CHAPTER_*/CHAPTER_*.md"))
    actual = len(files)
    physical_chapters += actual

    if actual != expected:
        chapter_mismatches.append((book_id, title, expected, actual))

    for chapter_file in files:
        text = chapter_file.read_text(encoding="utf-8")

        if "## Manuscript" not in text:
            manuscript_missing.append((book_id, chapter_file.name))
            continue

        section = text.split("## Manuscript", 1)[1]

        if "---" in section:
            section = section.split("---", 1)[0]

        section = section.replace(
            "<!-- Write the completed chapter manuscript here. -->",
            ""
        ).strip()

        words = len(re.findall(r"\b[\w'-]+\b", section))
        manuscript_words += words

print("BOOK STRUCTURES")
print("-" * 70)
print(f"Book folders found: {physical_book_folders}")
print(f"Missing book folders: {len(missing_books)}")

if missing_books:
    for item in missing_books:
        print(f"  {item[0]} | {item[1]}")
print()

print("CHAPTER STRUCTURES")
print("-" * 70)
print(f"Expected chapter files: {sum(int(b['Chapters Planned']) for b in books):,}")
print(f"Physical chapter files found: {physical_chapters:,}")
print(f"Chapter count mismatches: {len(chapter_mismatches)}")

if chapter_mismatches:
    for item in chapter_mismatches:
        print(f"  {item[0]} | {item[1]} | Expected {item[2]} | Found {item[3]}")
print()

print("MANUSCRIPT SECTIONS")
print("-" * 70)
print(f"Manuscript words actually present: {manuscript_words:,}")
print(f"Chapter files missing Manuscript section: {len(manuscript_missing)}")

if manuscript_missing:
    for item in manuscript_missing[:50]:
        print(f"  {item[0]} | {item[1]}")

if len(manuscript_missing) > 50:
    print(f"  ... and {len(manuscript_missing) - 50} more")

print()

nonzero_tracker = [
    (b["Book ID"], b["Current Words"], b["Book Title"])
    for b in books
    if int(b["Current Words"] or 0) > 0
]

print("TRACKER VS ACTUAL MANUSCRIPT")
print("-" * 70)
print(f"Tracker Current Words: {sum(int(b['Current Words'] or 0) for b in books):,}")
print(f"Actual Manuscript Words: {manuscript_words:,}")
print(f"Books with non-zero tracker words: {len(nonzero_tracker)}")
print()

if nonzero_tracker:
    for item in nonzero_tracker:
        print(f"  {item[0]} | Tracker: {item[1]} | {item[2]}")

print()
print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
