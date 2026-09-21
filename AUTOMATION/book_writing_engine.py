from pathlib import Path
import json
import csv

ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = ROOT / "AUTOMATION" / "WRITING_ENGINE_CONFIG.json"
TRACKER_FILE = ROOT / "BOOK_TRACKER" / "BOOK_MASTER_TRACKER.csv"

def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def load_books():
    with TRACKER_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))

def main():
    config = load_config()
    books = load_books()

    print("=" * 60)
    print("BOOK WRITING ENGINE")
    print("=" * 60)
    print()
    print(f"Books loaded: {len(books)}")
    print(f"Target words per book: {config['target_words_per_book']:,}")
    print(f"Minimum pages: {config['minimum_pages']}")
    print(
        f"Chapter range: "
        f"{config['minimum_chapters']} - "
        f"{config['maximum_chapters']}"
    )
    print(
        f"Words per chapter: "
        f"{config['target_words_per_chapter']['minimum']:,} - "
        f"{config['target_words_per_chapter']['maximum']:,}"
    )
    print()

    required = [
        "title_specific_content",
        "category_specific_content",
        "research_based",
        "historical_context",
        "critical_analysis",
        "case_studies",
        "examples",
        "tables",
        "references",
        "chapter_conclusion",
        "avoid_repetition",
        "avoid_placeholder_text"
    ]

    print("Writing requirements:")
    for item in required:
        status = config["writing_requirements"].get(item, False)
        print(f"  {item}: {'ON' if status else 'OFF'}")

    print()
    print("Workflow:")
    for number, step in enumerate(config["workflow"], start=1):
        print(f"  {number}. {step}")

    print()
    print("Book sample:")
    for book in books[:3]:
        print(
            f"  {book['Book ID']} | "
            f"{book['Category']} | "
            f"{book['Book Title']} | "
            f"{book['Chapters Planned']} chapters"
        )

    print()
    print("Writing engine configuration loaded successfully.")
    print("No book content was modified.")

if __name__ == "__main__":
    main()
