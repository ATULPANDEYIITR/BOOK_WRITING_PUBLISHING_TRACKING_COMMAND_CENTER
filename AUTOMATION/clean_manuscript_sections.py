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


processed_books = 0
processed_chapters = 0
cleaned_sections = 0
already_clean = 0
missing_files = 0


for book in books:
    book_id = book["Book ID"]
    title = book["Book Title"]
    category = book["Category"]
    planned_chapters = int(book["Chapters Planned"])

    book_folder = (
        ROOT
        / "BOOKS"
        / category
        / f"{book_id}_{safe_name(title)}"
    )

    chapters_folder = book_folder / "05_CHAPTERS"

    if not chapters_folder.exists():
        print(f"Missing chapters folder: {book_id}")
        missing_files += planned_chapters
        continue

    processed_books += 1

    for chapter_number in range(1, planned_chapters + 1):
        chapter_name = f"CHAPTER_{chapter_number:02d}"
        chapter_file = (
            chapters_folder
            / chapter_name
            / f"{chapter_name}.md"
        )

        if not chapter_file.exists():
            print(f"Missing chapter file: {book_id} | {chapter_name}")
            missing_files += 1
            continue

        processed_chapters += 1

        content = chapter_file.read_text(encoding="utf-8")

        manuscript_marker = "## Manuscript"

        if manuscript_marker not in content:
            print(f"Missing Manuscript section: {book_id} | {chapter_name}")
            continue

        before, after = content.split(manuscript_marker, 1)

        completion_marker = "---\n\n**Chapter completion:**"

        if completion_marker in after:
            _, completion = after.split(completion_marker, 1)

            new_section = (
                "## Manuscript\n\n"
                "<!-- Write the completed chapter manuscript here. -->\n\n"
                "---\n\n"
                "**Chapter completion:**"
                + completion
            )

            new_content = before.rstrip() + "\n\n" + new_section
        else:
            new_section = (
                "## Manuscript\n\n"
                "<!-- Write the completed chapter manuscript here. -->\n\n"
                "---\n\n"
                "**Chapter completion:** 0%\n"
            )

            new_content = before.rstrip() + "\n\n" + new_section

        if new_content != content:
            chapter_file.write_text(new_content, encoding="utf-8")
            cleaned_sections += 1
        else:
            already_clean += 1


print()
print("=" * 60)
print("MANUSCRIPT SECTION CLEANUP")
print("=" * 60)
print()
print(f"Books processed: {processed_books}")
print(f"Chapter files processed: {processed_chapters:,}")
print(f"Sections cleaned: {cleaned_sections:,}")
print(f"Already clean: {already_clean:,}")
print(f"Missing files: {missing_files:,}")
print()
print("Manuscript sections are now ready for real book writing.")