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

- `config.json`: Set search parameters and output options.
- `scraper.py`: Main script for running the web scraper.
- `utils.py`: Helper functions for data processing.

## Example

```json
{
  "agency": "EPA",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "keywords": ["climate", "emissions"],
  "output_format": "csv"
}
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is for research purposes only. Please respect the [Regulations.gov Terms of Use](https://www.regulations.gov/terms).
