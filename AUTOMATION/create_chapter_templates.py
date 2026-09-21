import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

updated = 0

for book in books:
    category = book["Category"]
    title = book["Book Title"]
    book_id = book["Book ID"]
    chapter_count = int(book["Chapters Planned"])

    book_folder = BOOKS_DIR / category / f"{book_id}_{title.upper().replace(' ', '_')}"
    chapters_folder = book_folder / "05_CHAPTERS"

    if not chapters_folder.exists():
        continue

    target_words = int(book["Target Words"])
    words_per_chapter = target_words // chapter_count

    for number in range(1, chapter_count + 1):
        chapter_folder = chapters_folder / f"CHAPTER_{number:02d}"
        chapter_file = chapter_folder / f"CHAPTER_{number:02d}.md"

        content = f"""# Chapter {number}: [Chapter Title]

**Book:** {title}  
**Book ID:** {book_id}  
**Category:** {category}  
**Chapter:** {number} of {chapter_count}  
**Target Chapter Length:** approximately {words_per_chapter:,} words  
**Writing Status:** Not Started  
**Editing Status:** Not Started  

---

## Chapter Purpose

Define the main purpose of this chapter and explain how it contributes to the overall argument, narrative, or subject of the book.

## Learning or Reading Objectives

- Objective 1
- Objective 2
- Objective 3
- Objective 4

## Introduction

Introduce the central subject of the chapter and establish the context required for the reader.

## Main Section 1

Develop the first major idea of the chapter.

### Supporting Topic

Explain the supporting concept with sufficient depth, evidence, examples, and context.

## Main Section 2

Develop the second major idea of the chapter.

### Supporting Topic

Add detailed explanation, examples, comparisons, data, or historical context where appropriate.

## Main Section 3

Develop the third major idea of the chapter.

### Supporting Topic

Expand the discussion and connect it with the broader subject of the book.

## Evidence and Analysis

Add relevant evidence, research findings, historical records, statistics, primary sources, secondary sources, or analytical discussion.

## Examples and Case Studies

Include appropriate examples or case studies that help the reader understand the chapter.

## Tables and Figures

Add tables, charts, diagrams, or figures when they improve understanding.

## Critical Discussion

Examine important interpretations, limitations, disagreements, competing explanations, or unresolved questions.

## Practical or Applied Perspective

Explain how the ideas in this chapter can be applied or understood in real-world situations where relevant.

## Chapter Summary

Summarize the major ideas developed throughout the chapter.

## Key Terms

- Term 1
- Term 2
- Term 3
- Term 4

## Review Questions

1. Question 1
2. Question 2
3. Question 3
4. Question 4
5. Question 5

## References

Add chapter-specific references here.

## Research Notes

Record important research observations, source notes, quotations, data, and ideas for future revisions.

---

**Chapter completion:** 0%  
"""

        chapter_file.write_text(content, encoding="utf-8")

    updated += 1

print(f"Detailed chapter templates created for {updated} books.")
print("Each chapter now contains a structured writing framework.")
