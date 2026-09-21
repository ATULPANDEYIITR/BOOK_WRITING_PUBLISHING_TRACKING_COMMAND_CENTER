from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BOOKS_DIR = ROOT / "BOOKS"

updated = 0

for chapter_file in BOOKS_DIR.glob("*/*/05_CHAPTERS/CHAPTER_*/CHAPTER_*.md"):
    text = chapter_file.read_text(encoding="utf-8")

    if "## Manuscript" in text:
        continue

    marker = "## Chapter purpose"

    if marker not in text:
        continue

    parts = text.split(marker, 1)

    header = parts[0].rstrip()

    manuscript = """## Manuscript

Write the actual chapter here.

Begin the chapter manuscript below this line.

---

"""

    footer = """
---

## Chapter conclusion

Write the final analytical conclusion for the chapter.

## References

Add chapter-specific references.

## Research notes

Record important sources, evidence, data, quotations, questions, and ideas for future revisions.

---

**Chapter completion:** 0%
"""

    chapter_file.write_text(
        header + "\n\n" + manuscript + footer,
        encoding="utf-8"
    )

    updated += 1

print(f"Chapter files prepared for manuscript writing: {updated}")
print("A dedicated Manuscript section is now available in each chapter.")
