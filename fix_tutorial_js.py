import codecs
import re

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

old_js = '''            let targetEl = document.getElementById(step.id) || document.querySelector('.' + step.id);
            if (targetEl) {
                targetEl.classList.add('tutorial-highlight');
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }'''

new_js = '''            let targetEl = document.getElementById(step.id) || document.querySelector('.' + step.id);
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

if old_js in content:
    content = content.replace(old_js, new_js)
    print("JS successfully replaced!")
else:
    print("Could not find the target JS block!")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)
