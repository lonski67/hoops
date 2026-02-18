# Hoops - Project Memory

## Overview
Pixel-art 3v3 street basketball game built with Phaser 3. Single-file (`index.html`), all assets procedurally generated, runs as a PWA.

## Project Structure
```
index.html          - Entire game (~2600 lines, 12 sections)
sw.js               - Service worker (cache-first assets, network-first HTML)
manifest.json       - PWA manifest (fullscreen, any orientation)
icon-*.png          - App icons (180, 192, 512)
assets/backgrounds/ - 6 pixelated real-photo city backgrounds (PNG)
tools/pixelate_backgrounds.py - Downloads photos from Unsplash, applies pixel art filter
screenshots/        - App store screenshots
```

## Code Sections (index.html)
| Section | Lines | Content |
|---------|-------|---------|
| 1 | ~34-115 | Constants: GAME_W/H, BALL_COLORS, TEAMS, COURTS, COURT geometry, DIFFICULTY |
| 2 | ~116-137 | GameState object (scores, possession, phase, settings) |
| 3 | ~138-348 | Procedural asset generation (balls, players, courts, logos, team textures) |
| 4 | ~349-411 | Sound synthesizer (Web Audio API, no files) |
| 5 | ~412-715 | AI system (FSM: guard/wing/big roles, offense/defense behaviors) |
| 6 | ~716-1172 | Menu scenes (Boot, Title, Help, PlayerCustomize, BallSelect, CourtSelect, Difficulty) |
| 7 | ~1262-2057 | GameScene (main gameplay, physics, shooting, passing, fouls, shot clock) |
| 8 | ~2058-2101 | HUDScene (scores, team names, shot clock) |
| 9 | ~2102-2211 | FreeThrowScene (timing-based free throw minigame) |
| 10 | ~2212-2462 | GameOverScene (final score, rematch, replay animation) |
| 11 | ~2463-2494 | Phaser config (480x270, pixelArt, arcade physics, scene list) |
| 12 | ~2496-2630 | Portrait mode support + SW registration |

## Game Flow
TitleScene -> PlayerCustomizeScene (boy/girl + team) -> BallSelectScene -> CourtSelectScene -> DifficultyScene (easy/hard) -> GameScene + HUDScene -> GameOverScene

## Controls
### Keyboard
- Arrow Keys / WASD - Move
- SPACE - Shoot (hold to charge)
- X - Pass
- Z - Switch player
- C - Steal (defense)
- SHIFT - Sprint
- ENTER - Confirm / ESC - Back

### Touch
- Virtual joystick (left) - Move
- SHOOT button (right) - Hold & release
- PASS button - Pass
- A button - Tap to switch, hold to steal

## Teams (13)
- **NBA (6):** Warriors, Lakers, Celtics, Bulls, Heat, Nets
- **WNBA (7):** Valkyries, Aces, Storm, Liberty, Sun, Lynx, Mercury
- Opponent is always picked from opposite league to ensure visual contrast

## Courts (6)
Paris, San Francisco, Berlin, Tokyo, Rio, New York — each with unique court color and paint color

## Backgrounds
Real photos from Unsplash with pixel art filter applied via `tools/pixelate_backgrounds.py`:
- Pipeline: download -> crop to 16:9 -> boost saturation/contrast -> downscale to 160x90 -> quantize to 48-64 colors -> nearest-neighbor upscale to 480x270
- `pixel_size: 3`, `num_colors: 48-64`, `saturation: 1.2-1.3`

## Key Technical Details
- **Resolution:** 480x270 internal, scaled with `Phaser.Scale.FIT` + `CENTER_BOTH`
- **Physics:** Arcade physics, top-down perspective with pseudo-3D ball height (zHeight + shadow)
- **AI:** Simple FSM per player with roles (guard, wing, big). Behaviors: chase ball handler, guard assigned man, offensive cuts, shooting decisions
- **Difficulty:** Easy vs Hard affects defense speed, steal rate, contest radius, help defense, pass interception
- **Game rules:** First to 20 wins, 2pts inside three-point arc, 3pts outside, 12-second shot clock
- **Fouls:** Tracked per team but no foul limit/bonus — shooting fouls give free throws, non-shooting fouls give sideline inbound
- **PWA:** Service worker with skipWaiting + clients.claim, network-first for HTML, 60-second update check interval, controllerchange reload

## Bugs Found & Fixed
- Opponent gender was same as player (`gender === 'boy' ? 'boy' : 'girl'` bug) — fixed to use opposite
- Ball didn't follow holder during CHECK_BALL phase — added ball tracking outside LIVE_PLAY
- Ball started at (0,0) — fixed to start at controlled player position
- AI players clustered near basket — adjusted offensive spots and cut targets
- Court select title overlapped preview — reduced preview scale from 0.8 to 0.65
- Opponent team picked too similar visually — changed to pick from opposite league
- Backgrounds not updating due to SW cache — bump CACHE_NAME + clear caches
- Bottom UI buttons clipped on iPhone — moved from y=258 to y=245
- Yellow selection box overlapping sprites — enlarged from 60x80 to 70x110
