import json
import codecs

log_path = r"C:\Users\Admin\.gemini\antigravity\brain\c637fe2c-6845-48cc-a134-9a895a7e0fb9\.system_generated\logs\transcript.jsonl"

diff_text = ""
with codecs.open(log_path, 'r', 'utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('source') == 'SYSTEM' and data.get('type') == 'TOOL_RESPONSE':
                output = data.get('content', '')
                if '[diff_block_start]' in output and '-            font-family' in output:
                    diff_text = output
        except Exception as e:
            pass

with codecs.open('diff_output.txt', 'w', 'utf-8') as f:
    f.write(diff_text)
print(f"Diff extracted, length: {len(diff_text)}")
