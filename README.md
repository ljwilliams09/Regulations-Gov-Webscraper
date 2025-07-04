# Regulations-Gov-Webscraper

A Python-based web-scraper and evaluator for collecting data from [Regulations.gov](https://www.regulations.gov/). This tool is designed to automate the extraction of regulatory documents, comments, and metadata for research and analysis purposes.

## Features

- Scrapes regulatory dockets, documents, and public comments.
- Supports filtering by year.
- Outputs data in CSV.
- Affiliation evaluation for comments
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

Output files will be saved in the directory of origin.

## Guide

### Comments

- `config.json`: Parameters for comments.py and logger_config.py, year and api_key
- `comments.py`: Main script; retrieves comments metadata on the regulations.gov API posted during the parameter year
- `logger_config.py`: Initializes logger for `comments.py`.
- `run.pbs`: Portable batch script for running on a server; in this case on Colgate's supercomputer

### Dockets

- `dockets.py`: Main script; retrieves all docket metadata from the regulations.gov API.
- `logger_dockets.py`: Initializes logger for `dockets.py`.
- `run.pbs`: Portable batch script for running on a server; in this case on Colgate's supercomputer.

### Affiliations

- `config.json`: Parameters for `attachments.py` and `affiliations.py` to specifiy openai models to be used.
- `logger_affil.py`: Initializes logger for `affilations.py`.
- `helpers.py`: Helper functions for `affiliations.py` and `comments.py`.
- `attachments.py`: Handles attached files (if present) and evaluates the affiliation and provides a summary.
- `affiliations.py`: Takes all comment metadata and attachment summary to det

### Testing and Debugging

- Random test files and markdown files used to navigate the regulations.gov API and determine accuracy.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

## Additional Info

For any questions on the regulations.gov API, visit https://open.gsa.gov/api/regulationsgov/.
