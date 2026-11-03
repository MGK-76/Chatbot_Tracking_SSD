
import json
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = Path(
    r"D:\books\SSD Project_Local\disconnect-tracking-protection-master\services.json"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "reference_lists" / "disconnect"
OUTPUT_FILE = OUTPUT_DIR / "disconnect_domains.csv"

CATEGORY_MAP = {
    "Advertising": "advertising",
    "Analytics": "analytics",
}


def main():
    with open(INPUT_FILE, "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    domains = {}

    for category, services in data["categories"].items():
        mapped_category = CATEGORY_MAP.get(category, "other")

        for service in services:
            for service_name, urls in service.items():
                for domain_list in urls.values():
                    for domain in domain_list:
                        domain = domain.lower().strip().rstrip(".")

                        if not domain:
                            continue

                        if domain not in domains:
                            domains[domain] = {
                                "category": mapped_category,
                                "source_category": category,
                                "service": service_name,
                            }
                        elif domains[domain]["category"] != mapped_category:
                            domains[domain]["category"] = "other"
                            domains[domain]["source_category"] = (
                                "conflicting categories"
                            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "domain",
                "category",
                "source_category",
                "service",
            ],
        )
        writer.writeheader()

        for domain, details in sorted(domains.items()):
            writer.writerow({
                "domain": domain,
                **details,
            })

    print("Unique domains:", len(domains))
    print("Output file:", OUTPUT_FILE)

    counts = {}
    for details in domains.values():
        category = details["category"]
        counts[category] = counts.get(category, 0) + 1

    print("\nCategory counts:")
    for category, count in sorted(counts.items()):
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()
