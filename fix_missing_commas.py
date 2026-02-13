import re

def fix_missing_commas(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    fixed_lines = []
    changes = 0
    
    # Regex to detect line with just closing brace/bracket and whitespace
    closing_brace_pattern = re.compile(r'^\s*[\}\]]\s*$')
    # Regex to detect line starting with opening brace/bracket
    opening_brace_pattern = re.compile(r'^\s*[\{\[]')

    for i in range(len(lines)):
        line = lines[i].rstrip('\n')
        
        # If it's the last line, just append
        if i == len(lines) - 1:
            fixed_lines.append(line + '\n')
            continue
            
        next_line = lines[i+1]
        
        # Check if current line is closing brace and next is opening brace
        # And current line doesn't end with comma
        if (closing_brace_pattern.match(line) and 
            opening_brace_pattern.match(next_line) and 
            not line.strip().endswith(',')):
            
            # Watch out for the very last closing brace of the main array ]
            # If next line is empty or EOF, we don't add comma.
            # But here next_line matches { or [, so it's likely a new item.
            
            # Double check we are not inside a string (unlikely with this regex)
            
            print(f"Adding comma at line {i+1}")
            fixed_lines.append(line + ',\n')
            changes += 1
        else:
            fixed_lines.append(line + '\n')

    with open(filename, 'w') as f:
        f.writelines(fixed_lines)
        
    print(f"Fixed {changes} missing commas.")

fix_missing_commas('swarm-data.json')
