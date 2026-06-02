import codecs

def fix_code():
    with codecs.open('index.html', 'r', 'utf-8') as f:
        content = f.read()

    # 1. Fix cursor in .start-screen
    content = content.replace("cursor: pointer;", "cursor: url('content/cursor/genshin_link.cur'), pointer;")
    
    # 2. Add intro-prompt CSS
    pulse_css = """        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }"""
    
    if "id=\"intro-prompt\"" not in content:
        intro_css = """
        /* Dòng chữ "CLICK TO ENTER" */
        #intro-prompt {
            position: absolute;
            bottom: 10%;
            color: white;
            font-size: 1rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            opacity: 0;
            transition: opacity 1s;
            z-index: 40;
            text-shadow: 0 2px 12px rgba(0,0,0,0.9);
            pointer-events: none;
            animation: pulse 2s infinite;
        }
        """
        
        # Insert CSS
        css_insert_point = content.find("/* =====================================================")
        content = content[:css_insert_point] + intro_css + pulse_css + '\n' + content[css_insert_point:]
        
        # Insert HTML
        html_target = """            <video id="intro-vid" class="main-vid" playsinline muted>
                <source src="intro/intro.mp4" type="video/mp4">
            </video>"""
        html_replacement = html_target + '\n            <div id="intro-prompt">CLICK TO ENTER</div>'
        content = content.replace(html_target, html_replacement)

    # 3. Add intro-prompt to JS ended event
    ended_target = """        vids.intro.addEventListener('ended', () => {
             isIntroFinished = true;
             vids.introAmbient.loop = true;
             scenes.intro.style.cursor = "url('cursor/genshin_link.cur'), pointer";
             introWrapper.classList.add('frozen');
             vignette.classList.add('visible');
             particlesCanvas.classList.add('visible');
             particlesRunning = true;
             requestAnimationFrame(animateParticles);
        });"""
        
    ended_replacement = """        vids.intro.addEventListener('ended', () => {
             isIntroFinished = true;
             vids.introAmbient.loop = true;
             scenes.intro.style.cursor = "url('content/cursor/genshin_link.cur'), pointer";
             introWrapper.classList.add('frozen');
             vignette.classList.add('visible');
             particlesCanvas.classList.add('visible');
             particlesRunning = true;
             requestAnimationFrame(animateParticles);
             
             const introPrompt = document.getElementById('intro-prompt');
             if (introPrompt) introPrompt.style.opacity = '1';
        });"""
    content = content.replace(ended_target, ended_replacement)

    # Note: also fix "url('cursor/genshin_link.cur')" to "url('content/cursor/genshin_link.cur')" in JS
    content = content.replace("scenes.door.style.cursor = \"url('cursor/genshin_link.cur'), pointer\";", 
                              "scenes.door.style.cursor = \"url('content/cursor/genshin_link.cur'), pointer\";")

    # 4. Auto transition door -> main
    door_target = """        // ── VIDEO CỬA KẾT THÚC -> ĐỢI CLICK ──
        vids.door.addEventListener('ended', () => {
            isDoorFinished = true;
            vids.doorAmbient.loop = true;
            scenes.door.style.cursor = "url('content/cursor/genshin_link.cur'), pointer";
        });

        scenes.door.addEventListener('click', () => {
            if (!isDoorFinished) return;

            // Tắt hiệu ứng
            particlesRunning = false;
            vignette.classList.remove('visible');
            particlesCanvas.classList.remove('visible');
            doorWrapper.classList.remove('frozen');

            whiteFlash.classList.add('active');

            setTimeout(() => {
                switchScene(scenes.door, scenes.main);
                
                vids.door.pause();
                vids.doorAmbient.pause();
                audios.door.pause();
                
                audios.bg.play().then(() => { 
                    iconPlay.style.display = 'none'; 
                    iconPause.style.display = 'block'; 
                }).catch(() => {});

                setTimeout(() => {
                    whiteFlash.classList.remove('active');
                }, 800);
            }, 800);
        });"""
        
    door_replacement = """        // ── VIDEO CỬA KẾT THÚC -> FLASH TRẮNG VÀO MAIN LUÔN ──
        vids.door.addEventListener('ended', () => {
            isDoorFinished = true;
            vids.doorAmbient.loop = true;
            
            // Tắt hiệu ứng
            particlesRunning = false;
            vignette.classList.remove('visible');
            particlesCanvas.classList.remove('visible');
            if (doorWrapper) doorWrapper.classList.remove('frozen');

            whiteFlash.classList.add('active');

            setTimeout(() => {
                switchScene(scenes.door, scenes.main);
                
                vids.door.pause();
                vids.doorAmbient.pause();
                audios.door.pause();
                
                audios.bg.play().then(() => { 
                    iconPlay.style.display = 'none'; 
                    iconPause.style.display = 'block'; 
                }).catch(() => {});

                setTimeout(() => {
                    whiteFlash.classList.remove('active');
                }, 800);
            }, 800);
        });"""
    
    # Try replacing it. If it fails, maybe the target string didn't match.
    content = content.replace(door_target, door_replacement)

    # 5. Track Name
    # Search for function loadTrack(index) { ... }
    # and insert loadTrack(0); right after it.
    if "loadTrack(0);" not in content:
        load_track_target = """        function loadTrack(index) {
            let track = tracks[index];
            audios.bg.src = track.file;
            audios.bg.load();
            titleUI.textContent = track.name;
        }"""
        load_track_replacement = load_track_target + "\n        loadTrack(0);"
        content = content.replace(load_track_target, load_track_replacement)

    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(content)

fix_code()
print("Done")
