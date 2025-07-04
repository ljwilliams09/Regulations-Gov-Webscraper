# Regulations-Gov-Webscraper

A Python-based web scraper for collecting data from [Regulations.gov](https://www.regulations.gov/). This tool is designed to automate the extraction of regulatory documents, comments, and metadata for research and analysis purposes.

## Features

- Scrapes regulatory dockets, documents, and public comments.
- Supports filtering by agency, date, and keyword.
- Outputs data in CSV or JSON format.
- Handles pagination and rate limiting.
- Modular and extensible codebase.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Regulations-Gov-Webscraper.git
   cd Regulations-Gov-Webscraper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Update `config.json` with your desired parameters (e.g., agency, date range, keywords).

Run the scraper:

```bash
python scraper.py
```

Output files will be saved in the `output/` directory.

## Configuration

### Comments

- `config.json`: Parameters for comments.py and logger_config.py, year and api_key
- `comments.py`: Retrieves comments metadata on the regulations.gov API posted during the parameter year
- `logger_config.py`: Initializes logger for `comments.py`.
- `run.pbs`: Portable batch script for running on a server; in this case on Colgate's supercomputer

### Dockets

- `dockets.py`: Retrieves all docket metadata from the regulations.gov API.
- `logger_dockets.py`: Initializes logger for `dockets.py`.
- `run.pbs`: Portable batch script for running on a server; in this case on Colgate's supercomputer.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

## Disclaimer

This tool is for research purposes only. Please respect the [Regulations.gov Terms of Use](https://www.regulations.gov/terms).
