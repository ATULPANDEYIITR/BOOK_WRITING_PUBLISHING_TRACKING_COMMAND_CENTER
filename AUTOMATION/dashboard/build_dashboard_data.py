from pathlib import Path
import csv
import json
import re
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[2]

TRACKER_FILE = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"
OUTPUT_FILE = ROOT / "dashboard" / "data" / "dashboard-data.json"


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def number(value):
    value = clean(value).replace(",", "")
    if not value:
        return 0.0

    try:
        return float(value)
    except ValueError:
        return 0.0


def integer(value):
    value = clean(value).replace(",", "")
    if not value:
        return 0

    try:
        return int(float(value))
    except ValueError:
        return 0


def slug(value):
    value = clean(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def safe_percentage(value):
    value = number(value)

    if value > 1:
        return round(value, 2)

    return round(value * 100, 2)


def normalize_status(value):
    value = clean(value)

    if not value:
        return "Not Started"

    return value


def find_book_directory(book_id, title):
    book_id = clean(book_id).lower()
    title_slug = slug(title)

    candidates = []

    if BOOKS_DIR.exists():
        for category_dir in BOOKS_DIR.iterdir():
            if not category_dir.is_dir():
                continue

            for book_dir in category_dir.iterdir():
                if not book_dir.is_dir():
                    continue

                name_lower = book_dir.name.lower()

                if book_id and name_lower.startswith(book_id):
                    return book_dir

                if title_slug and title_slug in slug(book_dir.name):
                    candidates.append(book_dir)

    if candidates:
        return candidates[0]

    return None


def chapter_word_count(chapter_file):
    try:
        text = chapter_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        return 0

    return len(re.findall(r"\b[\w'-]+\b", text))


def chapter_status(chapter_file):
    try:
        text = chapter_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    except Exception:
        return "Unreadable"

    stripped = text.strip()

    if not stripped:
        return "Not Started"

    lowered = stripped.lower()

    completed_markers = [
        "status: completed",
        "status: complete",
        "completed: true",
        "chapter status: completed",
        "chapter status: complete",
        "[x] completed",
        "## completed",
    ]

    for marker in completed_markers:
        if marker in lowered:
            return "Completed"

    words = chapter_word_count(chapter_file)

    if words < 25:
        return "Started"

    return "In Progress"


def scan_chapters(book_dir):
    chapters = []

    if not book_dir:
        return chapters

    chapters_dir = book_dir / "05_CHAPTERS"

    if not chapters_dir.exists():
        return chapters

    for chapter_dir in sorted(chapters_dir.iterdir()):
        if not chapter_dir.is_dir():
            continue

        match = re.search(
            r"CHAPTER[_ -]?(\d+)",
            chapter_dir.name,
            re.IGNORECASE
        )

        if not match:
            continue

        chapter_number = int(match.group(1))

        markdown_files = sorted(chapter_dir.glob("*.md"))

        if markdown_files:
            chapter_file = markdown_files[0]
        else:
            all_files = [
                p for p in chapter_dir.iterdir()
                if p.is_file()
            ]

            if all_files:
                chapter_file = all_files[0]
            else:
                chapter_file = None

        if chapter_file:
            words = chapter_word_count(chapter_file)
            status = chapter_status(chapter_file)

            relative_file = chapter_file.relative_to(ROOT).as_posix()
        else:
            words = 0
            status = "Not Started"
            relative_file = ""

        chapters.append(
            {
                "number": chapter_number,
                "name": chapter_dir.name,
                "status": status,
                "words": words,
                "file": relative_file,
            }
        )

    return chapters


def read_tracker():
    if not TRACKER_FILE.exists():
        raise FileNotFoundError(
            f"Tracker file not found: {TRACKER_FILE}"
        )

    with TRACKER_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        rows = []

        for row in reader:
            rows.append(
                {
                    clean(k): clean(v)
                    for k, v in row.items()
                }
            )

        return rows


def build_book(row):
    book_id = clean(row.get("Book ID"))
    category = clean(row.get("Category"))
    title = clean(row.get("Book Title"))

    book_dir = find_book_directory(
        book_id,
        title
    )

    chapters = scan_chapters(book_dir)

    actual_chapters = len(chapters)

    planned_chapters = integer(
        row.get("Chapters Planned")
    )

    completed_chapters = sum(
        1
        for chapter in chapters
        if chapter["status"] == "Completed"
    )

    current_words = integer(
        row.get("Current Words")
    )

    actual_words = sum(
        chapter["words"]
        for chapter in chapters
    )

    if actual_words > 0:
        current_words = actual_words

    target_words = integer(
        row.get("Target Words")
    )

    completion = safe_percentage(
        row.get("Completion %")
    )

    if completion == 0 and target_words > 0:
        completion = round(
            current_words / target_words * 100,
            2
        )

    repository_path = ""

    if book_dir:
        repository_path = book_dir.relative_to(ROOT).as_posix()

    return {
        "id": book_id,
        "category": category,
        "title": title,
        "status": normalize_status(row.get("Status")),
        "targetPages": integer(row.get("Target Pages")),
        "currentPages": integer(row.get("Current Pages")),
        "targetWords": target_words,
        "currentWords": current_words,
        "chaptersPlanned": planned_chapters,
        "chaptersCompleted": completed_chapters,
        "chaptersActual": actual_chapters,
        "researchStatus": normalize_status(
            row.get("Research Status")
        ),
        "writingStatus": normalize_status(
            row.get("Writing Status")
        ),
        "editingStatus": normalize_status(
            row.get("Editing Status")
        ),
        "publishingStatus": normalize_status(
            row.get("Publishing Status")
        ),
        "completion": completion,
        "startDate": clean(row.get("Start Date")),
        "targetCompletionDate": clean(
            row.get("Target Completion Date")
        ),
        "lastUpdated": clean(row.get("Last Updated")),
        "notes": clean(row.get("Notes")),
        "repositoryFound": book_dir is not None,
        "repositoryPath": repository_path,
        "chapters": chapters,
    }


def build_categories(books):
    categories = {}

    for book in books:
        category = book["category"] or "Uncategorized"

        if category not in categories:
            categories[category] = {
                "name": category,
                "books": 0,
                "chapters": 0,
                "completedChapters": 0,
                "words": 0,
                "targetWords": 0,
                "completionTotal": 0,
            }

        item = categories[category]

        item["books"] += 1
        item["chapters"] += book["chaptersActual"]
        item["completedChapters"] += book[
            "chaptersCompleted"
        ]
        item["words"] += book["currentWords"]
        item["targetWords"] += book["targetWords"]
        item["completionTotal"] += book["completion"]

    result = []

    for item in categories.values():
        books_count = item["books"]

        item["completion"] = round(
            item["completionTotal"] / books_count,
            2
        ) if books_count else 0

        del item["completionTotal"]

        result.append(item)

    result.sort(
        key=lambda x: (
            x["completion"],
            x["words"]
        ),
        reverse=True
    )

    return result


def build_pipeline(books):
    stages = [
        ("Research", "researchStatus"),
        ("Writing", "writingStatus"),
        ("Editing", "editingStatus"),
        ("Publishing", "publishingStatus"),
    ]

    pipeline = []

    for stage_name, field in stages:
        counts = {}

        for book in books:
            status = book[field]

            if status not in counts:
                counts[status] = 0

            counts[status] += 1

        pipeline.append(
            {
                "stage": stage_name,
                "statuses": counts,
            }
        )

    return pipeline


def build_attention(books):
    attention = []

    for book in books:

        if not book["repositoryFound"]:
            attention.append(
                {
                    "type": "Repository",
                    "severity": "High",
                    "bookId": book["id"],
                    "title": book["title"],
                    "message": "Book directory not found in BOOKS."
                }
            )

        if book["chaptersActual"] == 0:
            attention.append(
                {
                    "type": "Chapters",
                    "severity": "High",
                    "bookId": book["id"],
                    "title": book["title"],
                    "message": "No chapter directories detected."
                }
            )

        elif (
            book["chaptersPlanned"] > 0
            and book["chaptersActual"]
            < book["chaptersPlanned"]
        ):
            attention.append(
                {
                    "type": "Chapters",
                    "severity": "Medium",
                    "bookId": book["id"],
                    "title": book["title"],
                    "message": (
                        f"{book['chaptersActual']} actual chapters "
                        f"vs {book['chaptersPlanned']} planned."
                    )
                }
            )

        empty_chapters = [
            chapter["name"]
            for chapter in book["chapters"]
            if chapter["status"] == "Not Started"
        ]

        if empty_chapters:
            attention.append(
                {
                    "type": "Writing",
                    "severity": "Medium",
                    "bookId": book["id"],
                    "title": book["title"],
                    "message": (
                        f"{len(empty_chapters)} chapter(s) "
                        "have no content."
                    )
                }
            )

        if not book["notes"]:
            attention.append(
                {
                    "type": "Tracking",
                    "severity": "Low",
                    "bookId": book["id"],
                    "title": book["title"],
                    "message": "Tracker notes are empty."
                }
            )

    return attention


def build_summary(books, categories):
    total_books = len(books)

    total_chapters = sum(
        book["chaptersActual"]
        for book in books
    )

    completed_chapters = sum(
        book["chaptersCompleted"]
        for book in books
    )

    words = sum(
        book["currentWords"]
        for book in books
    )

    target_words = sum(
        book["targetWords"]
        for book in books
    )

    average_completion = (
        round(
            sum(book["completion"] for book in books)
            / total_books,
            2
        )
        if total_books
        else 0
    )

    book_statuses = {}

    for book in books:
        status = book["status"]

        book_statuses[status] = (
            book_statuses.get(status, 0) + 1
        )

    chapter_statuses = {}

    for book in books:
        for chapter in book["chapters"]:
            status = chapter["status"]

            chapter_statuses[status] = (
                chapter_statuses.get(status, 0) + 1
            )

    return {
        "totalBooks": total_books,
        "totalCategories": len(categories),
        "totalChapters": total_chapters,
        "completedChapters": completed_chapters,
        "wordsWritten": words,
        "targetWords": target_words,
        "averageCompletion": average_completion,
        "bookStatuses": book_statuses,
        "chapterStatuses": chapter_statuses,
    }


def main():
    print("=" * 70)
    print("BOOK WRITING & PUBLISHING COMMAND CENTER DATA BUILDER")
    print("=" * 70)

    print(f"Repository root : {ROOT}")
    print(f"Tracker file    : {TRACKER_FILE}")
    print(f"Books directory : {BOOKS_DIR}")
    print(f"Output file     : {OUTPUT_FILE}")
    print()

    print("Checking required paths...")

    if not ROOT.exists():
        raise FileNotFoundError(
            f"Repository root does not exist: {ROOT}"
        )

    if not TRACKER_FILE.exists():
        raise FileNotFoundError(
            f"Tracker CSV does not exist: {TRACKER_FILE}"
        )

    if not BOOKS_DIR.exists():
        raise FileNotFoundError(
            f"BOOKS directory does not exist: {BOOKS_DIR}"
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Required paths found.")
    print()

    print("Reading tracker...")

    rows = read_tracker()

    print(f"Tracker rows: {len(rows)}")
    print()

    print("Building book records...")

    books = []

    for index, row in enumerate(rows, start=1):
        try:
            book = build_book(row)
            books.append(book)
        except Exception as error:
            print(
                f"ERROR processing tracker row {index}: "
                f"{error}"
            )
            raise

    print(f"Books built: {len(books)}")
    print()

    print("Building categories...")

    categories = build_categories(books)

    print(f"Categories built: {len(categories)}")
    print()

    print("Building pipeline...")

    pipeline = build_pipeline(books)

    print()

    print("Building attention list...")

    attention = build_attention(books)

    print(
        f"Attention items: {len(attention)}"
    )
    print()

    summary = build_summary(
        books,
        categories
    )

    data = {
        "generatedAt": datetime.now(
            timezone.utc
        ).isoformat(),

        "generator": {
            "name": (
                "Book Writing & Publishing "
                "Tracking Command Center"
            ),
            "version": "2.0",
        },

        "summary": summary,

        "categories": categories,

        "books": books,

        "pipeline": pipeline,

        "attention": attention,
    }

    print("Writing JSON...")

    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print()
    print("=" * 70)
    print("BUILD SUCCESSFUL")
    print("=" * 70)

    print(
        f"Books       : {summary['totalBooks']}"
    )

    print(
        f"Categories  : {summary['totalCategories']}"
    )

    print(
        f"Chapters    : {summary['totalChapters']}"
    )

    print(
        f"Words       : {summary['wordsWritten']:,}"
    )

    print(
        f"Completion  : {summary['averageCompletion']}%"
    )

    print(
        f"Output      : {OUTPUT_FILE}"
    )

    print(
        f"Output size : {OUTPUT_FILE.stat().st_size:,} bytes"
    )


if __name__ == "__main__":
    main()
