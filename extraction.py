
import argparse
import json
import re
from pathlib import Path


def split_sql_statements(sql_content):
    """Split SQL content into individual statements."""
    return [
        statement.strip()
        for statement in sql_content.split(";")
        if statement.strip()
    ]


def extract_create(statement):
    """Extract CREATE TABLE information."""
    match = re.search(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"]?(\w+)[`\"]?\s*\((.*)\)",
        statement,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    table_name = match.group(1)
    definition = match.group(2)

    columns = []

    for line in definition.splitlines():
        line = line.strip().rstrip(",")

        if not line or re.match(
            r"(PRIMARY|FOREIGN|UNIQUE|CONSTRAINT|KEY|CHECK)\b",
            line,
            re.IGNORECASE
        ):
            continue

        column_match = re.match(
            r"[`\"]?(\w+)[`\"]?\s+(.+)",
            line
        )

        if column_match:
            columns.append({
                "column": column_match.group(1),
                "definition": column_match.group(2).strip()
            })

    return {
        "type": "CREATE TABLE",
        "table": table_name,
        "columns": columns
    }


def extract_insert(statement):
    """Extract INSERT INTO information."""
    match = re.search(
        r"INSERT\s+INTO\s+[`\"]?(\w+)[`\"]?"
        r"\s*(?:\((.*?)\))?\s*VALUES\s*(.*)",
        statement,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    table_name = match.group(1)
    columns_text = match.group(2)
    values_text = match.group(3)

    columns = []

    if columns_text:
        columns = [
            column.strip().strip("`\"")
            for column in columns_text.split(",")
        ]

    values = re.findall(r"\((.*?)\)", values_text, re.DOTALL)

    return {
        "type": "INSERT",
        "table": table_name,
        "columns": columns,
        "values": [value.strip() for value in values]
    }


def extract_select(statement):
    """Extract SELECT information."""
    match = re.search(
        r"SELECT\s+(.*?)\s+FROM\s+(.*?)(?:\s+WHERE\b|\s+GROUP\s+BY\b|"
        r"\s+ORDER\s+BY\b|\s+HAVING\b|\s+LIMIT\b|$)",
        statement,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    selected_columns = [
        column.strip()
        for column in match.group(1).split(",")
    ]

    tables = re.findall(
        r"(?:FROM|JOIN)\s+[`\"]?([\w.]+)[`\"]?",
        statement,
        re.IGNORECASE
    )

    return {
        "type": "SELECT",
        "columns": selected_columns,
        "tables": tables
    }


def extract_update(statement):
    """Extract UPDATE information."""
    match = re.search(
        r"UPDATE\s+[`\"]?(\w+)[`\"]?\s+SET\s+(.*?)(?:\s+WHERE\b|$)",
        statement,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    return {
        "type": "UPDATE",
        "table": match.group(1),
        "set_clause": match.group(2).strip()
    }


def extract_delete(statement):
    """Extract DELETE information."""
    match = re.search(
        r"DELETE\s+FROM\s+[`\"]?(\w+)[`\"]?",
        statement,
        re.IGNORECASE
    )

    if not match:
        return None

    return {
        "type": "DELETE",
        "table": match.group(1)
    }


def extract_drop(statement):
    """Extract DROP TABLE information."""
    match = re.search(
        r"DROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?[`\"]?(\w+)[`\"]?",
        statement,
        re.IGNORECASE
    )

    if not match:
        return None

    return {
        "type": "DROP TABLE",
        "table": match.group(1)
    }


def extract_alter(statement):
    """Extract ALTER TABLE information."""
    match = re.search(
        r"ALTER\s+TABLE\s+[`\"]?(\w+)[`\"]?\s+(.*)",
        statement,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    return {
        "type": "ALTER TABLE",
        "table": match.group(1),
        "operation": match.group(2).strip()
    }


def extract_information(sql_content):
    """Extract information from all SQL statements."""
    extracted_data = []

    extractors = [
        (r"^CREATE\s+TABLE\b", extract_create),
        (r"^INSERT\s+INTO\b", extract_insert),
        (r"^SELECT\b", extract_select),
        (r"^UPDATE\b", extract_update),
        (r"^DELETE\s+FROM\b", extract_delete),
        (r"^DROP\s+TABLE\b", extract_drop),
        (r"^ALTER\s+TABLE\b", extract_alter)
    ]

    for statement in split_sql_statements(sql_content):
        statement = re.sub(r"--[^\n]*", "", statement).strip()

        if not statement:
            continue

        for pattern, extractor in extractors:
            if re.match(pattern, statement, re.IGNORECASE):
                result = extractor(statement)

                if result:
                    extracted_data.append(result)

                break

    return extracted_data


def main():
    parser = argparse.ArgumentParser(
        description="Extract information from SQL files into JSON"
    )

    parser.add_argument(
        "input",
        help="Path to the SQL file"
    )

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.is_file():
        parser.error(f"SQL file not found: {input_path}")

    if input_path.suffix.lower() != ".sql":
        parser.error("Input file must have a .sql extension")

    try:
        sql_content = input_path.read_text(encoding="utf-8")

        extracted_data = extract_information(sql_content)

        output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{input_path.stem}.json"

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(extracted_data, file, indent=4)

        print(f"Total statements extracted: {len(extracted_data)}")
        print(f"JSON file created successfully: {output_path}")

    except UnicodeDecodeError:
        parser.error("Could not read the SQL file as UTF-8")


if __name__ == "__main__":
    main()
