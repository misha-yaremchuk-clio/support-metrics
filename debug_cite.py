
import re

with open('/Users/mishayaremchuk/swarm-analysis/swarm-data.json', 'r') as f:
    content = f.read()

matches = list(re.finditer(r'\[cite_start\]', content))
print(f"Found {len(matches)} occurrences of [cite_start]")

if matches:
    m = matches[0]
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(f"Context: {repr(content[start:end])}")
