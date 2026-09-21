import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"

def folder_name(title):
    return re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

book = books[0]

book_id = book["Book ID"]
category = book["Category"]
title = book["Book Title"]
chapters = int(book["Chapters Planned"])

book_folder = (
    BOOKS_DIR
    / category
    / f"{book_id}_{folder_name(title)}"
)

plan_file = book_folder / "BOOK_CHAPTER_PLAN.md"

chapter_topics = [
    "Historical Foundations and Early Development",
    "Geographic Conditions and Strategic Landscapes",
    "Early Trade Networks and Commercial Exchange",
    "Maritime Routes and Oceanic Connectivity",
    "Land Routes and Transcontinental Commerce",
    "Markets Cities and Commercial Institutions",
    "Merchants Brokers and Trading Communities",
    "Currency Credit and Financial Exchange",
    "Technology Behind Long Distance Trade",
    "Transportation and Logistics Systems",
    "Agricultural Production and Trade Surpluses",
    "Natural Resources and Economic Power",
    "Ports Marketplaces and Trade Hubs",
    "Empires and Control of Commercial Routes",
    "Taxation Customs and Trade Regulation",
    "Military Power and Economic Expansion",
    "Diplomacy and Commercial Relationships",
    "Religion Culture and Commercial Networks",
    "Migration and Movement Across Regions",
    "Cultural Exchange Along Trade Routes",
    "Language Knowledge and Intellectual Exchange",
    "Trade Diasporas and Transnational Communities",
    "Competition Between Commercial Powers",
    "Economic Conflict and Strategic Rivalry",
    "Colonial Expansion and Commercial Interests",
    "Globalization of Trade Networks",
    "Industrial Transformation and Global Commerce",
    "Changing Technologies and New Trade Routes",
    "Financial Systems and Expanding Markets",
    "Trade Power and Political Transformation",
    "Economic Inequality and Unequal Exchange",
    "Resistance Conflict and Commercial Disruption",
    "Decline Transformation and Replacement of Networks",
    "Legacy of Historical Trade Systems",
    "Modern International Trade Connections",
    "Global Supply Chains and Strategic Dependence",
    "Trade Security and Geopolitical Competition",
    "Future Trade Routes and Emerging Powers",
    "Historical Lessons for the Modern World",
    "Conclusion: Trade Routes Power and Global Transformation"
]

if chapters > len(chapter_topics):
    for number in range(len(chapter_topics) + 1, chapters + 1):
        chapter_topics.append(
            f"Special Study {number}: Trade Power and Historical Transformation"
        )

chapter_topics = chapter_topics[:chapters]

lines = [
    f"# Chapter Plan: {title}",
    "",
    f"**Book ID:** {book_id}",
    f"**Category:** {category}",
    f"**Planned chapters:** {chapters}",
    "",
    "---",
    "",
    "## Planned chapters",
    ""
]

for number, topic in enumerate(chapter_topics, 1):
    chapter_folder = book_folder / "05_CHAPTERS" / f"CHAPTER_{number:02d}"
    chapter_file = chapter_folder / f"CHAPTER_{number:02d}.md"

    chapter_folder.mkdir(parents=True, exist_ok=True)

    lines.extend([
        f"### Chapter {number}: {topic}",
        "",
        f"**File:** `05_CHAPTERS/CHAPTER_{number:02d}/CHAPTER_{number:02d}.md`",
        "",
        f"**Central subject:** {topic}",
        "",
        "**Historical questions:**",
        "- What developments shaped this subject?",
        "- Which people, institutions, states, or communities were involved?",
        "- What economic, political, technological, or cultural effects followed?",
        "",
        "**Research requirements:**",
        "- Primary historical sources",
        "- Academic research",
        "- Relevant quantitative or documentary evidence",
        "- Maps, tables, or figures where appropriate",
        "",
        "**Expected contribution:**",
        f"This chapter examines {topic.lower()} and explains its relationship to the wider development of {title.lower()}.",
        "",
        "---",
        ""
    ])

    content = f"""# Chapter {number}: {topic}

**Book:** {title}  
**Book ID:** {book_id}  
**Category:** {category}  
**Chapter:** {number} of {chapters}  
**Writing Status:** Not Started  
**Editing Status:** Not Started  

---

## Chapter purpose

This chapter examines **{topic.lower()}** as part of the broader historical development explored in *{title}*.

## Central questions

1. What historical developments shaped this subject?
2. Which institutions, communities, states, or individuals influenced its development?
3. How did it affect trade, political authority, society, technology, or culture?
4. What evidence allows historians to understand these developments?
5. What long-term consequences followed?

## Historical context

Explain the conditions that existed before the developments examined in this chapter.

## Major developments

Present the important events, transformations, institutions, and processes connected with this subject.

## People and institutions

Identify important rulers, governments, merchants, communities, organizations, intellectuals, military powers, or other actors relevant to the chapter.

## Economic dimensions

Examine production, trade, taxation, markets, wealth, resources, finance, labour, or commercial activity where relevant.

## Political dimensions

Examine state power, diplomacy, conflict, administration, sovereignty, territorial control, and political consequences where relevant.

## Social and cultural dimensions

Examine migration, religion, language, cultural exchange, social structures, communities, and intellectual developments where relevant.

## Technology and infrastructure

Examine technologies, transportation systems, communication methods, infrastructure, navigation, logistics, or other technological factors where relevant.

## Evidence and historical interpretation

Present evidence from primary and secondary sources and explain major historical interpretations.

## Comparative perspective

Compare relevant regions, societies, institutions, or historical periods where this strengthens the analysis.

## Maps tables and figures

Add appropriate maps, tables, timelines, charts, or figures.

## Case study

Develop at least one detailed historical case study related to this chapter.

## Critical analysis

Discuss competing interpretations, limitations of available evidence, uncertainty, and unresolved historical questions.

## Chapter conclusion

Summarize the major findings and connect them to the next stage of the book.

## References

Add chapter-specific academic and primary-source references.

## Research notes

Record important evidence, source details, quotations, data, and questions for later revision.

---

**Chapter completion:** 0%
"""

    chapter_file.write_text(content, encoding="utf-8")

plan_file.write_text("\n".join(lines), encoding="utf-8")

print(f"Test chapter plan generated for Book {book_id}.")
print(f"Book: {title}")
print(f"Category: {category}")
print(f"Chapters generated: {chapters}")
print(f"Plan file: {plan_file}")
