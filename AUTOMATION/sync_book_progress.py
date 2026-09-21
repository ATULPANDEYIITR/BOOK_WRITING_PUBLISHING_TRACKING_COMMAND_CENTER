import csv
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"

def folder_name(title):
    return re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")

def count_words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))

def manuscript_text(text):
    if "## Manuscript" not in text:
        return ""

    section = text.split("## Manuscript", 1)[1]

    if "## Chapter conclusion" in section:
        section = section.split("## Chapter conclusion", 1)[0]

    if "---" in section:
        section = section.split("---", 1)[0]

    return section.strip()

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for book in books:
    book_folder = (
        BOOKS_DIR
        / book["Category"]
        / f'{book["Book ID"]}_{folder_name(book["Book Title"])}'
    )

    chapters_folder = book_folder / "05_CHAPTERS"

    if not chapters_folder.exists():
        continue

    chapter_files = sorted(chapters_folder.glob("CHAPTER_*/CHAPTER_*.md"))

    total_words = 0
    completed_chapters = 0

    for chapter_file in chapter_files:
        text = chapter_file.read_text(encoding="utf-8")
        manuscript = manuscript_text(text)

        words = count_words(manuscript)
        total_words += words

        if words >= 1000:
            completed_chapters += 1

    planned_chapters = int(book["Chapters Planned"])
    target_words = int(book["Target Words"])

    chapter_progress = (
        completed_chapters / planned_chapters
        if planned_chapters else 0
    )

    word_progress = (
        total_words / target_words
        if target_words else 0
    )

    completion = min(
        100,
        round(((chapter_progress * 0.5) + (word_progress * 0.5)) * 100, 2)
    )

    book["Current Words"] = str(total_words)
    book["Chapters Completed"] = str(completed_chapters)
    book["Completion %"] = str(completion)
    book["Last Updated"] = now

    if total_words == 0:
        book["Status"] = "Planned"
        book["Writing Status"] = "Not Started"
    elif completion >= 100:
        book["Status"] = "Completed"
        book["Writing Status"] = "Completed"
    else:
        book["Status"] = "In Progress"
        book["Writing Status"] = "In Progress"

with open(TRACKER, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print("Progress calculation corrected.")
print("Only text inside the Manuscript sections is counted.")
print("Template instructions are no longer counted as book words.")
