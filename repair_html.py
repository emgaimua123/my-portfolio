import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

bad_chunk_1 = '''                        <div class="timeline-card">
                            <div class="tl-top">
                                <h3 class="tl-title">Math & English Tutor</h3>
                                <span class="tl-date">7/2024 - Present</span>
                            </div>
                            <p class="tl-org">Freelance</p>
                            <p class="tl-desc">Tutoring elementary and middle school students. All students have shown significant improvement in their academic results.</p>
                        </div>
                    </div>'''

good_chunk_1 = '''                    <!-- Card 3 -->
                    <div class="genshin-card">
                        <div class="card-icon">🌐</div>
                        <h3 class="card-title">Foreign Languages</h3>
                        <p class="card-desc">Fluent English (IELTS 7.5). Currently learning Japanese (JLPT N4). Confident in communicating and teaching in English.</p>
                        <div class="card-footer">
                            <span class="skill-bar">
                                <span class="skill-fill" style="width:92%"></span>
                            </span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- EXPERIENCE -->
            <section class="section" id="experience">
                <div class="section-header">
                    <span class="section-gem"></span>
                    <h2 class="section-title">Experience</h2>
                    <span class="section-gem"></span>
                </div>

                <div class="timeline">
                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-card">
                            <div class="tl-top">
                                <h3 class="tl-title">English Teaching Assistant</h3>
                                <span class="tl-date">7/2024 - Present</span>
                            </div>
                            <p class="tl-org">Sao Viet Cultural Enrichment Center</p>
                            <p class="tl-desc">Experienced in tutoring, assisting, and leading classes of various proficiency levels.</p>
                        </div>
                    </div>

                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-card">
                            <div class="tl-top">
                                <h3 class="tl-title">Math & English Tutor</h3>
                                <span class="tl-date">7/2024 - Present</span>
                            </div>
                            <p class="tl-org">Freelance</p>
                            <p class="tl-desc">Tutoring elementary and middle school students. All students have shown significant improvement in their academic results.</p>
                        </div>
                    </div>

                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-card">
                            <div class="tl-top">
                                <h3 class="tl-title">Student Volunteer</h3>
                                <span class="tl-date">8/2024 - Present</span>
                            </div>
                            <p class="tl-org">Faculty of International Economics, FTU</p>
                            <p class="tl-desc">Assisting the faculty in major events such as Vietnamese Teachers' Day and the 65th & 40th Anniversaries.</p>
                        </div>
                    </div>

                    <div class="timeline-item">
                        <div class="timeline-dot"></div>
                        <div class="timeline-card">
                            <div class="tl-top">
                                <h3 class="tl-title">Store Clerk</h3>
                                <span class="tl-date">2015 - Present</span>
                            </div>
                            <p class="tl-org">Nam Phuong Grocery</p>
                            <p class="tl-desc">Experienced in sales, customer service, bookkeeping, supply chain management, and ensuring monthly revenue targets.</p>
                        </div>
                    </div>'''

if bad_chunk_1 in content:
    content = content.replace(bad_chunk_1, good_chunk_1)
    print("Fixed chunk 1")

bad_chunk_2 = '''                            <div class="achievement-pills">
                                <span class="pill gold">GPA 4.0 Sem 1</span>
                                <span class="pill anemo">Training Score: Excellent</span>
                            </div>'''

good_chunk_2 = '''                            <div class="achievement-pills">
                                <span class="pill gold">GPA 3.63 (Year 1)</span>
                                <span class="pill anemo">GPA 3.74 (Year 2 Sem 1)</span>
                            </div>'''

if bad_chunk_2 in content:
    content = content.replace(bad_chunk_2, good_chunk_2)
    print("Fixed chunk 2")

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(content)
