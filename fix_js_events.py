import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

bad_block = """        // "?"? INIT DANDELIONS "?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"""

good_block = """        document.addEventListener('mousemove', (e) => {
            if (window.matchMedia('(hover: none) and (pointer: coarse)').matches) return;
            mouseTrail.push({ x: e.clientX, y: e.clientY, age: 1.0 });
            if (mouseTrail.length > 22) mouseTrail.shift();
        });

        // "?"? INIT DANDELIONS "?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"?"""

if bad_block in content:
    content = content.replace(bad_block, good_block)
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(content)
    print("Fixed JS mouse events.")
else:
    print("Could not find dandelions block.")
