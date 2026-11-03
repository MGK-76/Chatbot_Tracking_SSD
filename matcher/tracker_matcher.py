from urllib.parse import urlsplit
import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference_lists"
    / "combined_tracker_reference.csv"
)


def load_reference():
    reference = defaultdict(list)

    with open(REFERENCE_FILE, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            domain = row["domain"].strip().lower()

            if domain:
                reference[domain].append({
                    "category": row["category"],
                    "source": row["source"],
                    "source_categories": row["source_categories"],
                })

    return reference



def match_domain(domain, reference):
    value = domain.strip().lower()

    if "://" not in value:
        value = "//" + value

    host = (urlsplit(value).hostname or "").rstrip(".")

    if not host:
        return {
            "domain": domain,
            "status": "invalid",
            "matches": [],
        }

    labels = host.split(".")
    candidates = [
        ".".join(labels[i:])
        for i in range(len(labels))
    ]

    matches = []

    for candidate in candidates:
        for entry in reference.get(candidate, []):
            matches.append({
                **entry,
                "matched_reference_domain": candidate,
            })

    return {
        "domain": host,
        "status": "matched" if matches else "unmatched",
        "matches": matches,
    }


if __name__ == "__main__":
    reference = load_reference()

    print("Reference domains loaded:", len(reference))

    test_domains = [
    "google-analytics.com",
    "www.google-analytics.com",
    "https://doubleclick.net/path",
    "example.com",
    ]

    for domain in test_domains:
        result = match_domain(domain, reference)
        print(f"\n{result['domain']}: {result['status']}")

        for match in result["matches"]:
            print(f"  Source: {match['source']}")
            print(f"  Category: {match['category']}")
            print(f"  Matched domain: {match['matched_reference_domain']}")