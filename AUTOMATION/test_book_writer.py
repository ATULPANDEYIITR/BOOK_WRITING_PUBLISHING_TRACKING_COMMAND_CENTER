from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

BOOK_ID = "WH-001"
BOOK_FOLDER = (
    ROOT
    / "BOOKS"
    / "World History"
    / "WH-001_EMPIRES_TRADE_ROUTES_AND_POWER"
)

CHAPTERS = BOOK_FOLDER / "05_CHAPTERS"

def extract_topic(text):
    match = re.search(r"^# Chapter \d+: (.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "Historical Development"

def create_section(topic, number):
    return f"""## Manuscript

### {topic}

This chapter examines {topic.lower()} as part of the broader historical development of empires, trade routes, and political power. The subject cannot be understood through a single event or institution. It developed through interactions among geography, economic exchange, political authority, technological capability, social organization, and cultural contact.

The study of {topic.lower()} begins with context. Historical systems emerge from conditions that already exist, including patterns of settlement, access to resources, transportation possibilities, political organization, and relationships between communities. These conditions influence what forms of exchange and political organization become possible. They also influence which regions become important centers of activity and which regions remain comparatively peripheral.

Trade networks provide an important way to understand these relationships. Commercial exchange connects producers, merchants, consumers, rulers, ports, cities, and transport systems across considerable distances. A trade route is therefore more than a physical path. It is a system through which goods, information, technology, cultural practices, and political influence can move between societies.

Political power is closely connected with these networks. States and empires have historically sought to control strategic territory, important marketplaces, transportation corridors, ports, and sources of valuable resources. Control over such locations can generate taxation revenue, strengthen military capabilities, and increase diplomatic influence. Commercial wealth can therefore contribute to political power, while political stability can make long-distance commerce easier to maintain.

### Historical context

The historical context surrounding {topic.lower()} should be examined through evidence from different periods and regions. Researchers must distinguish between direct evidence and later interpretations. Archaeological discoveries, administrative records, inscriptions, maps, correspondence, travel accounts, commercial documents, and other primary materials can provide different perspectives on historical developments.

Geography is particularly important. Mountains, deserts, rivers, seas, forests, climate patterns, and natural resources affect the movement of people and goods. Routes that appear straightforward on a modern map may have been difficult to travel in earlier periods. Seasonal conditions, political boundaries, security concerns, and available transportation technology could determine whether a route was practical.

### Economic dimensions

Economic exchange creates relationships between regions with different resources and productive capabilities. Agricultural products, metals, textiles, spices, timber, livestock, manufactured goods, and luxury products could travel through interconnected markets. The value of these goods was shaped by scarcity, demand, transportation costs, taxation, risk, and purchasing power.

Merchants and trading communities played an important role in maintaining these systems. They required information about prices, political conditions, security, currencies, credit arrangements, and local customs. Financial practices therefore developed alongside physical trade networks.

### Political dimensions

Political authorities frequently attempted to regulate commercial activity. Taxes, customs duties, licenses, market regulations, protection arrangements, and restrictions on particular goods could influence the movement of wealth. Political institutions also determined how disputes were resolved and how commercial agreements were enforced.

Military power could affect trade in both constructive and destructive ways. Stable political authority could protect routes and reduce uncertainty, while warfare could interrupt transportation, destroy infrastructure, displace communities, and redirect commercial activity toward safer routes.

### Social and cultural exchange

Trade routes also functioned as channels of human interaction. Merchants, travelers, migrants, scholars, religious figures, soldiers, and administrators moved between societies. Their movements could contribute to linguistic exchange, religious transmission, technological diffusion, artistic influence, and changes in social organization.

Cultural exchange was rarely one-directional. Different societies adapted imported ideas to local circumstances. Objects, technologies, beliefs, and practices could therefore change as they moved across geographical and cultural boundaries.

### Technology and infrastructure

Transportation and communication technologies determine the practical limits of long-distance interaction. Ships, roads, bridges, navigation techniques, pack animals, carts, warehouses, ports, and communication systems can all influence the scale and reliability of trade.

Technological improvements can change the balance of power between regions. A society capable of transporting goods more efficiently or maintaining safer routes can gain economic advantages. Such advantages may then reinforce political and military capabilities.

### Evidence and historical interpretation

A rigorous historical analysis requires comparison among different sources. Written records may reflect the interests of rulers, merchants, religious institutions, or other groups. Archaeological evidence can reveal patterns that written records do not mention. Quantitative evidence can help researchers identify changes in population, production, prices, trade volumes, or taxation where reliable records survive.

Historians may therefore reach different interpretations from the same broad body of evidence. Differences in interpretation should be examined carefully rather than treated as simple disagreements. The quality, date, geographical coverage, and purpose of each source affect what conclusions can reasonably be drawn.

### Comparative perspective

Comparing different regions can reveal why similar commercial systems developed differently. Political institutions, geography, technological capabilities, social structures, and resource availability can produce different outcomes even when regions participate in related networks.

Comparative analysis also prevents a single region from being treated as the universal model of historical development. The history of trade and political power is inherently interconnected and requires attention to multiple societies.

### Case study

A detailed case study should be developed around a specific empire, trading center, route, commercial community, political decision, or historical transformation directly relevant to this chapter. The case study should use primary and secondary evidence and demonstrate how broader historical forces operated in a concrete setting.

### Critical analysis

The relationship between commerce and political power should not be treated as automatic. Economic wealth does not always produce political stability, and political control does not always produce prosperous trade. Internal conflict, environmental change, technological disruption, external competition, disease, demographic change, and institutional weakness can alter historical trajectories.

The chapter should therefore examine both continuity and change. It should identify which structures persisted over time and which were transformed by major historical developments.

### Chapter conclusion

{topic} demonstrates that historical systems emerge from interconnected economic, political, geographical, technological, and social forces. Understanding these relationships provides a stronger foundation for examining the subsequent development of empires, commercial networks, and global systems of power.

## References

References will be added after the research stage.

## Research notes

Research sources, evidence, quotations, data, maps, and questions will be recorded here during the research process.

---

**Chapter completion:** 10%
"""

updated = 0

for chapter_file in sorted(CHAPTERS.glob("CHAPTER_*/CHAPTER_*.md")):
    text = chapter_file.read_text(encoding="utf-8")

    if "## Manuscript" not in text:
        continue

    topic = extract_topic(text)
    number_match = re.search(r"CHAPTER_(\d+)", chapter_file.name)
    number = number_match.group(1) if number_match else "?"

    manuscript = create_section(topic, number)

    before = text.split("## Manuscript", 1)[0].rstrip()

    chapter_file.write_text(
        before + "\n\n" + manuscript,
        encoding="utf-8"
    )

    updated += 1

print(f"Test manuscript generated for {updated} chapters.")
print(f"Book: {BOOK_ID}")
print(f"Location: {BOOK_FOLDER}")
print("No other books were modified.")
