import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

ids_to_check = [
    'bg-music', 'btn-hide-player', 'btn-next', 'btn-play-pause', 'btn-prev',
    'btn-repeat', 'btn-shuffle', 'cert-modal', 'cert-modal-img',
    'close-modal-btn', 'dandelion-container', 'door-ambient', 'door-audio',
    'door-scene', 'door-vid', 'icon-pause', 'icon-play', 'intro-ambient',
    'intro-audio', 'intro-scene', 'intro-vid', 'intro-wrapper', 'main-scene',
    'music-backdrop', 'music-btn', 'paimon-action', 'paimon-avatar',
    'paimon-close', 'paimon-guide', 'paimon-text', 'paimon-toggle-btn',
    'particles-canvas', 'player-time', 'player-title', 'progress-bar',
    'quest-toast', 'start-screen', 'track-list', 'tracklist-container',
    'tutorial-overlay', 'unlock-modal', 'vignette', 'white-flash'
]

missing = []
for expected_id in ids_to_check:
    # Look for id="expected_id"
    if f'id="{expected_id}"' not in content and f"id='{expected_id}'" not in content:
        missing.append(expected_id)

if missing:
    print("MISSING IDs:", missing)
else:
    print("ALL IDs FOUND!")
