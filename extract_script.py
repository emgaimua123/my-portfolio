import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if match:
    with open('test_script.js', 'w', encoding='utf-8') as f:
        f.write(match.group(1))
    print("Extracted script to test_script.js")
else:
    print("Could not find <script> tag")
