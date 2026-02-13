
with open('/Users/mishayaremchuk/swarm-analysis/swarm-data.json', 'r') as f:
    content = f.read()

error_pos = 1634804
start = max(0, error_pos - 300)
end = min(len(content), error_pos + 300)

print(f"Context around char {error_pos}:")
print(content[start:end])
