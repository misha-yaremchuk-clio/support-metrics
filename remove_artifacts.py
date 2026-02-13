
import re
import json

file_path = '/Users/mishayaremchuk/swarm-analysis/swarm-data.json'

with open(file_path, 'r') as f:
    content = f.read()

print(f"Original length: {len(content)}")

# Count occurrences before
cite_start_count = len(re.findall(r'\[cite_start\]', content))
slash_key_count = len(re.findall(r'\\"(?=\w+":)', content))
print(f"[cite_start] count: {cite_start_count}")
print(f"Backslash before keys count: {slash_key_count}")

# Remove [cite_start]
content, n_subs = re.subn(r'\[cite_start\]', '', content)
print(f"Removed {n_subs} [cite_start] tags")

# Remove [cite_start] split across lines (if any)
content, n_subs_split = re.subn(r'\n(\s*)\[cite_start\s*\n\s*\]\"', r'\n\1\"', content)
print(f"Removed {n_subs_split} split [cite_start] tags")

# Remove backslashes before keys
content, n_subs_slash = re.subn(r'\\"(?=\w+":)', '"', content)
print(f"Fixed {n_subs_slash} backslashes before keys")

# Save
with open(file_path, 'w') as f:
    f.write(content)

print(f"New length: {len(content)}")

# Validate
try:
    json.loads(content)
    print("SUCCESS: JSON is valid.")
except json.JSONDecodeError as e:
    print(f"ERROR: JSON invalid at char {e.pos}: {e.msg}")
    context_start = max(0, e.pos - 50)
    context_end = min(len(content), e.pos + 50)
    print(f"Context: {repr(content[context_start:context_end])}")
