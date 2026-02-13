
import re
import json
import sys

file_path = '/Users/mishayaremchuk/swarm-analysis/swarm-data.json'

with open(file_path, 'r') as f:
    content = f.read()

# 1. Fix Markdown links [url](url) -> url
# We look for [text](url) where text is usually the url or close to it.
# Taking the part in parentheses is safer for JSON string values.
content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\2', content)

# 2. Remove Markdown code block markers
content = re.sub(r'```json', '', content)
content = re.sub(r'```', '', content)

# 3. Fix missing commas between objects
# Case: } { -> }, {
# We use a lookahead/lookbehind or just grouping to ensure we don't break things.
# Matches: closing brace, optional whitespace, opening brace.
content = re.sub(r'\}\s*\{', '},\n  {', content)

# 4. Handle pasted arrays inside the list
# Case: ... }, [ { ...
# We want to turn this into ... }, { ...
# So we effectively remove the comma-newline-bracket sequence if it exists, or just the bracket.
# But we must be careful of "helpers": [ ... ]
# The pasted array usually starts on a new line or after a closing brace.
# A top level object ends with }, and the next starts with {.
# If we see: }, [ {  it means we have an array insertion.
content = re.sub(r'\}\s*,\s*\[\s*\{', '},\n  {', content) # Case: }, [ { -> }, {
content = re.sub(r'\}\s*\[\s*\{', '},\n  {', content)      # Case: } [ { -> }, {

# 5. Fix double commas or list ends if any
content = re.sub(r'\]\s*\]', ']', content) # Case: List end inside list end

# 6. Ensure only one [ at start and ] at end (heuristic)
# This is Risky if we do it blindly. 
# Let's rely on the regexes above first.

# 7. Remove any "cite" artifacts if they re-appeared (User might have pasted old content)
content = re.sub(r'\[cite: [0-9, ]+\]', '', content)
content = re.sub(r'\[cite_start\]', '', content)
# Handle split or multi-line cite artifacts
content = re.sub(r'\n(\s*)\[cite_start\s*\n\s*\]\"', r'\n\1\"', content)
content = re.sub(r'\n\s*\[cite_start\s*\n', '\n', content)

# 9. Fix backslashes before keys (e.g. \"key":)
content = re.sub(r'\\"(?=\w+":)', '"', content)

# 8. Ensure the file ends with ] if it starts with [

if content.strip().startswith('[') and not content.strip().endswith(']'):
    content = content.rstrip() + ']'


with open(file_path, 'w') as f:
    f.write(content)

print("Text cleaning complete. Attempting to parse JSON...")

try:
    data = json.loads(content)
    print("SUCCESS: JSON is valid.")
except json.JSONDecodeError as e:
    print(f"ERROR: JSON invalid at char {e.pos}: {e.msg}")
    print(f"Context: {content[e.pos-50:e.pos+50]}")
