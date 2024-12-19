import json
from collections import defaultdict

def organize_by_date(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        domain_data = json.load(f)

    # Create a nested defaultdict for year/month/day structure
    date_structure = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(list)
        )
    )

    # Process each domain and its bookmarks
    for domain, bookmarks in domain_data.items():
        for bookmark in bookmarks:
            date_str = bookmark['date']
            if not date_str:  # Skip if no date
                continue
                
            # Split date into components
            year, month, day = date_str.split('-')
            
            # Add bookmark to appropriate date location
            date_structure[year][month][day].append({
                'domain': domain,
                'title': bookmark['title'],
                'url': bookmark['url']
            })

    # Convert defaultdict to regular dict for JSON serialization
    organized_data = {}
    for year in date_structure:
        organized_data[year] = {}
        for month in date_structure[year]:
            organized_data[year][month] = {}
            for day in date_structure[year][month]:
                organized_data[year][month][day] = sorted(
                    date_structure[year][month][day],
                    key=lambda x: x['title']
                )

    # Write the organized data to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(organized_data, f, ensure_ascii=False, indent=2)

def main():
    input_file = 'data/bookmarks_24_12_19_urls_by_domain.json'
    output_file = 'data/bookmarks_by_date.json'
    organize_by_date(input_file, output_file)
    print(f'Bookmarks have been organized by date and saved to {output_file}')

if __name__ == '__main__':
    main()
