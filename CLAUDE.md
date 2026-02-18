# Hoops - Claude Code Instructions

## Dev Workflow
- Local server: `python3 -m http.server 8080` from project root
- Test at `http://localhost:8080`
- After changing assets or code, bump `CACHE_NAME` in `sw.js` (e.g. `hoops-v8` -> `hoops-v9`)
- Clear stale SW in browser: `navigator.serviceWorker.getRegistrations().then(r => r.forEach(reg => reg.unregister())); caches.keys().then(keys => keys.forEach(k => caches.delete(k)));`
- Hosted on GitHub Pages: https://lonski67.github.io/hoops/

## Code Conventions
- Single-file game: everything lives in `index.html` (~2600 lines)
- Code is organized into numbered SECTION comments (1-12)
- All assets are procedurally generated via Canvas API in BootScene — no external sprite files
- Backgrounds are real photos with pixel art filter applied (see `tools/pixelate_backgrounds.py`)
- Sound is synthesized via Web Audio API — no audio files
- Use `GAME_W` (480) and `GAME_H` (270) constants, never hardcode resolution

## Phaser Gotchas
- `generateTexture` from Graphics doesn't auto-create frame data — must use `tex.add(frameIndex, ...)` manually for spritesheets
- `Phaser.Input.Keyboard.JustDown/JustUp` requires actual DOM keyboard events, can't be simulated by setting `isDown`
- Chrome extension can't screenshot `file://` URLs — always use local HTTP server
- Service worker is cache-first for assets, network-first for HTML — always bump cache version after changes

## Important Constraints
- Internal resolution is 480x270 with `pixelArt: true` and `Phaser.Scale.FIT`
- Keep UI elements at least 25px from bottom edge (y <= 245) for iPhone safe area
- Touch controls (joystick + buttons) only render on touch devices (`GameState.isTouchDevice`)
- Portrait mode auto-rotates canvas 90 degrees on touch devices
