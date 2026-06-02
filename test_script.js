
        // ── ELEMENTS ────────────────────────────────────────────────
        const scenes = {
            intro: document.getElementById('intro-scene'),
            door:  document.getElementById('door-scene'),
            main:  document.getElementById('main-scene')
        };
        const vids = {
            intro:        document.getElementById('intro-vid'),
            introAmbient: document.getElementById('intro-ambient'),
            door:         document.getElementById('door-vid'),
            doorAmbient:  document.getElementById('door-ambient')
        };
        const audios = {
            intro: document.getElementById('intro-audio'),
            door:  document.getElementById('door-audio'),
            bg:    document.getElementById('bg-music')
        };
        const whiteFlash      = document.getElementById('white-flash');
        const introWrapper    = document.getElementById('intro-wrapper');
        const vignette        = document.getElementById('vignette');
        const particlesCanvas = document.getElementById('particles-canvas');
        const ctx             = particlesCanvas.getContext('2d');

        let isIntroFinished = false;

        function switchScene(from, to) {
            from.classList.remove('active');
            to.classList.add('active');
        }

        // ─── MUSIC PLAYER LOGIC ────────────────────────────────────────
        const musicBtn = document.getElementById('music-btn');
        const tracklistContainer = document.getElementById('tracklist-container');
        const trackListUI = document.getElementById('track-list');
        const titleUI = document.getElementById('player-title');
        const timeUI = document.getElementById('player-time');
        const progressBar = document.getElementById('progress-bar');
        const btnPlayPause = document.getElementById('btn-play-pause');
        const btnNext = document.getElementById('btn-next');
        const btnPrev = document.getElementById('btn-prev');
        const btnShuffle = document.getElementById('btn-shuffle');
        const btnRepeat = document.getElementById('btn-repeat');
        const musicBackdrop = document.getElementById('music-backdrop');
        const iconPlay = document.getElementById('icon-play');
        const iconPause = document.getElementById('icon-pause');
        
        let rawTracks = [
            { name: 'A Day in Mondstadt', file: 'music/A Day in Mondstadt.mp3' },
            { name: 'Bustling Afternoon of Mondstadt', file: 'music/Bustling Afternoon of Mondstadt.mp3' },
            { name: 'Dusk in Mondstadt', file: 'music/Dusk in Mondstadt.mp3' },
            { name: 'Knights of Favonius', file: 'music/Knights of Favonius.m4a' },
            { name: 'Legend of the Wind', file: 'music/Legend of the Wind.mp3' },
            { name: 'Midnight in Monstadt', file: 'music/Midnight in Monstadt.m4a' },
            { name: 'Mondstadt Starlit', file: 'music/Mondstadt Starlit.m4a' },
            { name: 'Moonlike Smile', file: 'music/Moonlike-Smile.m4a' },
            { name: 'Ripples of Daydream', file: 'music/Ripples-of-Daydream.m4a' },
            { name: 'Say My Name', file: 'music/Say My Name.m4a' },
            { name: 'The City Favored By Wind', file: 'music/The City Favored By Wind.mp3' },
            { name: 'Whence the Flow Cometh', file: 'music/Whence-the-Flow-Cometh.m4a' },
            { name: 'Windborne Hymn', file: 'music/WIndborne Hymn.m4a' }
        ];
        
        let hiddenTrack = { name: 'Hidden track (do not click)', file: 'music/Hidden track (do not click).m4a' };
        
        // Sắp xếp bài hát theo ABC và đẩy hidden track xuống cuối
        let tracks = rawTracks.sort((a, b) => a.name.localeCompare(b.name));
        tracks.push(hiddenTrack);
        
        let currentTrackIndex = 0; // Bắt đầu với bài đầu tiên
        let isShuffle = false;
        let repeatMode = 0; // 0: Tắt, 1: Lặp lại danh sách, 2: Lặp lại 1 bài
        let isHiddenTrackUnlocked = false;
        let hasSeenUnlockModal = false;

        audios.bg.loop = false; // Tắt loop mặc định

        const unlockModal = document.getElementById('unlock-modal');
        const closeModalBtn = document.getElementById('close-modal-btn');

        closeModalBtn.addEventListener('click', () => {
            unlockModal.classList.remove('active');
        });

        // Render Tracklist UI
        function renderTracklist() {
            trackListUI.innerHTML = '';
            tracks.forEach((track, index) => {
                let li = document.createElement('li');
                li.className = 'track-item';
                li.textContent = track.name;
                
                let isHidden = track.name === 'Hidden track (do not click)';
                
                if (isHidden && !isHiddenTrackUnlocked) {
                    li.classList.add('track-locked');
                    let lockIcon = document.createElement('span');
                    lockIcon.className = 'lock-icon';
                    lockIcon.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>';
                    li.appendChild(lockIcon);
                } else if (isHidden && isHiddenTrackUnlocked) {
                    let unlockIcon = document.createElement('span');
                    unlockIcon.className = 'lock-icon';
                    unlockIcon.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 9.9-1"></path></svg>';
                    li.appendChild(unlockIcon);
                }
                
                if (index === currentTrackIndex) {
                    li.classList.add('active');
                }
                
                li.addEventListener('click', () => {
                    if (isHidden && !isHiddenTrackUnlocked) {
                        hasSeenUnlockModal = true;
                        unlockModal.classList.add('active');
                        return; // Không cho phát nhạc
                    }
                    currentTrackIndex = index;
                    loadAndPlayTrack();
                });
                trackListUI.appendChild(li);
            });
        }
        renderTracklist();

        // Unlock Quest Trigger: Click vào content cụ thể
        const portfolioRoot = document.querySelector('.portfolio-root');
        
        // Paimon Data
        let exploredSections = [];
        let hasGivenReward = false;
        const allSections = ['about', 'skills', 'experience', 'education', 'awards', 'research', 'contact'];

        // Mobile Research Cards Touch Logic
        document.querySelectorAll('.research-card').forEach(card => {
            card.addEventListener('click', function(e) {
                if (window.matchMedia('(hover: none)').matches) {
                    if (this.classList.contains('active')) {
                        this.classList.remove('active');
                    } else {
                        document.querySelectorAll('.research-card.active').forEach(c => c.classList.remove('active'));
                        this.classList.add('active');
                    }
                }
            });
        });

        
        portfolioRoot.addEventListener('click', (e) => {
            // Kiểm tra xem user có click vào nội dung cụ thể không (tránh click vào khoảng không)
            const isContentClick = e.target.closest('.genshin-card, .timeline-item, .genshin-btn, .nav-link, h1, h2, h3, p, span, img');
            
            // Paimon Tracking
            const section = e.target.closest('section');
            if (section && section.id) {
                if (!exploredSections.includes(section.id) && allSections.includes(section.id)) {
                    exploredSections.push(section.id);
                }
            }
            
            // Không tính khi click vào khu vực music player
            if (e.target.closest('.music-system')) return;
            
            if (isContentClick && hasSeenUnlockModal && !isHiddenTrackUnlocked) {
                isHiddenTrackUnlocked = true;
                renderTracklist();
                
                // Hiển thị Quest completed toast
                const toast = document.getElementById('quest-toast');
                if (toast) {
                    toast.classList.add('active');
                    setTimeout(() => toast.classList.remove('active'), 3000);
                }
            }
        });

        function formatTime(seconds) {
            if (isNaN(seconds)) return "00:00";
            let min = Math.floor(seconds / 60);
            let sec = Math.floor(seconds % 60);
            return (min < 10 ? '0' : '') + min + ':' + (sec < 10 ? '0' : '') + sec;
        }

        // Tải và phát bài hát
        function loadAndPlayTrack(withFadeIn = false) {
            let track = tracks[currentTrackIndex];
            if (audios.bg.src.indexOf(encodeURI(track.file)) === -1) {
                audios.bg.src = track.file;
            }
            titleUI.textContent = track.name;
            
            // Cập nhật trạng thái đang phát trong danh sách
            document.querySelectorAll('.track-item').forEach((li, idx) => {
                if (idx === currentTrackIndex) li.classList.add('active');
                else li.classList.remove('active');
            });
            
            if (withFadeIn) audios.bg.volume = 0;
            
            audios.bg.play().then(() => {
                iconPlay.style.display = 'none';
                iconPause.style.display = 'block';
                if (withFadeIn) fadeAudio(audios.bg, 0, 1, 3000);
            }).catch(e => {
                // Dự phòng nếu trình duyệt chặn autoplay
                if (withFadeIn) {
                    document.addEventListener('pointerdown', () => {
                        audios.bg.play().then(() => {
                            iconPlay.style.display = 'none';
                            iconPause.style.display = 'block';
                            fadeAudio(audios.bg, 0, 1, 3000);
                        });
                    }, { once: true });
                }
            });
        }

        // -------------------------
        // PAIMON LOGIC
        // -------------------------
        const paimonContainer = document.getElementById('paimon-guide');
        const paimonAvatar = document.getElementById('paimon-avatar');
        const paimonDialog = document.querySelector('.paimon-dialog');
        const paimonText = document.getElementById('paimon-text');
        const paimonAction = document.getElementById('paimon-action');
        const paimonClose = document.getElementById('paimon-close');
        const paimonToggleBtn = document.getElementById('paimon-toggle-btn');
        
        const sectionNames = {
            'about': 'About',
            'skills': 'Skills',
            'experience': 'Experience',
            'education': 'Education',
            'awards': 'Awards',
            'research': 'Research & Essays',
            'contact': 'Contact'
        };
        let suggestedSection = null;

        if (paimonToggleBtn) {
            paimonToggleBtn.addEventListener('click', () => {
                paimonContainer.classList.toggle('hidden');
            });
        }
        
        // Tutorial State
        let tutorialStep = -1;
        const tutorialElements = [
            { id: 'genshin-nav', text: 'This is the Navigation Bar. You can use it to quickly jump to different sections of the page!' },
            { id: 'music-btn', text: 'In the top right is the Music button. Click here to toggle the Media Player!' },
            { id: 'btn-toggle-tracklist', text: 'Inside the Media Player is the Menu button. Click it to open the Tracklist!', preAction: () => { const md = document.querySelector('.music-dropdown'); if (md) md.classList.remove('hidden'); } },
            { id: 'paimon-toggle-btn', text: "In the top left is Paimon's icon. Click here to summon me or let me rest!" },
            { id: 'paimon-avatar', text: "Finally, if you don't know what to explore next, just click on me and Paimon will give you a suggestion!" }
        ];
        
        function forceCleanupTutorial() {
            document.querySelectorAll('.tutorial-highlight').forEach(el => el.classList.remove('tutorial-highlight'));
            document.querySelectorAll('.tutorial-parent-elevate').forEach(el => el.classList.remove('tutorial-parent-elevate'));
            document.querySelectorAll('.local-tutorial-overlay').forEach(el => el.remove());
            const globalOverlay = document.getElementById('tutorial-overlay');
            if(globalOverlay) globalOverlay.classList.add('hidden');
            
            // Clean up any interaction popups that might have been opened during tutorial
            const md = document.querySelector('.music-dropdown');
            if (md) md.classList.add('hidden');
            const mb = document.getElementById('music-backdrop');
            if (mb) mb.classList.remove('active');
            const certModal = document.getElementById('cert-modal');
            if (certModal) certModal.classList.add('hidden');
        }
        
        function highlightTutorialStep(stepIndex) {
            document.querySelectorAll('.tutorial-highlight').forEach(el => el.classList.remove('tutorial-highlight'));
            document.querySelectorAll('.tutorial-parent-elevate').forEach(el => el.classList.remove('tutorial-parent-elevate'));
            document.querySelectorAll('.local-tutorial-overlay').forEach(el => el.remove());
            
            if (stepIndex >= tutorialElements.length) {
                tutorialStep = -1;
                document.getElementById('tutorial-overlay').classList.add('hidden');
                paimonText.innerHTML = "That's it! Now feel free to explore, Traveler! Have fun! ✨";
                paimonAction.innerHTML = "Let's explore!";
                suggestedSection = 'tutorial_end';
                paimonAction.style.display = 'block';
                return;
            }
            
            const step = tutorialElements[stepIndex];
            if (step.preAction) step.preAction();
            
            let targetEl = document.getElementById(step.id) || document.querySelector('.' + step.id);
            if (targetEl) {
                targetEl.classList.add('tutorial-highlight');
                
                let parent = targetEl.parentElement;
                while(parent && parent.classList && !parent.classList.contains('portfolio-root') && parent !== document.body) {
                    const style = window.getComputedStyle(parent);
                    if (style.zIndex !== 'auto' && style.position !== 'static') {
                        parent.classList.add('tutorial-parent-elevate');
                        let overlay = document.createElement('div');
                        overlay.className = 'local-tutorial-overlay';
                        parent.appendChild(overlay);
                    }
                    parent = parent.parentElement;
                }
                
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            
            paimonText.innerHTML = step.text;
            paimonAction.innerHTML = "Next ➜";
            suggestedSection = 'tutorial_next';
            paimonAction.style.display = 'block';
        }

        // Auto-show Paimon on load
        setTimeout(() => {
            if (paimonDialog && paimonContainer && !paimonContainer.classList.contains('hidden')) {
                paimonDialog.classList.remove('hidden');
                paimonText.innerHTML = "Hi Traveler! Welcome to my Portfolio! ✨<br><br>Would you like Paimon to show you around?";
                paimonAction.innerHTML = "Start Tutorial 🗺️";
                suggestedSection = 'tutorial_start';
                paimonAction.style.display = 'block';
            }
        }, 1500);

        const notExploredLines = [
            "Hey Traveler! You haven't explored the <b style=\"color:var(--gold-bright)\">{section}</b> section yet. Let's go!",
            "Paimon thinks we should check out <b style=\"color:var(--gold-bright)\">{section}</b> next. What do you say?",
            "Look over there! The <b style=\"color:var(--gold-bright)\">{section}</b> section is waiting for us!",
            "Traveler! Don't forget to look at the <b style=\"color:var(--gold-bright)\">{section}</b> part of the portfolio!",
            "Ooh, Paimon is curious about your <b style=\"color:var(--gold-bright)\">{section}</b>. Let's take a look!"
        ];
        
        const fullyExploredLines = [
            "Wow! You've explored every corner of this portfolio! Paimon is impressed!",
            "Looks like we've seen it all, Traveler! Good job!",
            "Paimon is tired from all this exploring. But we checked everything!",
            "Every section has been visited. You're a true adventurer!"
        ];
        
        const cheerLines = [
            "You're doing great, Traveler! Keep up the good work! ✨",
            "Paimon believes in you! You can do anything you set your mind to! ᕙ(`▽´)ᕗ",
            "Is it time for a snack break? Paimon could really go for some Sticky Honey Roast right now... 🤤",
            "Don't push yourself too hard! Taking a break is just as important as working hard! 🛌",
            "Hehe, Paimon is always here to cheer you on! 🌟",
            "Whatever challenges come your way, Paimon knows you'll overcome them! ⚔️"
        ];

        if (paimonAvatar) {
            paimonAvatar.addEventListener('click', () => {
                if (tutorialStep !== -1 || suggestedSection === 'tutorial_end') return;
                // Kích hoạt animation nhảy
                paimonAvatar.classList.remove('jump');
                void paimonAvatar.offsetWidth; // trigger reflow
                paimonAvatar.classList.add('jump');
                setTimeout(() => {
                    if (paimonAvatar) paimonAvatar.classList.remove('jump');
                }, 500);

                const unexplored = allSections.filter(s => !exploredSections.includes(s));
                if (unexplored.length > 0) {
                    // 25% cơ hội Paimon nói những câu đáng yêu/cổ vũ thay vì gợi ý
                    if (Math.random() < 0.25) {
                        suggestedSection = null;
                        const randomLine = cheerLines[Math.floor(Math.random() * cheerLines.length)];
                        paimonText.innerHTML = randomLine;
                        paimonAction.style.display = 'none';
                    } else {
                        suggestedSection = unexplored[Math.floor(Math.random() * unexplored.length)];
                        const randomLine = notExploredLines[Math.floor(Math.random() * notExploredLines.length)].replace('{section}', sectionNames[suggestedSection]);
                        paimonText.innerHTML = randomLine;
                        paimonAction.innerHTML = "Teleport 🌠";
                        paimonAction.style.display = 'block';
                    }
                } else {
                    if (!hasGivenReward) {
                        suggestedSection = 'reward';
                        paimonText.innerHTML = "Wow! You've explored every corner of this portfolio! Paimon is impressed! Here is a special reward just for you! ✨";
                        paimonAction.innerHTML = "Reward 🎁";
                        paimonAction.style.display = 'block';
                        hasGivenReward = true;
                    } else {
                        suggestedSection = null;
                        const allFunLines = fullyExploredLines.concat(cheerLines);
                        const randomLine = allFunLines[Math.floor(Math.random() * allFunLines.length)];
                        paimonText.innerHTML = randomLine;
                        paimonAction.style.display = 'none';
                    }
                }
                paimonDialog.classList.remove('hidden');
            });
        }

        if (paimonClose) {
                        paimonClose.addEventListener('click', (e) => {
                e.stopPropagation();
                paimonDialog.classList.add('hidden');
                if (tutorialStep >= 0) {
                    tutorialStep = -1;
                    forceCleanupTutorial();
                }
            });
        }

        if (paimonAction) {
            paimonAction.addEventListener('click', (e) => {
                e.stopPropagation();
                if (suggestedSection === 'reward') {
                    window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1', '_blank');
                    paimonDialog.classList.add('hidden');
                } else if (suggestedSection === 'tutorial_start') {
                    const overlay = document.getElementById('tutorial-overlay');
                    if (overlay) overlay.classList.remove('hidden');
                    tutorialStep = 0;
                    highlightTutorialStep(tutorialStep);
                } else if (suggestedSection === 'tutorial_next') {
                    tutorialStep++;
                    highlightTutorialStep(tutorialStep);
                } else if (suggestedSection === 'tutorial_end') {
                    paimonDialog.classList.add('hidden');
                    const md = document.querySelector('.music-dropdown');
                    if (md && !md.classList.contains('hidden')) {
                        md.classList.add('hidden');
                    }
                    suggestedSection = null;
                forceCleanupTutorial();
                } else if (suggestedSection) {
                    const targetEl = document.getElementById(suggestedSection);
                    if (targetEl) {
                        targetEl.scrollIntoView({ behavior: 'smooth' });
                        if (!exploredSections.includes(suggestedSection)) {
                            exploredSections.push(suggestedSection);
                        }
                    }
                    paimonDialog.classList.add('hidden');
                }
            });
        }
        // -------------------------

        // Bật/tắt dropdown và hiệu ứng mờ web
        const btnHidePlayer = document.getElementById('btn-hide-player');
        const musicDropdown = document.querySelector('.music-dropdown');

        btnHidePlayer.addEventListener('click', () => {
            musicDropdown.classList.add('hidden');
            if (tracklistContainer.classList.contains('open')) {
                tracklistContainer.classList.remove('open');
                musicBackdrop.classList.remove('active');
            }
        });

        const btnToggleTracklist = document.getElementById('btn-tracklist-menu');
        btnToggleTracklist.addEventListener('click', () => {
            tracklistContainer.classList.toggle('open');
            musicBackdrop.classList.toggle('active');
        });

        musicBtn.addEventListener('click', () => {
            if (musicDropdown.classList.contains('hidden')) {
                musicDropdown.classList.remove('hidden');
            } else {
                musicDropdown.classList.add('hidden');
                if (tracklistContainer.classList.contains('open')) {
                    tracklistContainer.classList.remove('open');
                    musicBackdrop.classList.remove('active');
                }
            }
        });

        // Bấm ra ngoài (lên lớp mờ) để đóng
        musicBackdrop.addEventListener('click', () => {
            tracklistContainer.classList.remove('open');
            musicBackdrop.classList.remove('active');
        });

        // Play/Pause
        btnPlayPause.addEventListener('click', () => {
            if (audios.bg.paused) {
                audios.bg.play();
                iconPlay.style.display = 'none';
                iconPause.style.display = 'block';
            } else {
                audios.bg.pause();
                iconPlay.style.display = 'block';
                iconPause.style.display = 'none';
            }
        });

        // Next/Prev Bài Hát
        function playNext() {
            const playableLength = isHiddenTrackUnlocked ? tracks.length : tracks.length - 1;
            if (isShuffle) {
                currentTrackIndex = Math.floor(Math.random() * playableLength);
            } else {
                currentTrackIndex = (currentTrackIndex + 1) % playableLength;
            }
            loadAndPlayTrack();
        }
        function playPrev() {
            const playableLength = isHiddenTrackUnlocked ? tracks.length : tracks.length - 1;
            if (isShuffle) {
                currentTrackIndex = Math.floor(Math.random() * playableLength);
            } else {
                currentTrackIndex = (currentTrackIndex - 1 + playableLength) % playableLength;
            }
            loadAndPlayTrack();
        }
        btnNext.addEventListener('click', playNext);
        btnPrev.addEventListener('click', playPrev);

        // Progress Bar
        audios.bg.addEventListener('timeupdate', () => {
            if (!isNaN(audios.bg.duration)) {
                let current = audios.bg.currentTime;
                let duration = audios.bg.duration;
                progressBar.value = (current / duration) * 100;
                timeUI.textContent = formatTime(current) + " / " + formatTime(duration);
            }
        });
        audios.bg.addEventListener('loadedmetadata', () => {
            timeUI.textContent = "00:00 / " + formatTime(audios.bg.duration);
        });
        progressBar.addEventListener('input', () => {
            let duration = audios.bg.duration;
            audios.bg.currentTime = (progressBar.value / 100) * duration;
        });

        // Khi bài hát kết thúc
        audios.bg.addEventListener('ended', () => {
            if (repeatMode === 2) {
                audios.bg.currentTime = 0;
                audios.bg.play(); // Lặp 1 bài
            } else if (repeatMode === 1) {
                playNext(); // Lặp cả list
            } else {
                // Không lặp, nếu hết list thì dừng, chưa hết thì Next
                const playableLength = isHiddenTrackUnlocked ? tracks.length : tracks.length - 1;
                if (currentTrackIndex < playableLength - 1) playNext();
                else {
                    iconPlay.style.display = 'block';
                    iconPause.style.display = 'none';
                }
            }
        });

        // Nút Trộn Bài (Shuffle)
        btnShuffle.addEventListener('click', () => {
            isShuffle = !isShuffle;
            btnShuffle.classList.toggle('active', isShuffle);
        });

        // Nút Lặp Lại (Repeat: Tắt -> Tất cả -> 1 bài)
        btnRepeat.addEventListener('click', () => {
            repeatMode = (repeatMode + 1) % 3;
            if (repeatMode === 0) {
                btnRepeat.classList.remove('active');
                btnRepeat.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>';
            } else if (repeatMode === 1) {
                btnRepeat.classList.add('active');
                btnRepeat.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path></svg>';
            } else if (repeatMode === 2) {
                btnRepeat.classList.add('active');
                btnRepeat.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"></polyline><path d="M3 11V9a4 4 0 0 1 4-4h14"></path><polyline points="7 23 3 19 7 15"></polyline><path d="M21 13v2a4 4 0 0 1-4 4H3"></path><text x="12" y="16" font-size="8" font-family="sans-serif" text-anchor="middle" fill="currentColor">1</text></svg>';
            }
        });

        // ── AUTOPLAY ÂM THANH (hook vào video muted) ─────────────────
                const startScreen = document.getElementById('start-screen');
        startScreen.addEventListener('click', () => {
            startScreen.classList.add('hidden');
            vids.intro.play();
            vids.introAmbient.play();
            audios.intro.play().catch(() => {});
        });

        // SHARED FX CANVAS - click burst + mouse trail dùng chung 1 canvas
        // ═══════════════════════════════════════════════════════
        const fxCanvas = document.createElement('canvas');
        fxCanvas.style.cssText = `
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 99998;
        `;
        document.body.appendChild(fxCanvas);
        const fxCtx = fxCanvas.getContext('2d');

        function resizeFxCanvas() {
            fxCanvas.width  = window.innerWidth;
            fxCanvas.height = window.innerHeight;
        }
        resizeFxCanvas();
        window.addEventListener('resize', resizeFxCanvas);

        // ─── CLICK BURST (Epic Seven Style - Vàng Xanh Trắng) ───────────
        let clickBursts = [];

        function spawnClickBurst(x, y) {
            clickBursts.push({ 
                type: 'epic7', 
                x, y, 
                r: 0, 
                maxR: 35, // Vòng tròn nhỏ
                life: 1.0, 
                decay: 0.018, // Kéo dài thời gian hiệu ứng ~ gấp đôi
                angle: Math.random() * Math.PI 
            });
        }

        function updateClickBursts() {
            for (let i = clickBursts.length - 1; i >= 0; i--) {
                const p = clickBursts[i];
                if (p.type === 'epic7') {
                    p.r += (p.maxR - p.r) * 0.12; // Lan tỏa chậm lại một chút để khớp với thời gian
                    p.life -= p.decay;
                    p.angle += 0.02;
                    
                    const alpha = Math.max(0, p.life);
                    const brightAlpha = Math.min(1, alpha * 1.5); // Giữ độ sáng cao lâu hơn
                    
                    // 1. Dư ảnh màu trắng rực rỡ bên trong (Inner Flash)
                    const innerR = p.r * 0.95;
                    if (innerR > 0) {
                        fxCtx.beginPath();
                        fxCtx.arc(p.x, p.y, innerR, 0, Math.PI * 2);
                        const flashGrad = fxCtx.createRadialGradient(p.x, p.y, 0, p.x, p.y, innerR);
                        flashGrad.addColorStop(0, `rgba(255, 255, 255, ${brightAlpha})`);
                        flashGrad.addColorStop(0.6, `rgba(255, 255, 255, ${brightAlpha * 0.8})`);
                        flashGrad.addColorStop(1, `rgba(255, 255, 255, 0)`);
                        fxCtx.fillStyle = flashGrad;
                        fxCtx.fill();
                    }

                    // 2. Vòng tròn viền ngoài sáng rực
                    fxCtx.beginPath();
                    fxCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    fxCtx.strokeStyle = `rgba(255, 255, 255, ${brightAlpha})`;
                    fxCtx.lineWidth = 1.5 + alpha * 3;
                    fxCtx.shadowBlur = 15 + alpha * 10; // Tăng cường độ phát sáng
                    fxCtx.shadowColor = `rgba(173, 255, 47, ${brightAlpha})`;
                    fxCtx.stroke();
                    fxCtx.shadowBlur = 0;
                    
                    // 3. Ngôi sao 4 cánh (Glow) ở giữa sáng hơn
                    const starSize = p.maxR * (1 - alpha) * 0.8 + 20; 
                    
                    fxCtx.save();
                    fxCtx.translate(p.x, p.y);
                    fxCtx.rotate(p.angle);
                    
                    fxCtx.beginPath();
                    const spikes = 4;
                    const innerRadius = starSize * 0.15;
                    for (let j = 0; j < spikes * 2; j++) {
                        const r = (j % 2 === 0) ? starSize : innerRadius;
                        const a = (Math.PI / spikes) * j;
                        fxCtx.lineTo(Math.cos(a) * r, Math.sin(a) * r);
                    }
                    fxCtx.closePath();
                    
                    const grad = fxCtx.createRadialGradient(0, 0, 0, 0, 0, starSize);
                    grad.addColorStop(0, `rgba(255, 255, 255, ${brightAlpha})`);
                    grad.addColorStop(0.4, `rgba(215, 255, 100, ${brightAlpha})`);
                    grad.addColorStop(0.8, `rgba(130, 255, 50, ${alpha * 0.8})`);
                    grad.addColorStop(1, `rgba(50, 200, 100, 0)`);
                    
                    fxCtx.fillStyle = grad;
                    fxCtx.fill();
                    fxCtx.restore();
                    
                    if (p.life <= 0) clickBursts.splice(i, 1);
                }
            }
        }

        function playRandomClickSound() {
            // No global mute check anymore
            const r = Math.floor(Math.random() * 5) + 1;
            const snd = new Audio(`content/cursorsound${r}.m4a`);
            snd.volume = 0.6;
            snd.play().catch(() => {});
        }

        document.addEventListener('click', (e) => {
            spawnClickBurst(e.clientX, e.clientY);
            playRandomClickSound();
        });

        // ─── MOUSE TRAIL - đường thẳng từ ĐUÔI cursor (rocket exhaust) ──
        // Điểm trail được spawn NGƯỢC hướng di chuyển 12px → trail luôn
        // nằm phía sau cursor, không tại mũi. Vẽ dạng đường như cũ.
        const TRAIL_LEN = 22;
        let mouseTrail = [];
        let prevMx = 0, prevMy = 0;

        document.addEventListener('mousemove', (e) => {
            // Loại bỏ offset tính bằng vận tốc (tránh glitch/nhảy góc)
            // Ghi nhận trực tiếp tọa độ con trỏ chuột
            mouseTrail.push({ x: e.clientX, y: e.clientY, age: 1.0 });
            if (mouseTrail.length > TRAIL_LEN) mouseTrail.shift();
        });

        function updateMouseTrail() {
            for (let p of mouseTrail) p.age -= 0.055;
            mouseTrail = mouseTrail.filter(p => p.age > 0);
            if (mouseTrail.length < 2) return;

            for (let i = 0; i < mouseTrail.length - 1; i++) {
                // t=0: điểm cũ nhất (đuôi xa) → t=1: điểm mới nhất (chính xác tại mũi cursor)
                const t  = i / (mouseTrail.length - 1);
                const p0 = mouseTrail[i];
                const p1 = mouseTrail[i + 1];

                // Dùng đường cong hình chuông (bell curve):
                // Mũi (t=1): bell ~ 0 → mỏng & trong suốt (cảm giác xuất phát TỪ ĐUÔI mũi)
                // Giữa (t=0.6): bell ~ 1 → to nhất, sáng nhất (lõi lửa)
                // Đuôi (t=0): bell = 0 → mỏng dần, mờ đi
                const bell = Math.sin(Math.pow(t, 0.8) * Math.PI);

                const w     = bell * 6 + 0.3;
                const lig   = 40 + bell * 35;
                const alpha = p0.age * (bell * 0.9 + 0.1);

                fxCtx.beginPath();
                fxCtx.moveTo(p0.x, p0.y);
                fxCtx.lineTo(p1.x, p1.y);
                fxCtx.strokeStyle = `hsla(168, 95%, ${lig}%, ${alpha})`;
                fxCtx.lineWidth   = w;
                fxCtx.lineCap     = 'round';
                fxCtx.shadowBlur  = bell * 14;
                fxCtx.shadowColor = 'hsl(168, 100%, 70%)';
                fxCtx.stroke();
                fxCtx.shadowBlur  = 0;
            }
        }

        // ─── MAIN FX LOOP ──────────────────────────────────────────────
        function fxLoop() {
            requestAnimationFrame(fxLoop);
            fxCtx.clearRect(0, 0, fxCanvas.width, fxCanvas.height);
            updateMouseTrail();
            updateClickBursts();
        }
        fxLoop();

        // ── INIT DANDELIONS ───────────────────────────────────
        function initDandelions() {
            const container = document.getElementById('dandelion-container');
            if (!container) return;
            const seedCount = 25;
            for (let i = 0; i < seedCount; i++) {
                const seed = document.createElement('div');
                seed.classList.add('dandelion-seed');
                
                const leftPos = Math.random() * 100;
                const animDuration = 12 + Math.random() * 15;
                const animDelay = Math.random() * 20;
                const drift = (Math.random() - 0.5) * 2;
                const scale = 0.5 + Math.random() * 0.8;
                
                seed.style.left = `${leftPos}%`;
                seed.style.animationDuration = `${animDuration}s`;
                seed.style.animationDelay = `-${animDelay}s`;
                seed.style.setProperty('--drift', drift);
                seed.style.setProperty('--scale', scale);
                
                container.appendChild(seed);
            }
        }
        initDandelions();


        // Certificate Modal Logic
        const certModal = document.getElementById('cert-modal');
        const certModalImg = document.getElementById('cert-modal-img');
        const certModalClose = document.querySelector('.cert-modal-close');
        certModalImg.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!certModalImg.classList.contains('zoomed')) {
                const rect = certModalImg.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                certModalImg.style.transformOrigin = `${x}% ${y}%`;
                certModalImg.classList.add('zoomed');
            } else {
                certModalImg.classList.remove('zoomed');
                setTimeout(() => { certModalImg.style.transformOrigin = 'center'; }, 300);
            }
        });

        
        document.querySelectorAll('.award-item.cert').forEach(item => {
            item.addEventListener('click', () => {
                const imgSrc = item.getAttribute('data-img');
                if (imgSrc) {
                    certModalImg.src = imgSrc;
                    certModal.classList.add('active');
                }
            });
        });

        certModalClose.addEventListener('click', () => {
            certModal.classList.remove('active');
            certModalImg.classList.remove('zoomed');
            setTimeout(() => { certModalImg.src = ''; }, 300);
        });

        certModal.addEventListener('click', (e) => {
            if (e.target === certModal) {
                certModal.classList.remove('active');
                certModalImg.classList.remove('zoomed');
                setTimeout(() => { certModalImg.src = ''; }, 300);
            }
        });
    