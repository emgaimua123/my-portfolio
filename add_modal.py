import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add CSS
css_anchor = '    </style>'
css_inject = '''        /* Certificate Modal */
        .cert-modal {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 10000;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .cert-modal.active {
            opacity: 1;
            pointer-events: auto;
        }
        .cert-modal img {
            max-width: 90%;
            max-height: 90vh;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            transform: scale(0.8);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .cert-modal.active img {
            transform: scale(1);
        }
        .cert-modal-close {
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            cursor: pointer;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            transition: color 0.3s;
        }
        .cert-modal-close:hover {
            color: #ff5555;
        }
        .award-item.cert {
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }
        .award-item.cert:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
            background: rgba(230, 194, 117, 0.1);
        }
        .award-item.cert::after {
            content: "👁 View";
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.8rem;
            color: var(--gold-bright);
            opacity: 0;
            transition: opacity 0.2s;
        }
        .award-item.cert:hover::after {
            opacity: 1;
        }
    </style>'''
content = content.replace(css_anchor, css_inject)

# 2. Update certificates HTML with data-img
old_certs = '''                            <div class="award-item cert">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">IELTS 7.5</p>
                                    <p class="award-date">Aug 2023</p>
                                </div>
                            </div>
                            <div class="award-item cert">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">JLPT N4</p>
                                    <p class="award-date">Jan 2026 (91/180)</p>
                                </div>
                            </div>
                            <div class="award-item cert">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">JLPT N5</p>
                                    <p class="award-date">Aug 2023 (104/180)</p>
                                </div>
                            </div>'''
new_certs = '''                            <div class="award-item cert" data-img="content/IELTS.jpg">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">IELTS 7.5</p>
                                    <p class="award-date">Aug 2023</p>
                                </div>
                            </div>
                            <div class="award-item cert" data-img="content/JLPT N4.jpg">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">JLPT N4</p>
                                    <p class="award-date">Jan 2026 (91/180)</p>
                                </div>
                            </div>
                            <div class="award-item cert" data-img="content/JLPT N5.jpg">
                                <span class="award-icon">📜</span>
                                <div>
                                    <p class="award-title">JLPT N5</p>
                                    <p class="award-date">Aug 2023 (104/180)</p>
                                </div>
                            </div>'''
content = content.replace(old_certs, new_certs)

# 3. Add Modal to Body
html_body_anchor = '    <div id="tutorial-overlay" class="tutorial-overlay hidden"></div>'
html_body_inject = '''    <div id="tutorial-overlay" class="tutorial-overlay hidden"></div>

    <!-- Certificate Modal -->
    <div id="cert-modal" class="cert-modal">
        <span class="cert-modal-close">&times;</span>
        <img id="cert-modal-img" src="" alt="Certificate">
    </div>'''
content = content.replace(html_body_anchor, html_body_inject)

# 4. Add JavaScript
js_anchor = '    </script>'
js_inject = '''
        // Certificate Modal Logic
        const certModal = document.getElementById('cert-modal');
        const certModalImg = document.getElementById('cert-modal-img');
        const certModalClose = document.querySelector('.cert-modal-close');
        
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
            setTimeout(() => { certModalImg.src = ''; }, 300);
        });

        certModal.addEventListener('click', (e) => {
            if (e.target === certModal) {
                certModal.classList.remove('active');
                setTimeout(() => { certModalImg.src = ''; }, 300);
            }
        });
    </script>'''
content = content.replace(js_anchor, js_inject)

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)

print("Modal Update Done!")
