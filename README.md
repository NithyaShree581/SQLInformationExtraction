# SQL Information Extraction

A Python-based SQL Information Extraction tool that reads `.sql` files, extracts information using regular expressions, and generates structured JSON output.

## Features

- Accepts SQL files through command-line arguments.
- Extracts CREATE TABLE statements and column definitions.
- Extracts INSERT INTO statements and values.
- Extracts SELECT statements, columns, and tables.
- Extracts UPDATE and DELETE statements.
- Extracts ALTER TABLE and DROP TABLE statements.
- Generates corresponding JSON output files.

## Technologies Used

- Python
- Regular Expressions (`re`)
- JSON
- Argparse
- Pathlib

## Project Structure

```text
SQLInformationExtraction/
├── input/
│   └── sample.sql
├── output/
│   └── sample.json
├── extraction.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

```bash
git clone https://github.com/NithyaShree581/SQLInformationExtraction.git
cd SQLInformationExtraction

python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Usage

Place your SQL file inside the `input` directory.

```powershell
python extraction.py "input/sample.sql"
```

The extracted information is saved as:

```text
output/sample.json
```

## Note

This project uses regular expressions for SQL information extraction. It is intended for educational use and does not support every possible SQL syntax or complex SQL structure.