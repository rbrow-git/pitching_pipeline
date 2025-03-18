# MLB Pitching Pipeline

A tool for scraping MLB starting pitcher game logs from Baseball Reference.

## Description

This project provides a parallel scraping solution to extract game logs for MLB starting pitchers from [Baseball Reference](https://www.baseball-reference.com/). It collects detailed statistics for each starting pitcher's appearances from 2020 to 2024.

## Features

- Parallel processing for efficient data collection
- Robust error handling for network issues 
- Random delays to respect server load
- Automatically cleans up Selenium processes
- Saves data to CSV format

## Installation

### Prerequisites

- Python 3.9 or higher
- Chrome browser installed

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pitching_pipeline.git
cd pitching_pipeline
```

2. Install dependencies using uv (recommended):
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add pandas selenium beautifulsoup4 webdriver-manager tqdm lxml
```

## Usage

The main script can be run directly from the notebook or converted to a Python script:

```bash
uv run python scrape_starting_pitchers_logs.py
```

The script will:
1. Load pitcher IDs from `Starting_Pitchers_IDs.csv`
2. Scrape game logs for each pitcher for the seasons 2020-2024
3. Save the combined data to `MLB_Pitcher_Game_Logs.csv`

## Data Description

The output CSV contains detailed game logs with the following information:
- Standard pitching statistics (IP, H, R, ER, BB, SO, etc.)
- Game metadata (date, opponent, result)
- Pitcher identification and season

## Troubleshooting

If you encounter ChromeDriver issues:
- Ensure Chrome is up to date
- Check that webdriver-manager is installed correctly
- Run the cleanup_selenium() function to clear lingering processes

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
