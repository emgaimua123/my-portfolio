import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

# JS Auto-show
js_auto_show_anchor = """        // Auto-show Paimon on load
        setTimeout(() => {
            if (paimonDialog && paimonContainer && !paimonContainer.classList.contains('hidden')) {
                paimonDialog.classList.remove('hidden');
                paimonText.innerHTML = "Hi Traveler! Welcome to my Portfolio! ✨<br><br><small style='color: var(--gold-bright);'><i>(Nhấn vào Paimon để nhận gợi ý khám phá nhé!)</i></small>";
                paimonAction.style.display = 'none';
            }
        }, 1500);"""
js_auto_show_new = """        // Tutorial State
        let tutorialStep = -1;
        const tutorialElements = [
            { id: 'genshin-nav', text: 'Đây là thanh điều hướng (Navigation Bar). Bạn có thể dùng nó để nhảy nhanh tới các phần của trang nhé!' },
            { id: 'music-btn', text: 'Góc trên bên phải là nút Music. Click vào đây để mở/tắt trình phát nhạc (Media Player)!' },
            { id: 'btn-toggle-tracklist', text: 'Bên trong Media Player có nút Menu này. Hãy nhấn để mở danh sách bài hát (Tracklist)!', preAction: () => { const md = document.querySelector('.music-dropdown'); if (md) md.classList.remove('hidden'); } },
            { id: 'paimon-toggle-btn', text: 'Góc trên bên trái là biểu tượng của Paimon. Nhấn vào đây để gọi Paimon ra hoặc cho Paimon nghỉ ngơi!' },
            { id: 'paimon-avatar', text: 'Cuối cùng, nếu bạn không biết xem gì tiếp theo, cứ nhấn vào người Paimon, Paimon sẽ gợi ý cho bạn!' }
        ];
        
        function highlightTutorialStep(stepIndex) {
            document.querySelectorAll('.tutorial-highlight').forEach(el => el.classList.remove('tutorial-highlight'));
            
            if (stepIndex >= tutorialElements.length) {
                tutorialStep = -1;
                document.getElementById('tutorial-overlay').classList.add('hidden');
                paimonText.innerHTML = "Vậy là xong rồi đó! Giờ thì tự do khám phá nhé Traveler! Have fun! ✨";
                paimonAction.innerHTML = "Khám phá thôi!";
                suggestedSection = 'tutorial_end';
                paimonAction.style.display = 'block';
                return;
            }
            
            const step = tutorialElements[stepIndex];
            if (step.preAction) step.preAction();
            
            let targetEl = document.getElementById(step.id) || document.querySelector('.' + step.id);
            if (targetEl) {
                targetEl.classList.add('tutorial-highlight');
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
                paimonText.innerHTML = "Hi Traveler! Welcome to my Portfolio! ✨<br><br>Bạn có muốn Paimon hướng dẫn một chút về cách sử dụng các tính năng ở đây không?";
                paimonAction.innerHTML = "Start Tutorial 🗺️";
                suggestedSection = 'tutorial_start';
                paimonAction.style.display = 'block';
            }
        }, 1500);"""

if js_auto_show_anchor in content:
    content = content.replace(js_auto_show_anchor, js_auto_show_new)
    print('Replaced auto show')
else:
    print('Could not find auto show block')

# JS paimonAction listener
js_listener_anchor = """        if (paimonAction) {
            paimonAction.addEventListener('click', (e) => {
                e.stopPropagation();
                if (suggestedSection === 'reward') {
                    window.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1', '_blank');
                    paimonDialog.classList.add('hidden');
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
        }"""
js_listener_new = """        if (paimonAction) {
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
        }"""

if js_listener_anchor in content:
    content = content.replace(js_listener_anchor, js_listener_new)
    print('Replaced listener')
else:
    print('Could not find listener block')

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)
print('Done!')
