import json
import pandas as pd

def json_to_excel(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        domain_data = json.load(f)

    # Prepare data for DataFrame
    rows = []
    for domain, bookmarks in domain_data.items():
        for bookmark in bookmarks:
            date_str = bookmark['date']
            if not date_str:
                continue
                
            # Split date into components and convert to integers
            year, month, day = map(int, date_str.split('-'))
            
            rows.append({
                'year': year,
                'month': month,
                'day': day,
                'domain': domain,
                'title': bookmark['title'],
                'url': bookmark['url'],
                'date': date_str
            })

    # Create DataFrame and remove duplicates
    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=['url'], keep='first')
    
    # Sort by date and domain
    df = df.sort_values(['year', 'month', 'day', 'domain', 'title'])
    
    # Reorder columns
    columns = ['year', 'month', 'day', 'domain', 'title', 'url', 'date']
    df = df[columns]
    
    # Set numeric dtypes explicitly
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)
    
    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Write main sheet with all bookmarks
        df.to_excel(writer, sheet_name='All Bookmarks', index=False)
        
        # Create sheets for different year ranges
        year_ranges = [
            ('Before 2019', lambda x: x < 2019),
            ('2019-2021', lambda x: x >= 2019 and x <= 2021),
            ('2022', lambda x: x == 2022),
            ('2023', lambda x: x == 2023),
            ('2024', lambda x: x == 2024)
        ]
        
        for sheet_name, year_filter in year_ranges:
            year_data = df[df['year'].apply(year_filter)]
            if not year_data.empty:
                year_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Create pivot table for domain counts by date
        pivot = pd.pivot_table(
            df,
            values='title',
            index=['year', 'month', 'day'],
            columns=['domain'],
            aggfunc='count',
            fill_value=0
        )
        pivot.to_excel(writer, sheet_name='Domain Summary')

def main():
    input_file = 'data/bookmarks_24_12_19_urls_by_domain.json'
    output_file = 'data/bookmarks_summary.xlsx'
    json_to_excel(input_file, output_file)
    print(f'Bookmarks have been exported to Excel: {output_file}')
    
    # Print summary statistics
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    total_before = sum(len(bookmarks) for bookmarks in data.values())
    
    df = pd.read_excel(output_file, sheet_name='All Bookmarks')
    print(f'\nSummary:')
    print(f'Total bookmarks before deduplication: {total_before}')
    print(f'Total unique bookmarks: {len(df)}')
    print(f'Duplicate URLs removed: {total_before - len(df)}')
    print('\nBookmarks by year range:')
    year_counts = df.groupby(
        pd.cut(df['year'].astype(int), 
               bins=[-float('inf'), 2018, 2021, 2022, 2023, 2024],
               labels=['Before 2019', '2019-2021', '2022', '2023', '2024'])
    ).size()
    print(year_counts)

if __name__ == '__main__':
    main()
