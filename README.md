# FontAwesome Icon Generator

A Python utility that generates a Swift dictionary mapping FontAwesome icon names to their Unicode representations.

## Overview

This tool streamlines the process of using FontAwesome icons in Swift projects by automatically generating a mapping between icon names and their Unicode values. It fetches the latest icon definitions directly from FontAwesome's official repository and creates a Swift-compatible dictionary file.

## Features

- Automatically downloads the latest FontAwesome icon definitions
- Generates a Swift dictionary for easy icon lookup
- Progress bar with download statistics
- Error handling and validation
- Generates type-safe Swift code

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`:
  - requests
  - tqdm

## Installation

1. Clone this repository:

```
bash
git clone https://github.com/yourusername/fontawesome-gen.git
cd fontawesome-gen
```

2. Install dependencies:

```
bash
pip install -r requirements.txt
```

## Usage

Simply run the script:
```bash
python generate.py
```

This will:
1. Download the latest FontAwesome icon definitions
2. Parse the JSON data
3. Generate a Swift file (`FontAwesomeIconMap.swift`) containing the icon mappings

The generated Swift file can be imported into your iOS/macOS project and used like this:

```swift
let iconUnicode = fontAwesomeIconMap["heart"] // Returns the Unicode value for the heart icon
```

## Output

The script generates two files:
- `icons.json`: The raw icon definitions from FontAwesome
- `FontAwesomeIconMap.swift`: The Swift dictionary mapping icon names to Unicode values

## How It Works

1. The script first converts the GitHub URL to a raw content URL
2. Downloads the JSON file
3. Parses the JSON data and extracts icon names and their Unicode values
4. Generates a Swift dictionary with proper formatting and documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- [Font Awesome](https://fontawesome.com/) for providing the icon definitions
- The Python community for the excellent `requests` and `tqdm` libraries

## Note

This tool is meant to be used in conjunction with FontAwesome in your Swift projects. Make sure you comply with FontAwesome's licensing terms when using their icons in your projects.

