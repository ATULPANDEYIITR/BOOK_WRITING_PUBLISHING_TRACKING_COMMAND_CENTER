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
added_sections = 0
already_present = 0
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

        if "## Manuscript" in content:
            already_present += 1
            continue

        manuscript_section = """
## Manuscript

Write the completed manuscript for this chapter in this section.

The manuscript should be:
- Specific to the book title and chapter topic
- Based on appropriate research
- Detailed and evidence-based
- Written as continuous book-quality prose
- Supported by examples, case studies, data, and references where appropriate
- Free from placeholder text
- Free from repetitive filler
- Structured with clear subsections where necessary

Target chapter length: approximately 4,000 to 7,000 words.

"""

        marker = "\n---\n\n**Chapter completion:**"

        if marker in content:
            content = content.replace(
                marker,
                "\n" + manuscript_section + "---\n\n**Chapter completion:**",
                1
            )
        else:
            content = (
                content.rstrip()
                + "\n\n"
                + manuscript_section
                + "\n---\n\n**Chapter completion:** 0%\n"
            )

        chapter_file.write_text(content, encoding="utf-8")
        added_sections += 1


print()
print("=" * 60)
print("MANUSCRIPT SECTION REPAIR")
print("=" * 60)
print()
print(f"Books processed: {processed_books}")
print(f"Chapter files processed: {processed_chapters:,}")
print(f"Manuscript sections added: {added_sections:,}")
print(f"Already present: {already_present:,}")
print(f"Missing files: {missing_files:,}")
print()
print("Manuscript section repair completed.")