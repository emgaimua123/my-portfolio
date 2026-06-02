import json
import codecs

log_path = r"C:\Users\Admin\.gemini\antigravity\brain\c637fe2c-6845-48cc-a134-9a895a7e0fb9\.system_generated\logs\transcript.jsonl"
with codecs.open(log_path, 'r', 'utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in data:
                for call in data['tool_calls']:
                    if call['name'] == 'write_to_file' and 'TargetFile' in call['args'] and 'index.html' in call['args']['TargetFile']:
                        content = call['args'].get('CodeContent', '')
                        if 'function animateParticles' in content:
                            print("FOUND animateParticles in transcript!")
                            idx = content.find("function animateParticles")
                            print(content[idx-100:idx+800])
                            break
        except Exception as e:
            pass
