import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

bad_target = """        vids.intro.addEventListener('timeupdate', () => {
            if (vids.intro.currentTime >= vids.intro.duration - 0.5 && !isIntroFinished) {
                isIntroFinished = true;
                whiteFlash.classList.add('active');
                setTimeout(() => {
                    switchScene(scenes.intro, scenes.door);
                    vids.door.play();
                    vids.doorAmbient.play();
                    audios.door.play().catch(() => {});
                    setTimeout(() => whiteFlash.classList.remove('active'), 800);
                }, 800);
            }
        });

        scenes.door.addEventListener('click', () => {
            whiteFlash.classList.add('active');
            setTimeout(() => {
                switchScene(scenes.door, scenes.main);
                vids.door.pause();
                vids.doorAmbient.pause();
                audios.door.pause();
                audios.bg.play().then(() => { iconPlay.style.display = 'none'; iconPause.style.display = 'block'; }).catch(() => {});
                setTimeout(() => whiteFlash.classList.remove('active'), 800);
            }, 800);
        });"""

good_target = """        let isDoorFinished = false;
        const doorWrapper = document.getElementById('door-wrapper');

        vids.intro.addEventListener('ended', () => {
             isIntroFinished = true;
             vids.introAmbient.loop = true;
             scenes.intro.style.cursor = "url('cursor/genshin_link.cur'), pointer";
             introWrapper.classList.add('frozen');
             vignette.classList.add('visible');
             particlesCanvas.classList.add('visible');
             particlesRunning = true;
             requestAnimationFrame(animateParticles);
        });

        // ── CLICK -> CHUYỂN SANG CỬA ──
        scenes.intro.addEventListener('click', () => {
            if (!isIntroFinished) return;

            // Chuyển hiệu ứng viền sáng sang cửa, GIỮ NGUYÊN particles và vignette
            introWrapper.classList.remove('frozen');
            doorWrapper.classList.add('frozen');
            
            audios.intro.pause();

            switchScene(scenes.intro, scenes.door);
            vids.door.play();
            vids.doorAmbient.play();
            audios.door.play();
        });

        // ── VIDEO CỬA KẾT THÚC -> ĐỢI CLICK ──
        vids.door.addEventListener('ended', () => {
            isDoorFinished = true;
            vids.doorAmbient.loop = true;
            scenes.door.style.cursor = "url('cursor/genshin_link.cur'), pointer";
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

if bad_target in content:
    new_content = content.replace(bad_target, good_target)
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("BAD TARGET NOT FOUND")
    # let's try to find it without exact whitespace
