import re

def check_missing_commas(filename, start_line=None, end_line=None):
    with open(filename, 'r') as f:
        lines = f.readlines()

    errors = []
    # Regex for a line ending with a value (string, number, boolean, null)
    # This is a simplification but works for formatted JSON
    value_patterns = [
        r'":\s*".*"$',       # String value
        r'":\s*\d+(\.\d+)?$', # Number value
        r'":\s*(true|false|null)$', # Boolean/Null value
        r'\]$',              # End of array
        r'\}$'               # End of object
    ]
    
    # Combined pattern for lines that *should* potentially have a comma if followed by another property/element
    combined_pattern = re.compile('|'.join(value_patterns))

    for i in range(len(lines) - 1):
        line_num = i + 1
        if start_line and line_num < start_line:
            continue
        if end_line and line_num > end_line:
            break
            
        line = lines[i].rstrip()
        next_line = lines[i+1].strip()
        
        # Skip if line already has comma
        if line.endswith(','):
            continue
            
        # Skip if line is just opening brace/bracket
        if line.strip().endswith('{') or line.strip().endswith('['):
            continue

        # Check if line ends with a value/closing brace
        if combined_pattern.search(line):
            # Check if next line implies continuation (starts with quote or opening brace/bracket)
            if next_line.startswith('"') or next_line.startswith('{') or next_line.startswith('['):
                # We have a missing comma!
                errors.append((line_num, line))
                print(f"Missing comma at line {line_num}: {line}")

    return errors

print("Checking relevant range 1874-1928...")
check_missing_commas('swarm-data.json', 1874, 1928)

print("\nChecking specifically for the known error around 97593...")
check_missing_commas('swarm-data.json', 97590, 97600)

print("\nChecking full file for other errors (limit 10)...")
all_errors = check_missing_commas('swarm-data.json')
if len(all_errors) > 10:
    print(f"... and {len(all_errors) - 10} more errors.")
