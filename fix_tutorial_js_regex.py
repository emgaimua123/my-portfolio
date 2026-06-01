import codecs
import re

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

pattern = re.compile(
    r'let targetEl = document\.getElementById\(step\.id\) \|\| document\.querySelector\(\'\.\' \+ step\.id\);\s*if \(targetEl\) \{\s*targetEl\.classList\.add\(\'tutorial-highlight\'\);\s*targetEl\.scrollIntoView\(\{ behavior: \'smooth\', block: \'center\' \}\);\s*\}'
)

replacement = '''let targetEl = document.getElementById(step.id) || document.querySelector('.' + step.id);
            if (targetEl) {
                targetEl.classList.add('tutorial-highlight');
                
                let parent = targetEl.parentElement;
                while(parent && parent !== document.body) {
                    const style = window.getComputedStyle(parent);
                    if (style.zIndex !== 'auto' && style.position !== 'static') {
                        parent.classList.add('tutorial-parent-elevate');
                    }
                    parent = parent.parentElement;
                }
                
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }'''

if pattern.search(content):
    content = pattern.sub(replacement, content)
    print("JS successfully replaced using regex!")
else:
    print("Could not find the target JS block with regex!")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)
