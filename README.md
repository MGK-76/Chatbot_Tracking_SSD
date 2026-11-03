# SSD Chatbot Tracking

## 1. Project Overview

This project investigates third-party tracking associated with the use of AI chatbots. It aims to identify and analyze third-party domains contacted during chatbot interactions.

The project uses Python, Playwright, and publicly available tracker databases to collect browser network requests and identify known tracking domains.

### Objectives
- Collect network traffic generated during AI chatbot usage.
- Identify third-party domains contacted by the chatbot platform.
- Match observed domains against established tracker databases.
- Categorize identified trackers into Advertising, Analytics, and Other.
- Analyze third-party tracking activity associated with AI chatbot platforms.

## 2. Technologies Used

- **Python:** Data processing and automation.
- **Playwright:** Browser automation and network request collection.
- **Chromium:** Browser used for automated testing.
- **Pandas:** Data processing and manipulation.
- **DuckDuckGo Tracker Radar:** Tracker reference database.
- **Disconnect Tracking Protection:** Additional tracker reference database.

## 3. Dataset Sources

The project uses two publicly available tracker databases.

### DuckDuckGo Tracker Radar
Repository: https://github.com/duckduckgo/tracker-radar

The original dataset is processed and normalized into a CSV file containing tracker domain information.

### Disconnect Tracking Protection
Repository: https://github.com/disconnectme/disconnect-tracking-protection

The original dataset is processed into a structured CSV file containing tracker domains.

**Note:** The original repositories are not included in this project. Only the processed datasets required for the analysis are maintained here.

## 4. Tracker Reference Database

The `data/reference_lists/` directory contains:

| File | Description |
|---|---|
| `duckduckgo_domains_normalized.csv` | Normalized DuckDuckGo tracker domains. |
| `disconnect_domains.csv` | Processed Disconnect tracker domains. |
| `combined_tracker_reference.csv` | Combined reference database used for tracker matching. |

The two datasets are combined to create a unified tracker reference database. Duplicate domains are handled during processing.

Trackers are classified into three broad categories:

- Advertising
- Analytics
- Other

## 5. Project Structure

```text
Maus Testing/
│
├── data/
│   ├── reference_lists/
│   │   ├── duckduckgo_domains_normalized.csv
│   │   ├── disconnect_domains.csv
│   │   └── combined_tracker_reference.csv
│   │
│   └── observed_traffic/
│
├── matcher/
│
├── notebooks/
│
├── parser/
│
├── platforms/
│   └── Manus/
│       └── manus_capture.py
│
├── scripts/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 6. System Workflow

The project follows these main stages:

1. **Dataset Preparation:** Obtain DuckDuckGo and Disconnect tracker databases.
2. **Data Normalization:** Process the original datasets into structured CSV files.
3. **Reference Database Creation:** Combine both datasets and handle duplicate domains.
4. **Traffic Collection:** Use Playwright and Chromium to automate browser interactions and capture network requests.
5. **Domain Extraction:** Extract domains from observed network requests.
6. **Tracker Matching:** Compare observed domains against the combined tracker reference database.
7. **Classification:** Identify and categorize matching tracker domains.

## 7. Installation

Clone the repository:

```bash
git clone <https://github.com/MGK-76/Chatbot_Tracking_SSD>
cd "Maus Testing"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright Chromium browser:

```bash
playwright install chromium
```

## 8. Running the Project

The Manus browser capture script is located at:

```text
platforms/Manus/manus_capture.py
```

Run it using:

```bash
python platforms/Manus/manus_capture.py
```

The captured network traffic is stored in:

```text
data/observed_traffic/
```

The tracker matching scripts are located in the `matcher/` directory.

Refer to the respective scripts for their execution commands.

## 9. Repository Management

The repository contains the processed datasets and project scripts required for the research.

The following items are excluded:

- Original DuckDuckGo and Disconnect repositories.
- Python virtual environments.
- Python cache files.
- Temporary development files.
- Browser session profiles and credentials.

This keeps the repository lightweight while maintaining the essential resources needed to reproduce the research workflow.

## 10. Research Scope

This project focuses on identifying third-party tracking domains observed during AI chatbot usage.

A domain matching a known tracker database indicates that it is recognized as a tracking-related domain. It does not, by itself, establish that personal information was collected or transmitted.

The results should therefore be interpreted as observed network activity and tracker-domain matches rather than definitive evidence of data collection.