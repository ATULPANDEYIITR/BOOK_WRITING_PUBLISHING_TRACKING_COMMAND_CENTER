from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parent.parent
TRACKER_FILE = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

def safe_name(text):
    return (
        text.upper()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("?", "")
        .replace('"', "")
        .replace("'", "")
    )

def get_chapter_files(book_folder):
    chapters = book_folder / "05_CHAPTERS"
    return sorted(chapters.glob("CHAPTER_*/CHAPTER_*.md"))

def extract_chapter_topic(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^# Chapter \d+: (.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else path.stem

def create_chapter_research_plan(book, chapter_files):
    book_id = book["Book ID"]
    title = book["Book Title"]
    category = book["Category"]

    book_folder = (
        ROOT
        / "BOOKS"
        / category
        / f"{book_id}_{safe_name(title)}"
    )

    output = book_folder / "08_RESEARCH_NOTES" / "CHAPTER_RESEARCH_PLAN.md"

    lines = [
        "# Chapter Research Plan",
        "",
        f"**Book ID:** {book_id}",
        f"**Book Title:** {title}",
        f"**Category:** {category}",
        f"**Planned Chapters:** {len(chapter_files)}",
        "",
        "This research plan connects every chapter directly to the subject "
        "of the book. Each chapter should be researched independently while "
        "maintaining continuity with the complete manuscript.",
        "",
        "---",
        ""
    ]

    for index, chapter_file in enumerate(chapter_files, start=1):
        topic = extract_chapter_topic(chapter_file)

        lines.extend([
            f"## Chapter {index}: {topic}",
            "",
            "### Research objective",
            "",
            f"Identify reliable evidence and analysis directly related to "
            f"**{topic}** within the broader subject of **{title}**.",
            "",
            "### Questions to investigate",
            "",
            f"- What does {topic.lower()} mean in this context?",
            f"- What historical or intellectual background shaped {topic.lower()}?",
            f"- Which people, institutions, events, or systems are important?",
            f"- What evidence supports the major claims?",
            f"- What competing interpretations exist?",
            f"- What examples or case studies clarify the subject?",
            f"- How does this chapter connect with the rest of the book?",
            "",
            "### Sources to locate",
            "",
            "- Primary sources",
            "- Academic books",
            "- Peer-reviewed research",
            "- Government or institutional publications",
            "- Official datasets",
            "- Reliable historical records",
            "- Expert analysis",
            "",
            "### Evidence to collect",
            "",
            "- Important facts",
            "- Dates and chronology",
            "- Names and institutions",
            "- Quantitative evidence",
            "- Definitions",
            "- Significant quotations",
            "- Case studies",
            "- Contrasting interpretations",
            "",
            "### Research notes",
            "",
            "Add verified research material here.",
            "",
            "### Source evaluation",
            "",
            "Record why each important source is reliable, relevant, "
            "and appropriate for this chapter.",
            "",
            "### Research status",
            "",
            "**Status:** Not Started",
            "",
            "---",
            ""
        ])

    output.write_text("\n".join(lines), encoding="utf-8")

def main():
    with TRACKER_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        books = list(csv.DictReader(file))

    processed = 0
    total_chapters = 0

    for book in books:
        book_folder = (
            ROOT
            / "BOOKS"
            / book["Category"]
            / f"{book['Book ID']}_{safe_name(book['Book Title'])}"
        )

        chapter_files = get_chapter_files(book_folder)

        if not chapter_files:
            continue

        create_chapter_research_plan(book, chapter_files)

        processed += 1
        total_chapters += len(chapter_files)

    print("=" * 60)
    print("CHAPTER RESEARCH PLAN GENERATOR")
    print("=" * 60)
    print()
    print(f"Books processed: {processed}")
    print(f"Chapters connected to research plans: {total_chapters:,}")
    print()
    print("Every chapter now has title-specific research instructions.")
    print("No manuscript content was modified.")

if __name__ == "__main__":
    main()
