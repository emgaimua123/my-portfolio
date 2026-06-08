# my-portfolio

An immersive, highly interactive personal portfolio website inspired by the aesthetics, user interface, and experience of the game **Genshin Impact**. 

This project aims to deliver a "wow" factor by combining cinematic video transitions, stateful JavaScript animations, and custom UI components to create a journey rather than just a standard webpage.

## ✨ Key Features

- **Cinematic Intro Sequence**: A seamless multi-step entry experience. It starts with a pre-rendered video intro, transitions into an interactive "frozen frame" with dynamic particle effects, and concludes with a door-opening video sequence that leads into the main content.
- **Paimon Companion Guide**: An interactive Paimon assistant located in the navigation bar. Paimon can guide you through the portfolio sections and provides a step-by-step tutorial for new visitors.
- **Integrated Music Player**: A built-in, fully functional media player featuring a tracklist of Genshin Impact OSTs to enhance the atmospheric immersion.
- **Authentic Genshin UI Aesthetics**: Custom styling mirroring the game's interface, including authentic fonts (`hywenhei` / `Genshin Impact DRIP FONT`), custom interactive cursors, and gold-trimmed borders.
- **Immersive Visual Effects**: Features continuous background animations like floating dandelions, reactive mouse trails, and dynamic vignette/flash screen transitions.
- **Responsive Design**: Designed primarily for desktop viewing, with a dedicated landscape orientation mode enforced for mobile and tablet users to ensure the UI is experienced exactly as intended.

## 📂 Project Structure

- `index.html`: The core application file containing all the HTML structure, CSS stylesheets, and vanilla JavaScript logic handling the state machines and animations.
- `content/`: Contains all core assets including fonts, custom cursors, avatar images, UI icons, and document files (PDF/DOCX CVs).
- `intro/`: Houses the heavy media files for the cinematic entry sequence (intro videos, door opening videos, and sound effects).
- `music/`: Contains all the `.mp3` audio tracks utilized by the interactive Music Player.

## 🚀 Live Demo & How to Run

**🌍 Experience the live website here:** [https://emgaimua123.github.io/my-portfolio/](https://emgaimua123.github.io/my-portfolio/)

Alternatively, to run the project locally:
1. **Clone or Download** this repository to your local machine.
2. **Open `index.html`** in any modern web browser (Chrome, Edge, Firefox, Safari).
3. *(Optional but Recommended)*: Serve the directory using a local web server (like VS Code's "Live Server" extension) to prevent any strict browser security policies from blocking local media autoplay.

## 🛠️ Technologies Used

- **HTML5**: Semantic structure and `<video>`/`<audio>` media elements.
- **CSS3**: Advanced styling, flexbox/grid layouts, keyframe animations, media queries, and custom fonts.
- **Vanilla JavaScript (ES6)**: DOM manipulation, event listeners, HTML5 Canvas for particle rendering, custom audio/video playback control, and state management for scene transitions.

---
*Created with ❤️ by Bui Tuan Phuong.*
