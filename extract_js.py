import json
import codecs

log_path = r"C:\Users\Admin\.gemini\antigravity\brain\c637fe2c-6845-48cc-a134-9a895a7e0fb9\.system_generated\logs\transcript.jsonl"
lines_found = []

try:
    with codecs.open(log_path, 'r', 'utf-8') as f:
        for line in f:
            if 'spawnClickBurst' in line or 'fxCanvas' in line or 'updateMouseTrail' in line:
                lines_found.append(line)
    
    with codecs.open('js_recover.txt', 'w', 'utf-8') as out:
        for l in lines_found[-5:]:
            out.write(l + '\n')
    print("Extracted to js_recover.txt")
except Exception as e:
    print("Error:", e)
