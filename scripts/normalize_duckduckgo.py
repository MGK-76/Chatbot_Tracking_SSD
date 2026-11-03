
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = Path(
    r"D:\books\SSD Project_Local\DuckDuckGoTracker\tracker-radar"
    r"\domains\US\duckduckgo_domains.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference_lists"
    / "duckduckgo_domains_normalized.csv"
)

ADVERTISING = {
    "Advertising",
    "Ad Motivated Tracking",
}

ANALYTICS = {
    "Analytics",
    "Third-Party Analytics Marketing",
    "Audience Measurement",
    "Session Replay",
    "Action Pixels",
}

def classify(categories):
    labels = {
        label.strip()
        for label in categories.split(";")
        if label.strip()
    }

    if not labels:
        return "unknown"

    if labels & ADVERTISING and labels & ANALYTICS:
        return "mixed"

    if labels & ADVERTISING:
        return "advertising"

    if labels & ANALYTICS:
        return "analytics"

    return "other"


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)

        with open(
            OUTPUT_FILE, "w", encoding="utf-8", newline=""
        ) as destination:
            fields = [
                "domain",
                "category",
                "source_categories",
                "source",
            ]
            writer = csv.DictWriter(
                destination, fieldnames=fields
            )
            writer.writeheader()

            counts = {}

            for row in reader:
                category = classify(row["categories"])
                counts[category] = counts.get(category, 0) + 1

                writer.writerow({
                    "domain": row["domain"],
                    "category": category,
                    "source_categories": row["categories"],
                    "source": "DuckDuckGo",
                })

    print("Output:", OUTPUT_FILE)
    print("Category counts:")
    for category, count in sorted(counts.items()):
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()
