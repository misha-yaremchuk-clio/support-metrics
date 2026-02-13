
import pandas as pd
import json
import re
import sys

# Regex to parse chat lines: [Date, Time] Name: Message
# Example: [12/8/2025, 9:51:42 AM] Service Cloud: Additional context...
CHAT_PATTERN = re.compile(r'^\[(.*?)\] (.*?): (.*)$')

def parse_raw_data(raw_text):
    if not isinstance(raw_text, str):
        return []
    
    messages = []
    lines = raw_text.split('\n')
    
    current_msg = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = CHAT_PATTERN.match(line)
        if match:
            # Save previous message
            if current_msg:
                messages.append(current_msg)
            
            timestamp, author, text = match.groups()
            current_msg = {
                'timestamp': timestamp,
                'author': author,
                'text': text
            }
        else:
            # Continuation of previous message
            if current_msg:
                current_msg['text'] += '\n' + line
            else:
                # Fallback for lines that don't start with timestamp but are at the start
                # or just unparseable lines
                messages.append({
                    'timestamp': '',
                    'author': 'System',
                    'text': line
                })
    
    if current_msg:
        messages.append(current_msg)
        
    return messages

def main():
    try:
        print("Reading Excel file...")
        df = pd.read_excel('consults-raw.xlsx')
        
        # Identify the correct column for raw data (it had a newline in inspection)
        raw_col = [c for c in df.columns if 'Raw' in c and 'Data' in c][0]
        id_col = [c for c in df.columns if 'Consult Number' in c][0]
        
        print(f"Using columns: ID='{id_col}', Data='{raw_col}'")
        
        consults = {}
        
        for _, row in df.iterrows():
            swarm_id = row[id_col]
            if pd.isna(swarm_id):
                continue
                
            raw_text = row[raw_col]
            messages = parse_raw_data(raw_text)
            
            consults[int(swarm_id)] = messages
            
        print(f"Processed {len(consults)} consults.")
        
        with open('consults-data.json', 'w') as f:
            json.dump(consults, f, indent=2)
            
        print("Saved to consults-data.json")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
