import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

with codecs.open('old_block.txt', 'r', 'utf-8') as f:
    old_block = f.read()

# Find start of block to replace
start_idx = content.find("const fxCanvas = document.createElement('canvas');")

# Find end of block to replace
end_idx = content.find("fxLoop();", start_idx)
if end_idx != -1:
    end_idx += len("fxLoop();")

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + old_block.strip() + '\n' + content[end_idx:]
    
    # Also we need to make sure we don't have duplicated mousemove/click from fix_js_events.py!
    # Because fix_js_events.py added a block right before INIT DANDELIONS.
    duplicate_events = """        document.addEventListener('mousemove', (e) => {
            if (window.matchMedia('(hover: none) and (pointer: coarse)').matches) return;
            mouseTrail.push({ x: e.clientX, y: e.clientY, age: 1.0 });
            if (mouseTrail.length > 22) mouseTrail.shift();
        });"""
        
    if duplicate_events in new_content:
        new_content = new_content.replace(duplicate_events, "")
        
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(new_content)
    print("Restored original JS effects!")
else:
    print("Could not find boundaries.")
