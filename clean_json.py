
import re

file_path = '/Users/mishayaremchuk/swarm-analysis/swarm-data.json'

with open(file_path, 'r') as f:
    content = f.read()

# Remove [cite: 1, 2] patterns
content = re.sub(r'\[cite: [0-9, ]+\]', '', content)

# Remove inline [cite_start]
content = re.sub(r'\[cite_start\]', '', content)

# Remove split [cite_start] blocks causing syntax errors
# Matches: newline + whitespace + [cite_start + newline + whitespace + ]"
# Replaces with: newline + whitespace + "
content = re.sub(r'\n(\s*)\[cite_start\s*\n\s*\]"', r'\n\1"', content)

# Also removing any remaining lines that are just [cite_start if they exist separately
content = re.sub(r'\n\s*\[cite_start\s*\n', '\n', content)

with open(file_path, 'w') as f:
    f.write(content)

print("File cleaned successfully.")
