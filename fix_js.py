import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

bad_block = """        startScreen.addEventListener('click', () => {
            startScreen.classList.add('hidden');
            vids.intro.play();
            vids.introAmbient.play();
            audios.intro.play().catch(() => {});
            for (let p of mouseTrail) p.age -= 0.055;"""

good_block = """        startScreen.addEventListener('click', () => {
            startScreen.classList.add('hidden');
            vids.intro.play();
            vids.introAmbient.play();
            audios.intro.play().catch(() => {});
        });

        const fxCanvas = document.createElement('canvas');
        fxCanvas.style.cssText = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999;';
        document.body.appendChild(fxCanvas);
        const fxCtx = fxCanvas.getContext('2d');
        function resizeFxCanvas() {
            fxCanvas.width = window.innerWidth;
            fxCanvas.height = window.innerHeight;
        }
        resizeFxCanvas();
        window.addEventListener('resize', resizeFxCanvas);

        let mouseTrail = [];
        let clickBursts = [];
        
        function updateClickBursts() { }

        function updateMouseTrail() {
            for (let p of mouseTrail) p.age -= 0.055;"""

if bad_block in content:
    content = content.replace(bad_block, good_block)
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(content)
    print("Fixed JS logic.")
else:
    print("Could not find bad block.")
