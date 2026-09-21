import csv
import random
from pathlib import Path

tracker = Path("BOOK_TRACKER/BOOK_MASTER_TRACKER.csv")

with open(tracker, "r", encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))

random.seed(180)

for row in rows:
    row["Chapters Planned"] = str(random.randint(27, 45))

with open(tracker, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Chapter counts updated for all 180 books.")
print(f"Minimum chapters assigned: {min(int(row['Chapters Planned']) for row in rows)}")
print(f"Maximum chapters assigned: {max(int(row['Chapters Planned']) for row in rows)}")
