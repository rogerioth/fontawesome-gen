import requests
import json
import os
from urllib.parse import urljoin
from tqdm import tqdm
import time

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
        
        with open(output_file, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,  # Show sizes in KB/MB
                desc="Downloading",
                miniters=1,
                mininterval=0.05,  # Update every 50ms
                bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]'
            ) as pbar:
                downloaded = 0
                for data in response.iter_content(block_size):
                    size = f.write(data)
                    pbar.update(size)
                    downloaded += size
        
        # Calculate download speed
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

def generate_swift_dictionary(input_json, output_swift):
    """Generate Swift dictionary from JSON file"""
    try:
        print(f"Reading JSON file: {input_json}")
        with open(input_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Generating Swift dictionary file: {output_swift}")
        with open(output_swift, 'w', encoding='utf-8') as f:
            f.write('// Generated from Font Awesome icons.json\n')
            f.write('let fontAwesomeIconMap: [String: String] = [\n')
            
            # Ensure we're accessing the correct structure
            icons = data.get('icons', [])
            for icon in icons:
                name = icon.get('id', '')
                unicode = icon.get('unicode', '')
                if name and unicode:
                    f.write(f'    "{name}": "\\u{{{unicode}}}",\n')
            
            f.write(']\n')
        print("Successfully generated Swift dictionary")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {str(e)}")
        raise
    except Exception as e:
        print(f"Error generating Swift dictionary: {str(e)}")
        raise

def main():
    try:
        # Configuration
        github_url = "https://github.com/FortAwesome/Font-Awesome/blob/6.x/metadata/icons.json"
        json_file = "icons.json"
        swift_file = "FontAwesomeIconMap.swift"
        
        # Phase 1: Get raw URL
        print("\n=== Phase 1: Converting to Raw URL ===")
        raw_url = get_raw_github_url(github_url)
        
        # Phase 2: Download JSON
        print("\n=== Phase 2: Downloading JSON File ===")
        download_json_file(raw_url, json_file)
        
        # Phase 3: Generate Swift dictionary
        print("\n=== Phase 3: Generating Swift Dictionary ===")
        generate_swift_dictionary(json_file, swift_file)
        
        print("\n✅ All phases completed successfully!")
        
    except Exception as e:
        print("\n❌ Script failed!")
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
