import json
import codecs

log_path = r"C:\Users\Admin\.gemini\antigravity\brain\c637fe2c-6845-48cc-a134-9a895a7e0fb9\.system_generated\logs\transcript.jsonl"

diff_text = ""
with codecs.open(log_path, 'r', 'utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                pass
            if 'output' in data:
                pass
            # Actually, the output of the tool call is in a step with 'source': 'SYSTEM', 'type': 'TOOL_RESPONSE'
            # Let's just find the response string that contains the massive diff
            if data.get('source') == 'SYSTEM' and data.get('type') == 'TOOL_RESPONSE':
                output = data.get('content', '')
                if 'The following changes were made by the multi_replace_file_content tool' in output and 'font-family: \'HYWenHei-85W\', \'Inter\', sans-serif;' in output:
                    diff_text = output
        except:
            pass

with codecs.open('diff_output.txt', 'w', 'utf-8') as f:
    f.write(diff_text)
print(f"Diff extracted, length: {len(diff_text)}")
