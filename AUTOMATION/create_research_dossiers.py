from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent.parent
TRACKER_FILE = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

RESEARCH_SECTIONS = [
    "Research Questions",
    "Historical and Background Context",
    "Key Concepts",
    "Major Scholars and Thinkers",
    "Primary Sources",
    "Secondary Sources",
    "Important Events and Developments",
    "Organizations and Institutions",
    "Important People",
    "Data and Statistics",
    "Case Studies",
    "Competing Interpretations",
    "Critical Issues",
    "Examples",
    "Useful Quotations",
    "Tables and Figures",
    "Source Evaluation",
    "Research Gaps",
    "Chapter Connections",
    "Reference List"
]

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

def create_research_file(book):
    category = book["Category"]
    book_id = book["Book ID"]
    title = book["Book Title"]

    book_folder = (
        ROOT
        / "BOOKS"
        / category
        / f"{book_id}_{safe_name(title)}"
    )

    research_folder = book_folder / "08_RESEARCH_NOTES"
    research_folder.mkdir(parents=True, exist_ok=True)

    file_path = research_folder / "RESEARCH_DOSSIER.md"

    if file_path.exists():
        return False

    sections = [
        f"# Research Dossier",
        "",
        f"**Book ID:** {book_id}",
        f"**Book Title:** {title}",
        f"**Category:** {category}",
        "",
        "## Research Purpose",
        "",
        f"This research dossier supports the development of **{title}**. "
        "Research should remain directly connected to the book's title, "
        "subject, chapter structure, and intended analytical scope.",
        "",
        "Research should prioritize reliable primary and secondary sources. "
        "Important claims should be traceable to evidence. Conflicting "
        "interpretations should be recorded rather than silently removed.",
        ""
    ]

    for section in RESEARCH_SECTIONS:
        sections.extend([
            f"## {section}",
            "",
            "Research material will be added during the research stage.",
            ""
        ])

    sections.extend([
        "## Research Quality Checklist",
        "",
        "- Sources identified",
        "- Sources evaluated",
        "- Important claims supported",
        "- Conflicting interpretations recorded",
        "- Research gaps identified",
        "- Chapter relevance checked",
        "- References recorded",
        "- Publication details captured",
        "",
        "## Research Status",
        "",
        "**Status:** Not Started",
        "",
        "**Last Updated:**",
        ""
    ])

    file_path.write_text("\n".join(sections), encoding="utf-8")
    return True

def main():
    with TRACKER_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        books = list(csv.DictReader(file))

    created = 0
    existing = 0

    for book in books:
        if create_research_file(book):
            created += 1
        else:
            existing += 1

    print("=" * 60)
    print("RESEARCH WORKSPACE GENERATOR")
    print("=" * 60)
    print()
    print(f"Books processed: {len(books)}")
    print(f"Research dossiers created: {created}")
    print(f"Already existing: {existing}")
    print()
    print("Each book now has a dedicated research dossier.")
    print("No manuscript content was modified.")

if __name__ == "__main__":
    main()
