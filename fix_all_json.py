#!/usr/bin/env python3
"""Comprehensive iterative fix for swarm-data.json syntax errors."""
import re
import json

file_path = '/Users/mishayaremchuk/swarm-analysis/swarm-data.json'

with open(file_path, 'r') as f:
    content = f.read()

print(f"Original: {len(content)} bytes")

# Pass 1: Fix broken array items where closing got merged
# Pattern: "value""    ],"key" -> "value"\n      ],\n      "key"
content = re.sub(
    r'\"(\")\s*\]\s*,\s*\"',
    r'"\n      ],\n      "',
    content
)

# Pass 2: Fix helpers arrays that got flattened
# "Dan Kotak""    ],"step -> "Dan Kotak"\n      ],\n      "step
content = re.sub(
    r'\"\"(\s*)\],\"',
    r'"\n      ],\n      "',
    content
)

# Pass 3: Remove any remaining [cite_start] patterns (multiline)
content = re.sub(r'\[cite_start\s*\n?\s*\]', '', content)
content = re.sub(r'\[cite:\s*[\d,\s]+\]', '', content)

# Pass 4: Fix markdown links [text](url) -> url
content = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', r'\2', content)

# Pass 5: Remove markdown code fences
content = re.sub(r'```json\s*', '', content)
content = re.sub(r'```\s*', '', content)

# Pass 6: Fix missing comma between objects: }\n  { -> },\n  {
content = re.sub(r'\}\s*\n(\s*)\{', r'},\n\1{', content)

# Pass 7: Fix ][ split arrays
content = re.sub(r'\]\s*\[', ',', content)

# Pass 8: Fix }, [ { pattern
content = re.sub(r'\},\s*\[\s*\{', '},\n  {', content)

# Pass 9: Clean up double commas and trailing commas
content = re.sub(r',\s*,', ',', content)
content = re.sub(r',(\s*[\]\}])', r'\1', content)

# Pass 10: Ensure proper wrapper
stripped = content.strip()
if not stripped.startswith('['):
    content = '[\n' + content
if not stripped.endswith(']'):
    content = content.rstrip() + '\n]'

# Iterative fix: try to parse, and on error, attempt targeted fixes
max_attempts = 20
for attempt in range(max_attempts):
    try:
        data = json.loads(content)
        print(f"SUCCESS after {attempt} extra fix(es): {len(data)} items")
        break
    except json.JSONDecodeError as e:
        # Get context around error
        s = max(0, e.pos - 80)
        end_ctx = min(len(content), e.pos + 80)
        ctx = content[s:end_ctx]
        
        # Try common auto-fixes based on error type
        fixed = False
        
        if e.msg == "Expecting ',' delimiter":
            # Insert a comma at the error position if it looks like }\n  {
            before = content[max(0, e.pos-5):e.pos]
            after = content[e.pos:min(len(content), e.pos+5)]
            if after.lstrip().startswith('{') or after.lstrip().startswith('"'):
                # Missing comma - insert one
                content = content[:e.pos] + ',' + content[e.pos:]
                fixed = True
            elif '""' in content[max(0,e.pos-20):e.pos+20]:
                # Double quote issue
                content = content[:e.pos-1] + content[e.pos:]
                fixed = True
                
        elif e.msg == "Expecting value":
            # Trailing comma before ] or }
            before_char = content[e.pos-1:e.pos] if e.pos > 0 else ''
            if content[e.pos:e.pos+1] in (']', '}'):
                # Remove trailing comma
                look_back = content[max(0,e.pos-10):e.pos]
                comma_pos = look_back.rfind(',')
                if comma_pos >= 0:
                    abs_pos = max(0, e.pos-10) + comma_pos
                    content = content[:abs_pos] + content[abs_pos+1:]
                    fixed = True
        
        elif "Unterminated string" in e.msg:
            # Try to close the string at the next newline
            nl = content.find('\n', e.pos)
            if nl > 0:
                content = content[:nl] + '"' + content[nl:]
                fixed = True
        
        if not fixed:
            print(f"Attempt {attempt}: Could not auto-fix: {e.msg} at line {e.lineno}")
            print(f"Context: {repr(content[s:e.pos])} <<ERR>> {repr(content[e.pos:end_ctx])}")
            break
        else:
            print(f"Attempt {attempt}: Fixed '{e.msg}' at line {e.lineno}")
else:
    print(f"Gave up after {max_attempts} attempts")

# Final validation and dedup
try:
    data = json.loads(content)
    
    # Deduplicate by swarm_number
    seen = {}
    for item in data:
        sn = item.get('swarm_number')
        if sn not in seen:
            seen[sn] = item
    
    deduped = len(data) - len(seen)
    if deduped > 0:
        print(f"Removed {deduped} duplicates.")
        data = sorted(seen.values(), key=lambda x: x.get('swarm_number', 0))
    
    content = json.dumps(data, indent=2, ensure_ascii=False)
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"DONE: Saved {len(data)} unique swarm entries, {len(content)} bytes")
    
except json.JSONDecodeError as e:
    print(f"FINAL ERROR: {e.msg} at line {e.lineno}, col {e.colno}")
    with open(file_path, 'w') as f:
        f.write(content)
    print("Saved partially cleaned file.")
