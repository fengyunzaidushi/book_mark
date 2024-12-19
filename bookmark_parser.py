import os
from bs4 import BeautifulSoup
import json

def parse_bookmarks(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, features='lxml')
    
    def process_folder(dl):
        result = []
        if not dl:
            return result
            
        for dt in dl.find_all('dt', recursive=False):
            if dt.h3:  # This is a folder
                folder = {
                    'name': dt.h3.string.strip() if dt.h3.string else '',
                    'type': 'folder',
                    'add_date': dt.h3.get('add_date', ''),
                    'last_modified': dt.h3.get('last_modified', ''),
                    'items': []
                }
                # First process any bookmarks in the current dt
                for a in dt.find_all('a', recursive=False):
                    bookmark = {
                        'type': 'bookmark',
                        'title': a.string.strip() if a.string else '',
                        'url': a.get('href', ''),
                        'add_date': a.get('add_date', ''),
                        'icon': a.get('icon', '')
                    }
                    folder['items'].append(bookmark)
                
                # Then find and process nested dl
                next_dl = dt.find('dl') or dt.find_next_sibling('dl')
                if next_dl:
                    folder['items'].extend(process_folder(next_dl))
                result.append(folder)
            elif dt.a:  # This is a bookmark
                bookmark = {
                    'type': 'bookmark',
                    'title': dt.a.string.strip() if dt.a.string else '',
                    'url': dt.a.get('href', ''),
                    'add_date': dt.a.get('add_date', ''),
                    'icon': dt.a.get('icon', '')
                }
                result.append(bookmark)
        return result

    # Start processing from the root DL
    root_dl = soup.find('dl')
    if root_dl:
        bookmarks_tree = {
            'type': 'root',
            'items': process_folder(root_dl)
        }
    else:
        bookmarks_tree = {'type': 'root', 'items': []}

    return bookmarks_tree

def main():
    input_file = 'data/bookmarks_2024_12_19_1.html'
    output_file = 'data/bookmarks_2024_12_19_1.json'
    
    # Get absolute path for input file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_file)
    output_path = os.path.join(script_dir, output_file)
    
    # Parse bookmarks
    bookmarks = parse_bookmarks(input_path)
    
    # Save to JSON file with pretty printing
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    
    print(f"Bookmarks have been successfully parsed and saved to {output_file}")

if __name__ == "__main__":
    main()
