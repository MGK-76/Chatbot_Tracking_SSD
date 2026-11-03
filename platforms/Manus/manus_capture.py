
import csv
import threading
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

# Find the project root: Maus Testing/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from matcher.tracker_matcher import load_reference, match_domain

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "observed_traffic"
    / "manus_requests.csv"
)

START_URL = "https://manus.im"

requests_captured = []
seen_requests = set()


def main():
    reference = load_reference()
    stop_event = threading.Event()

    def capture_request(request):
        host = urlsplit(request.url).hostname

        if not host:
            return

        host = host.lower()

        request_key = (
            request.method,
            request.url,
            request.resource_type,
        )

        if request_key in seen_requests:
            return

        seen_requests.add(request_key)

        result = match_domain(host, reference)
        matches = result["matches"]

        requests_captured.append({
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "domain": host,
            "method": request.method,
            "resource_type": request.resource_type,
            "match_status": result["status"],
            "matched_sources": ";".join(
                sorted({m["source"] for m in matches})
            ),
            "matched_categories": ";".join(
                sorted({m["category"] for m in matches})
            ),
        })

    def wait_for_stop():
        input("\nPress Enter here to stop capturing...\n")
        stop_event.set()

    print("Project root:", PROJECT_ROOT)
    print("Reference domains loaded:", len(reference))
    print("Opening Manus. Log in manually if needed.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.on("request", capture_request)

            page.goto(
                START_URL,
                wait_until="domcontentloaded",
                timeout=60000,
            )

            print("Capture active. Use the browser normally.")
            print("Return to this terminal and press Enter to stop.")

            threading.Thread(
                target=wait_for_stop,
                daemon=True,
            ).start()

            while not stop_event.is_set():
                page.wait_for_timeout(250)

        finally:
            browser.close()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "timestamp_utc",
        "domain",
        "method",
        "resource_type",
        "match_status",
        "matched_sources",
        "matched_categories",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(requests_captured)

    matched = sum(
        row["match_status"] == "matched"
        for row in requests_captured
    )
    unmatched = sum(
        row["match_status"] == "unmatched"
        for row in requests_captured
    )

    print("\nCapture complete.")
    print("Unique request entries:", len(requests_captured))
    print("Matched entries:", matched)
    print("Unmatched entries:", unmatched)
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
