import codecs
import re

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add forceCleanupTutorial function
force_cleanup_fn = '''        function forceCleanupTutorial() {
            document.querySelectorAll('.tutorial-highlight').forEach(el => el.classList.remove('tutorial-highlight'));
            document.querySelectorAll('.tutorial-parent-elevate').forEach(el => el.classList.remove('tutorial-parent-elevate'));
            document.querySelectorAll('.local-tutorial-overlay').forEach(el => el.remove());
            const globalOverlay = document.getElementById('tutorial-overlay');
            if(globalOverlay) globalOverlay.classList.add('hidden');
        }
        
        function highlightTutorialStep(stepIndex) {'''

content = content.replace('        function highlightTutorialStep(stepIndex) {', force_cleanup_fn, 1)

# 2. Add to paimonClose
close_old = '''        paimonClose.addEventListener('click', () => {
            paimonDialog.classList.add('hidden');
            if (tutorialStep >= 0) {
                // Thot kh?i tutorial gi?a ch?ng
                tutorialStep = -1;
                document.getElementById('tutorial-overlay').classList.add('hidden');
            }
        });'''
close_old_regex = re.compile(r"paimonClose\.addEventListener\('click',\s*\(\)\s*=>\s*\{\s*paimonDialog\.classList\.add\('hidden'\);\s*if\s*\(tutorialStep\s*>=\s*0\)\s*\{[\s\S]*?tutorialStep\s*=\s*-1;[\s\S]*?document\.getElementById\('tutorial-overlay'\)\.classList\.add\('hidden'\);\s*\}\s*\}\);")

close_new = '''        paimonClose.addEventListener('click', () => {
            paimonDialog.classList.add('hidden');
            if (tutorialStep >= 0) {
                tutorialStep = -1;
                forceCleanupTutorial();
            }
        });'''

if close_old_regex.search(content):
    content = close_old_regex.sub(close_new, content, count=1)
    print("paimonClose fixed!")
else:
    print("paimonClose logic not found!")

# 3. Add to tutorial_end
end_old_regex = re.compile(r"(\}\s*else if\s*\(\s*suggestedSection\s*===\s*'tutorial_end'\s*\)\s*\{[\s\S]*?suggestedSection\s*=\s*null;\s*)(\})")
end_new = r"\1forceCleanupTutorial();\n                \2"

if end_old_regex.search(content):
    content = end_old_regex.sub(end_new, content, count=1)
    print("tutorial_end fixed!")
else:
    print("tutorial_end logic not found!")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)
