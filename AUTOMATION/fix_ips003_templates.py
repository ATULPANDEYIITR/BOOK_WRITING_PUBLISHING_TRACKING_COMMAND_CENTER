from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

BOOK_FOLDER = (
    ROOT
    / "BOOKS"
    / "Indian Political Science"
    / "IPS-003_FEDERALISM_AND_INDIAS_UNION_STRUCTURE"
)

CHAPTERS = BOOK_FOLDER / "05_CHAPTERS"

TOPICS = [
    "Meaning and Foundations of Indian Federalism",
    "Constitutional Design of the Union",
    "Distribution of Legislative Powers",
    "Union State Administrative Relations",
    "Financial Relations Between Union and States",
    "Role of the Finance Commission",
    "Fiscal Federalism and Resource Sharing",
    "Inter State Council and Cooperative Federalism",
    "Zonal Councils and Regional Coordination",
    "Emergency Provisions and Federal Relations",
    "Governor and State Constitutional Administration",
    "Role of the President in Federal Affairs",
    "Parliament and State Legislative Powers",
    "Supreme Court and Federal Disputes",
    "Judicial Interpretation of Federalism",
    "Inter State Water Disputes",
    "Language and Federal Accommodation",
    "Regionalism and State Formation",
    "Reorganization of Indian States",
    "Union Territories and Special Administration",
    "Fifth Schedule and Tribal Administration",
    "Sixth Schedule and Autonomous Councils",
    "Special Constitutional Provisions",
    "Asymmetric Federalism in India",
    "Coalition Politics and Federal Change",
    "Single Party Dominance and Federal Relations",
    "Economic Liberalization and Federalism",
    "Goods and Services Tax and Fiscal Federalism",
    "NITI Aayog and Cooperative Governance",
    "Centrally Sponsored Schemes",
    "Local Government and Multilevel Federalism",
    "Urban Governance and Federal Relations",
    "Rural Governance and Decentralization",
    "Disaster Management and Intergovernmental Coordination",
    "Internal Security and Union State Relations",
    "Public Health and Federal Governance",
    "Education Policy and Federal Responsibilities",
    "Agriculture and Intergovernmental Policy",
    "Infrastructure and Regional Development",
    "Natural Resources and Federal Governance",
    "Digital Governance Across Levels",
    "Competitive Federalism and State Policy",
    "Cooperative Federalism in Practice",
    "Challenges to Indian Federalism",
    "Future Directions of Indian Federalism"
]

def create_template(number, topic):
    return f"""# Chapter {number}: {topic}

## Manuscript

### {topic}

This chapter examines {topic.lower()} within the constitutional and institutional framework of Indian federalism. The discussion should connect constitutional principles with historical developments, institutional practice, judicial interpretation, public policy, and contemporary governance.

### Introduction

Introduce the central question of the chapter and explain why {topic.lower()} is important to understanding India's Union structure.

### Constitutional and institutional context

Explain the relevant constitutional provisions, institutions, legal principles, and administrative arrangements.

### Historical development

Trace the major historical developments that shaped {topic.lower()}. Identify important changes in institutions, laws, political practice, and public policy.

### Political dimensions

Examine how political institutions, political parties, elections, regional interests, and Union State relations have affected the subject.

### Economic and fiscal dimensions

Examine relevant financial arrangements, resource allocation, taxation, expenditure responsibilities, development disparities, and economic incentives.

### Administrative dimensions

Analyse the responsibilities of Union and State institutions, implementation mechanisms, coordination systems, and administrative challenges.

### Judicial interpretation

Discuss important constitutional interpretations and relevant Supreme Court decisions where applicable. Distinguish the text of judgments from later academic or political interpretations.

### Case studies

Develop detailed case studies using reliable evidence. Each case study should explain the background, institutions involved, decisions taken, consequences, and broader lessons.

### Comparative perspective

Compare relevant Indian arrangements with other federal or multilevel governance systems where the comparison adds analytical value.

### Critical analysis

Examine competing interpretations, institutional tensions, practical limitations, and areas where constitutional design and administrative practice may differ.

### Contemporary relevance

Explain how the chapter's subject affects present-day governance, public policy, Union State relations, and institutional decision-making.

### Chapter conclusion

Summarize the major evidence and arguments developed in the chapter without introducing unsupported claims.

## References

References will be added after the research stage.

## Research notes

Research sources, constitutional provisions, judgments, data, quotations, case studies, and research questions will be recorded here.

---

**Chapter completion:** 0%
"""

updated = 0

chapter_dirs = sorted(CHAPTERS.glob("CHAPTER_*"))

for index, chapter_dir in enumerate(chapter_dirs, start=1):
    chapter_file = chapter_dir / f"CHAPTER_{index:02d}.md"

    if index > len(TOPICS):
        break

    topic = TOPICS[index - 1]

    chapter_file.write_text(
        create_template(index, topic),
        encoding="utf-8"
    )

    updated += 1

print("=" * 60)
print("IPS-003 CHAPTER TEMPLATES")
print("=" * 60)
print()
print(f"Chapter templates updated: {updated}")
print(f"Book: Federalism and India's Union Structure")
print()
print("IPS-003 now has subject-specific chapter frameworks.")
print("No other books were modified.")