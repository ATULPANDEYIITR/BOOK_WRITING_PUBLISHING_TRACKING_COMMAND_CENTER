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

with TRACKER_FILE.open("r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

book = next(b for b in books if b["Book ID"] == "IPS-003")

book_folder = (
    ROOT
    / "BOOKS"
    / book["Category"]
    / f"{book['Book ID']}_{safe_name(book['Book Title'])}"
)

chapter_files = sorted(
    (book_folder / "05_CHAPTERS").glob("CHAPTER_*/CHAPTER_*.md")
)

output = book_folder / "08_RESEARCH_NOTES" / "CHAPTER_RESEARCH_PLAN.md"

lines = [
    "# Chapter Research Plan",
    "",
    f"**Book ID:** {book['Book ID']}",
    f"**Book Title:** {book['Book Title']}",
    f"**Category:** {book['Category']}",
    f"**Planned Chapters:** {len(chapter_files)}",
    "",
    "This research plan connects every chapter directly to the subject "
    "of the book. Each chapter should be researched independently while "
    "maintaining continuity with the complete manuscript.",
    ""
]

for index, chapter_file in enumerate(chapter_files, start=1):
    text = chapter_file.read_text(encoding="utf-8")

    match = re.search(
        r"^# Chapter \d+: (.+)$",
        text,
        re.MULTILINE
    )

    topic = match.group(1).strip() if match else chapter_file.stem

    lines.extend([
        f"## Chapter {index}: {topic}",
        "",
        "### Research objective",
        "",
        f"Identify reliable evidence and analysis directly related to "
        f"**{topic}** within the broader subject of "
        f"**{book['Book Title']}**.",
        "",
        "### Questions to investigate",
        "",
        f"- What does {topic.lower()} mean in the context of Indian federalism?",
        f"- What constitutional principles are connected with {topic.lower()}?",
        "- Which institutions, laws, judgments, events, or political developments are important?",
        "- What evidence supports the major claims?",
        "- What competing interpretations exist?",
        "- What examples or case studies clarify the subject?",
        "- How does this chapter connect with the rest of the book?",
        "",
        "### Sources to locate",
        "",
        "- Constitution of India",
        "- Supreme Court judgments",
        "- Parliamentary and government documents",
        "- Law Commission reports",
        "- Finance Commission reports",
        "- Academic books",
        "- Peer-reviewed research",
        "- Official government datasets",
        "- Reliable historical records",
        "",
        "### Evidence to collect",
        "",
        "- Constitutional provisions",
        "- Important dates",
        "- Judicial decisions",
        "- Institutional developments",
        "- Government policies",
        "- Quantitative evidence",
        "- Important quotations",
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

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines), encoding="utf-8")

print("=" * 60)
print("IPS-003 RESEARCH PLAN")
print("=" * 60)
print()
print(f"Book: {book['Book Title']}")
print(f"Chapters processed: {len(chapter_files)}")
print(f"Created: {output}")
print()
print("IPS-003 research plan created successfully.")
print("No other books were modified.")