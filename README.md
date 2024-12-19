# Chrome Bookmark Organizer

A Python-based tool to organize and analyze Chrome bookmarks by domain and creation date.

## Features

- **Domain-based Classification**: Automatically groups bookmarks by their domain (e.g., youtube.com, github.com)
- **Time-based Organization**: Sorts bookmarks by their creation date
- **Flexible Output**: Generates JSON files for easy data manipulation and analysis

## Project Structure

```
book_mark/
├── bookmark_parser.py      # Main parser for Chrome bookmarks HTML
├── url_extractor.py       # Extracts and organizes URLs by domain
├── date_organizer.py      # Organizes bookmarks by year/month/day
├── excel_exporter.py      # Exports bookmarks to Excel format
├── data/                  # Directory for data files (git-ignored)
└── README.md
```

## Usage

1. Export your Chrome bookmarks to HTML:
   - Chrome Menu → Bookmarks → Bookmark Manager
   - Click "..." → Export bookmarks

2. Run the bookmark parser:
```bash
python bookmark_parser.py
```

3. Extract URLs by domain:
```bash
python url_extractor.py
```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "https://example.com": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "date": "2024-12-19"
    }
  ]
}
```

## Requirements

- Python 3.6+
- BeautifulSoup4
- lxml

## Installation

```bash
pip install beautifulsoup4 lxml
```

## License

MIT License
