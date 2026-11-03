
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "reference_lists"

DUCKDUCKGO_FILE = DATA_DIR / "duckduckgo_domains_normalized.csv"
DISCONNECT_FILE = DATA_DIR / "disconnect" / "disconnect_domains.csv"
OUTPUT_FILE = DATA_DIR / "combined_tracker_reference.csv"

FIELDS = [
    "domain",
    "category",
    "source",
    "source_categories",
    "service",
]


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    duckduckgo_domains = set()
    disconnect_domains = set()

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()

        # Add DuckDuckGo records
        with open(DUCKDUCKGO_FILE, encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                writer.writerow({
                    "domain": row["domain"],
                    "category": row["category"],
                    "source": "DuckDuckGo",
                    "source_categories": row["source_categories"],
                    "service": "",
                })
                duckduckgo_domains.add(row["domain"])
                total_rows += 1

        # Add Disconnect records
        with open(DISCONNECT_FILE, encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                writer.writerow({
                    "domain": row["domain"],
                    "category": row["category"],
                    "source": "Disconnect",
                    "source_categories": row["source_category"],
                    "service": row["service"],
                })
                disconnect_domains.add(row["domain"])
                total_rows += 1

    overlap = duckduckgo_domains & disconnect_domains

    print("Combined file:", OUTPUT_FILE)
    print("DuckDuckGo domains:", len(duckduckgo_domains))
    print("Disconnect domains:", len(disconnect_domains))
    print("Combined rows:", total_rows)
    print("Domains appearing in both sources:", len(overlap))


if __name__ == "__main__":
    main()
