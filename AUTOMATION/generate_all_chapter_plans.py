import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"
BOOKS_DIR = ROOT / "BOOKS"

def folder_name(title):
    return re.sub(r"[^A-Z0-9]+", "_", title.upper()).strip("_")

TOPIC_PLANS = {
    "World History": [
        "Historical Foundations", "Geographic Conditions", "Early Political Structures",
        "Trade Networks", "Migration and Cultural Exchange", "Economic Systems",
        "Military Power", "Diplomacy and Alliances", "Religion and Society",
        "Technology and Innovation", "Urban Development", "Institutions and Administration",
        "Social Hierarchies", "Resource Competition", "Political Transformation",
        "Conflict and Warfare", "Commercial Expansion", "Intellectual Exchange",
        "Colonial Expansion", "Industrial Transformation", "Nationalism",
        "Revolutionary Change", "Imperial Competition", "Globalization",
        "Economic Transformation", "Social Transformation", "Cultural Transformation",
        "International Relations", "Decline and Transformation", "Historical Legacy",
        "Modern Connections", "Comparative Historical Analysis", "Long Term Consequences",
        "Major Historical Debates", "Research Evidence", "Conclusion"
    ],
    "World Political Science": [
        "Foundations of Political Order", "State Formation", "Political Institutions",
        "Constitutions", "Executive Power", "Legislative Power", "Judicial Institutions",
        "Political Parties", "Elections", "Political Representation", "Public Administration",
        "Bureaucracy", "Political Participation", "Civil Society", "Interest Groups",
        "Political Communication", "Political Economy", "Democratic Governance",
        "Authoritarian Governance", "Political Conflict", "Political Violence",
        "International Relations", "Geopolitics", "Sovereignty", "Global Institutions",
        "International Organizations", "Human Rights", "Political Development",
        "Institutional Change", "Comparative Politics", "Political Theory",
        "Contemporary Challenges", "Technology and Politics", "Future Governance",
        "Research Methods", "Conclusion"
    ],
    "Indian History": [
        "Early Civilizations", "Archaeological Evidence", "Political Formation",
        "Economic Systems", "Trade Networks", "Religion and Society",
        "Urban Development", "Imperial Administration", "Military Organization",
        "Cultural Exchange", "Intellectual Traditions", "Regional Kingdoms",
        "Social Structures", "Agriculture and Resources", "Maritime Connections",
        "Delhi Sultanate", "Mughal Expansion", "Mughal Administration",
        "Maratha Power", "Regional Political Systems", "European Expansion",
        "Company Rule", "Colonial Administration", "Economic Transformation",
        "Social Reform", "Resistance Movements", "Nationalism", "Mass Politics",
        "Constitutional Development", "Independence", "Partition",
        "Post Independence Transformation", "Historical Memory", "Major Debates",
        "Research Evidence", "Conclusion"
    ],
    "Indian Political Science": [
        "Constitutional Foundations", "Constitutional Institutions", "Parliament",
        "Executive Government", "Judiciary", "Federalism", "Centre State Relations",
        "State Governments", "Local Government", "Elections", "Political Parties",
        "Political Representation", "Bureaucracy", "Public Administration",
        "Public Policy", "Political Economy", "Social Movements", "Civil Society",
        "Media and Politics", "Political Communication", "Democratic Institutions",
        "Political Participation", "Governance Reform", "Economic Liberalization",
        "Social Policy", "Rights and Citizenship", "Judicial Governance",
        "Electoral Reform", "Institutional Change", "Contemporary Politics",
        "Technology and Governance", "Digital Democracy", "Political Accountability",
        "Comparative Perspectives", "Research Methods", "Conclusion"
    ],
    "Philosophy": [
        "Origins of Philosophical Thought", "Reason and Rationality", "Knowledge",
        "Truth", "Logic", "Language", "Mind", "Consciousness", "Perception",
        "Reality", "Existence", "Freedom", "Choice", "Moral Responsibility",
        "Ethics", "Justice", "Rights", "Society", "Political Philosophy",
        "Science and Knowledge", "Religion and Philosophy", "Eastern Traditions",
        "Western Traditions", "Metaphysics", "Epistemology", "Aesthetics",
        "Philosophy of Language", "Philosophy of Mind", "Technology and Humanity",
        "Artificial Intelligence", "Human Purpose", "Meaning", "Contemporary Debates",
        "Applied Philosophy", "Research Methods", "Conclusion"
    ],
    "Economics": [
        "Economic Foundations", "Markets", "Supply and Demand", "Incentives",
        "Consumer Behavior", "Production", "Firms", "Competition", "Pricing",
        "Money", "Banking", "Inflation", "Employment", "Monetary Policy",
        "Fiscal Policy", "Public Finance", "Economic Growth", "Development",
        "Institutions", "International Trade", "Globalization", "Exchange Rates",
        "Financial Markets", "Inequality", "Poverty", "Labor Markets",
        "Behavioral Economics", "Environmental Economics", "Digital Economics",
        "Technology and Productivity", "Economic Crises", "Economic Policy",
        "Economic Measurement", "Comparative Economics", "Future Economies",
        "Conclusion"
    ],
    "Finance": [
        "Financial Foundations", "Financial Markets", "Financial Institutions",
        "Money and Banking", "Investment Principles", "Financial Statements",
        "Fundamental Analysis", "Technical Analysis", "Portfolio Construction",
        "Asset Allocation", "Risk Management", "Corporate Finance", "Capital Structure",
        "Cost of Capital", "Business Valuation", "Equity Markets", "Bond Markets",
        "Derivatives", "Options", "Futures", "Hedging", "Financial Modeling",
        "Behavioral Finance", "International Finance", "Foreign Exchange",
        "Financial Technology", "Digital Assets", "Banking Risk", "Financial Regulation",
        "Market Crises", "Capital Allocation", "Investment Strategy",
        "Quantitative Finance", "Financial Data", "Future Financial Systems",
        "Conclusion"
    ],
    "Human Resource Management": [
        "Foundations of Human Resource Management", "Strategic Human Capital",
        "Workforce Planning", "Talent Acquisition", "Recruitment Systems",
        "Employee Selection", "Onboarding", "Training and Development",
        "Performance Management", "Employee Engagement", "Organizational Culture",
        "Leadership Development", "Succession Planning", "Compensation",
        "Rewards", "Benefits", "Employee Relations", "Workplace Communication",
        "Conflict Management", "Diversity and Inclusion", "Workforce Analytics",
        "People Intelligence", "HR Technology", "Digital Workplaces",
        "Remote Work", "Employee Wellbeing", "Organizational Change",
        "HR Strategy", "Global Workforce", "Employment Law", "Ethical HR",
        "Future of Work", "Artificial Intelligence in HR", "People Data",
        "HR Metrics", "Conclusion"
    ],
    "Marketing": [
        "Marketing Foundations", "Consumer Behavior", "Customer Psychology",
        "Market Research", "Segmentation", "Targeting", "Positioning",
        "Brand Strategy", "Brand Identity", "Product Strategy", "Product Marketing",
        "Pricing", "Distribution", "Advertising", "Digital Marketing",
        "Content Marketing", "Search Marketing", "Social Media", "Customer Acquisition",
        "Customer Retention", "Customer Experience", "Marketing Analytics",
        "Customer Intelligence", "Marketing Technology", "Automation",
        "Data Driven Marketing", "Global Marketing", "Cultural Markets",
        "Competitive Strategy", "Market Creation", "Growth Strategy",
        "Marketing Ethics", "Artificial Intelligence in Marketing",
        "Future Marketing Systems", "Research Methods", "Conclusion"
    ],
    "Educational Administration": [
        "Foundations of Educational Administration", "Educational Leadership",
        "Institutional Governance", "Strategic Planning", "Organizational Structure",
        "School Management", "Higher Education Management", "Education Policy",
        "Regulation", "Educational Finance", "Budget Management", "Human Resources",
        "Teacher Workforce", "Student Administration", "Academic Quality",
        "Institutional Performance", "Assessment Systems", "Curriculum Governance",
        "Technology Governance", "Digital Education", "Educational Data",
        "Information Systems", "Stakeholder Management", "Community Engagement",
        "Educational Equity", "Accessibility", "Institutional Change",
        "Leadership Development", "Risk Management", "Crisis Management",
        "Innovation", "Artificial Intelligence in Education", "Future Institutions",
        "Comparative Education", "Research Methods", "Conclusion"
    ],
    "Fiction": [
        "The World Before the Conflict", "The Hidden History", "The First Discovery",
        "The Unexplained Signal", "The Journey Begins", "The First Threat",
        "The Hidden Organization", "The Unexpected Alliance", "The Lost Evidence",
        "The Secret Location", "The Turning Point", "The Dangerous Discovery",
        "The Hidden Motive", "The Betrayal", "The Investigation",
        "The Journey Through the Unknown", "The Second Revelation", "The Rising Conflict",
        "The Hidden Enemy", "The Impossible Choice", "The Escape",
        "The Return", "The Final Investigation", "The Truth Revealed",
        "The Last Confrontation", "The Cost of Discovery", "The New Reality",
        "The Unfinished Mystery", "The Final Journey", "The Legacy",
        "The World Afterward", "The Hidden Future", "The Last Secret",
        "The Final Decision", "The Beginning of Another Story", "Epilogue"
    ],
    "Crime": [
        "Foundations of Criminal Investigation", "Crime Patterns", "Criminal Networks",
        "Organized Crime", "Criminal Markets", "Criminal Intelligence", "Investigation",
        "Evidence", "Crime Scenes", "Forensic Science", "Digital Evidence",
        "Financial Investigation", "Money Trails", "Cybercrime", "Criminal Psychology",
        "Serial Offending", "Violent Crime", "Property Crime", "Drug Markets",
        "Human Trafficking", "Corruption", "Criminal Organizations",
        "Investigative Technology", "Surveillance and Evidence", "Intelligence Analysis",
        "Interagency Cooperation", "International Crime", "Criminal Justice",
        "Prosecution", "Courts and Evidence", "Victimology", "Crime Prevention",
        "Policing Responses", "Emerging Criminal Threats", "Research Methods",
        "Conclusion"
    ],
    "Ethics": [
        "Foundations of Ethics", "Moral Reasoning", "Moral Responsibility",
        "Justice", "Rights", "Human Dignity", "Autonomy", "Consequences",
        "Virtue", "Professional Ethics", "Business Ethics", "Corporate Responsibility",
        "Technology Ethics", "Artificial Intelligence Ethics", "Privacy",
        "Surveillance", "Digital Responsibility", "Research Ethics",
        "Medical Ethics", "Environmental Ethics", "Political Ethics",
        "Institutional Power", "Authority", "Ethical Leadership", "Moral Conflict",
        "Difficult Decisions", "Ethics and Law", "Ethics and Society",
        "Global Ethics", "Cultural Perspectives", "Future Technologies",
        "Human Machine Relationships", "Ethical Governance", "Applied Ethics",
        "Contemporary Debates", "Conclusion"
    ],
    "Environment": [
        "Earth Systems", "Climate Systems", "Human Civilization", "Population",
        "Urbanization", "Pollution", "Air Quality", "Water Security",
        "Agriculture", "Soil Systems", "Forests", "Biodiversity",
        "Ecosystem Services", "Oceans", "Energy Systems", "Renewable Energy",
        "Fossil Fuels", "Climate Change", "Climate Risk", "Environmental Policy",
        "Environmental Governance", "Environmental Economics", "Natural Capital",
        "Sustainable Development", "Circular Economy", "Waste Management",
        "Conservation", "Environmental Justice", "Technology and Environment",
        "Climate Technology", "Cities and Sustainability", "Food Systems",
        "Water Systems", "Future Environmental Challenges", "Research Methods",
        "Conclusion"
    ],
    "Cybersecurity": [
        "Cybersecurity Foundations", "Threat Landscape", "Threat Intelligence",
        "Adversarial Operations", "Network Security", "Application Security",
        "Identity and Access", "Zero Trust", "Cryptography", "Key Management",
        "Security Architecture", "Cloud Security", "Container Security",
        "Endpoint Security", "Security Operations", "Threat Detection",
        "Incident Response", "Digital Forensics", "Malware Analysis",
        "Vulnerability Management", "Penetration Testing", "Secure Development",
        "Software Supply Chains", "Critical Infrastructure", "Industrial Security",
        "Cybercrime", "Cyber Warfare", "National Security", "Security Governance",
        "Risk Management", "Human Factors", "Security Awareness",
        "Artificial Intelligence Security", "Post Quantum Security",
        "Future Cyber Defense", "Conclusion"
    ],
    "Policing": [
        "Foundations of Modern Policing", "Police Organizations", "Police Leadership",
        "Recruitment and Training", "Police Administration", "Criminal Investigation",
        "Police Intelligence", "Evidence Management", "Crime Scene Investigation",
        "Forensics", "Community Policing", "Public Trust", "Police Accountability",
        "Police Technology", "Digital Policing", "Cybercrime Investigation",
        "Data Driven Policing", "Analytical Policing", "Predictive Systems",
        "Interagency Cooperation", "Organized Crime", "Financial Crime",
        "Violent Crime", "Public Order", "Emergency Response", "Crisis Management",
        "Police Ethics", "Human Rights", "Legal Frameworks", "Police Reform",
        "International Policing", "Artificial Intelligence in Policing",
        "Future Police Systems", "Research Methods", "Performance Measurement",
        "Conclusion"
    ],
    "Technology": [
        "Computing Foundations", "System Architecture", "Algorithms",
        "Programming Systems", "Data Structures", "Databases", "Computer Networks",
        "Distributed Systems", "Cloud Architecture", "Containers",
        "Kubernetes", "DevOps", "DevSecOps", "Software Engineering",
        "Software Supply Chains", "Artificial Intelligence", "Machine Learning",
        "Deep Learning", "Generative AI", "Large Language Models",
        "Intelligent Agents", "Retrieval Systems", "AI Security", "Cryptography",
        "Post Quantum Cryptography", "Blockchain", "Internet of Things",
        "Edge Computing", "Real Time Systems", "Data Engineering",
        "Autonomous Systems", "Cyber Defense", "Quantum Computing",
        "Human Machine Intelligence", "Emerging Computing", "Future Technology",
        "Conclusion"
    ]
}

with open(TRACKER, "r", encoding="utf-8-sig", newline="") as file:
    books = list(csv.DictReader(file))

processed = 0

for book in books:
    book_id = book["Book ID"]
    category = book["Category"]
    title = book["Book Title"]
    chapters = int(book["Chapters Planned"])

    book_folder = (
        BOOKS_DIR
        / category
        / f"{book_id}_{folder_name(title)}"
    )

    chapters_folder = book_folder / "05_CHAPTERS"
    plan_file = book_folder / "BOOK_CHAPTER_PLAN.md"

    topics = TOPIC_PLANS.get(category, TOPIC_PLANS["Technology"])

    if chapters <= len(topics):
        selected_topics = topics[:chapters]
    else:
        selected_topics = topics[:]

        while len(selected_topics) < chapters:
            selected_topics.append(
                f"Specialized Study {len(selected_topics) + 1}"
            )

    plan_lines = [
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

    for number, topic in enumerate(selected_topics, 1):
        chapter_folder = chapters_folder / f"CHAPTER_{number:02d}"
        chapter_folder.mkdir(parents=True, exist_ok=True)

        chapter_file = chapter_folder / f"CHAPTER_{number:02d}.md"

        plan_lines.extend([
            f"### Chapter {number}: {topic}",
            "",
            f"**File:** `05_CHAPTERS/CHAPTER_{number:02d}/CHAPTER_{number:02d}.md`",
            "",
            f"**Central subject:** {topic}",
            "",
            "**Research requirements:**",
            "- Academic and authoritative sources",
            "- Primary sources where applicable",
            "- Relevant data, examples, or case studies",
            "- Tables, figures, timelines, or diagrams where useful",
            "",
            "**Expected contribution:**",
            f"Explain how {topic.lower()} contributes to the central subject of *{title}*.",
            "",
            "---",
            ""
        ])

        if not chapter_file.exists() or book_id != "WH-001":
            content = f"""# Chapter {number}: {topic}

**Book:** {title}  
**Book ID:** {book_id}  
**Category:** {category}  
**Chapter:** {number} of {chapters}  
**Writing Status:** Not Started  
**Editing Status:** Not Started  

---

## Chapter purpose

This chapter examines **{topic.lower()}** within the broader subject of *{title}*.

## Central questions

1. What are the foundations of this subject?
2. What major developments shaped it?
3. Which people, institutions, systems, or forces influenced it?
4. What evidence supports the major explanations?
5. What consequences resulted from these developments?

## Introduction

Introduce the chapter subject and explain its importance to the overall book.

## Historical or conceptual context

Establish the background required to understand the subject.

## Major concepts and developments

Explain the principal ideas, events, systems, institutions, technologies, or processes connected with the chapter.

## Evidence and analysis

Present authoritative evidence and develop a detailed analytical discussion.

## Examples and case studies

Include relevant examples and detailed case studies.

## Comparative perspective

Compare relevant systems, periods, regions, institutions, theories, or approaches where appropriate.

## Tables and figures

Add useful tables, charts, timelines, maps, diagrams, or other visual material.

## Critical discussion

Discuss competing interpretations, limitations, uncertainties, and unresolved questions.

## Practical or applied perspective

Explain real-world implications where appropriate.

## Chapter conclusion

Summarize the major findings and connect the chapter with the wider argument of the book.

## References

Add chapter-specific references.

## Research notes

Record important sources, evidence, data, quotations, questions, and ideas for future revisions.

---

**Chapter completion:** 0%
"""
            chapter_file.write_text(content, encoding="utf-8")

    plan_file.write_text("\n".join(plan_lines), encoding="utf-8")
    processed += 1

print(f"Subject-specific chapter plans generated for {processed} books.")
print("All chapter plans now use category-specific subjects.")
