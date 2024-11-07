import requests
import json
import os
from urllib.parse import urljoin
from tqdm import tqdm
import time

GITHUB_URL = "https://github.com/FortAwesome/Font-Awesome/blob/6.x/metadata/icons.json"
JSON_FILE = "icons.json"
SWIFT_FILE = "FontAwesomeIconMap.swift"

def get_raw_github_url(github_url):
    """Convert regular GitHub URL to raw content URL"""
    try:
        # Convert the regular GitHub URL to raw content URL
        raw_url = github_url.replace('github.com', 'raw.githubusercontent.com')
        raw_url = raw_url.replace('/blob/', '/')
        print(f"Generated raw URL: {raw_url}")
        return raw_url
    except Exception as e:
        print(f"Error generating raw URL: {str(e)}")
        raise

def download_json_file(raw_url, output_file):
    """Download JSON file from the given URL with progress bar"""
    try:
        print(f"Downloading JSON from: {raw_url}")
        
        # Stream the response to handle large files
        response = requests.get(raw_url, stream=True)
        response.raise_for_status()
        
        # Get total file size if available
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB chunks
        
        # Calculate initial time for speed measurement
        start_time = time.time()
        
        # Open in binary mode for streaming
        with open(output_file, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading",
                miniters=1,
                mininterval=0.05,
                bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]'
            ) as pbar:
                downloaded = 0
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    pbar.update(size)
                    downloaded += size
        
        # Validate JSON content
        with open(output_file, 'r', encoding='utf-8') as f:
            json.load(f)
        
        duration = time.time() - start_time
        speed = downloaded / (1024 * 1024 * duration)  # MB/s
        
        print(f"\nDownload completed:")
        print(f"Total size: {total_size/1024/1024:.2f} MB")
        print(f"Average speed: {speed:.2f} MB/s")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Successfully saved to: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"Downloaded file is not valid JSON: {str(e)}")
        raise

def generate_swift_dictionary(input_json, output_swift):
    """Generate Swift dictionary from JSON file"""
    try:
        print(f"Reading JSON file: {input_json}")
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"JSON loaded successfully. Type of data: {type(data)}")
        print(f"Number of icons found: {len(data)}")
        
        # Show sample of data structure (for debug purposes)
        sample_key = next(iter(data))
        print(f"Sample icon data structure: {data[sample_key]}")
        
        print(f"Generating Swift dictionary file: {output_swift}")
        with open(output_swift, 'w', encoding='utf-8') as f:
            # Add file header
            current_date = time.strftime("%m/%d/%y")
            f.write('//\n')
            f.write(f'//  {output_swift}\n')
            f.write('//\n')
            f.write(f'//  Created by Roger Hirooka on {current_date}\n')
            f.write('//\n\n')
            
            f.write('// Generated from Font Awesome icons.json\n')
            f.write('let fontAwesomeIconMap: [String: String] = [\n')
            
            count = 0
            for icon_name, icon_data in data.items():
                if isinstance(icon_data, dict) and 'unicode' in icon_data:
                    unicode = icon_data['unicode']
                    f.write(f'    "{icon_name}": "\\u{{{unicode}}}",\n')
                    count += 1
            
            f.write(']\n')
            
        print(f"Successfully generated Swift dictionary with {count} icons")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {str(e)}")
        print(f"Error location: line {e.lineno}, column {e.colno}")
        print(f"Error context: {e.doc[max(0, e.pos-40):e.pos+40]}")
        raise
    except Exception as e:
        print(f"Error generating Swift dictionary: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
        raise

def main():
    try:
        # Phase 1: Get raw URL
        print("\n=== Phase 1: Converting to Raw URL ===")
        raw_url = get_raw_github_url(GITHUB_URL)
        
        # Phase 2: Download JSON
        print("\n=== Phase 2: Downloading JSON File ===")
        download_json_file(raw_url, JSON_FILE)
        
        # Phase 3: Generate Swift dictionary
        print("\n=== Phase 3: Generating Swift Dictionary ===")
        generate_swift_dictionary(JSON_FILE, SWIFT_FILE)
        
        print("\n✅ All phases completed successfully!")
        
    except Exception as e:
        print("\n❌ Script failed!")
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
