import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

target = """        vids.intro.addEventListener('ended', () => {"""

particle_logic = """        // ── PARTICLES EFFECT CHO FREEZE FRAME ──
        let particles = [];
        let particlesRunning = false;
        const particlesCount = 100;
        
        function initParticles() {
            if (!particlesCanvas) return;
            particlesCanvas.width = window.innerWidth;
            particlesCanvas.height = window.innerHeight;
            particles = [];
            for (let i = 0; i < particlesCount; i++) {
                particles.push({
                    x: Math.random() * particlesCanvas.width,
                    y: Math.random() * particlesCanvas.height,
                    size: Math.random() * 2 + 1,
                    speedX: Math.random() * 0.5 - 0.25,
                    speedY: Math.random() * 0.5 - 0.25,
                    opacity: Math.random() * 0.5 + 0.3
                });
            }
        }
        
        function animateParticles() {
            if (!particlesRunning || !ctx) return;
            ctx.clearRect(0, 0, particlesCanvas.width, particlesCanvas.height);
            
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                p.x += p.speedX;
                p.y += p.speedY;
                
                if (p.x < 0) p.x = particlesCanvas.width;
                if (p.x > particlesCanvas.width) p.x = 0;
                if (p.y < 0) p.y = particlesCanvas.height;
                if (p.y > particlesCanvas.height) p.y = 0;
                
                ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            }
            requestAnimationFrame(animateParticles);
        }
        
        window.addEventListener('resize', () => {
            if (particlesRunning && particlesCanvas) {
                particlesCanvas.width = window.innerWidth;
                particlesCanvas.height = window.innerHeight;
            }
        });
        initParticles();

        vids.intro.addEventListener('ended', () => {"""

if target in content and "function animateParticles" not in content:
    content = content.replace(target, particle_logic)
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(content)
    print("Injected particles logic.")
else:
    print("Already injected or target not found.")
