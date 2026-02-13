import json
import re
import sys

file_path = 'swarm-data.json'

try:
    with open(file_path, 'r') as f:
        lines = f.readlines()

    print(f"Read {len(lines)} lines.")
    
    # 1. Remove the specific corrupted line
    # "... and so on for the rest of the requested range ..."
    # We filter out lines containing this text
    
    clean_lines = []
    removed_count = 0
    for line in lines:
        if "... and so on for the rest of the requested range" in line:
            clean_lines.append("") # Keep removed line as empty string to preserve line count? Or just remove?
            # Removing is cleaner for JSON structure.
            # But wait, if we remove it, we might join two lines together?
            # The line is usually on its own line.
            # Let's verify context.
            # If line is removed, we have `}` on prev line and `{` on next line.
            # So `}\n{` which needs a comma.
            removed_count += 1
            print(f"Removed corrupted line: {line.strip()}")
        else:
            clean_lines.append(line)
            
    content = "".join(clean_lines)

    # 2. Fix missing commas between objects
    # Regex to find } followed by { with optional whitespace
    pattern = r'}(\s*){'
    fixed_content, count = re.subn(pattern, '},\n  {', content)
    
    print(f"Replaced {count} occurrences of missing commas.")
    
    # 3. Try parsing
    try:
        data = json.loads(fixed_content)
        print("Successfully parsed JSON.")
        
        # Write back formatted
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print("Successfully wrote formatted JSON.")
        
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        # Print context around error
        start = max(0, e.pos - 50)
        end = min(len(fixed_content), e.pos + 50)
        context = fixed_content[start:end]
        print(f"Context around error:\n{context!r}")
        
        line_no = fixed_content.count('\n', 0, e.pos) + 1
        print(f"Line number in fixed content: {line_no}")

except Exception as e:
    print(f"General Error: {e}")
