import json
import re

def find_trailing_commas(file_path):
    errors = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check each line for trailing comma before closing ] or }
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if line_stripped.endswith(',') and (i + 1 < len(lines)):
            next_line = lines[i + 1].strip()
            if next_line.startswith(']') or next_line.startswith('}'):
                errors.append((i + 1, "Trailing comma before closing bracket"))

    return errors


def validate_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print("✅ JSON is valid.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return [(e.lineno, e.msg)]


def main():
    file_path = 'anime_data.JSON'  # change this to your actual JSON path
    print("🔍 Checking for syntax errors in:", file_path)

    # Run validation first to catch top-level JSON errors
    syntax_errors = validate_json(file_path)

    # Check for trailing commas separately
    trailing_comma_errors = find_trailing_commas(file_path)

    all_errors = syntax_errors + trailing_comma_errors

    if all_errors:
        print("\n🛑 Found the following issues:")
        for line, msg in all_errors:
            print(f"Line {line}: {msg}")
    else:
        print("✅ No issues found in the JSON file.")

if __name__ == "__main__":
    main()

