# Hoops — Development Prompts & Plans

A chronological record of the prompts and plans that built this game, from initial concept to polish.

---

## 1. The Original Prompt

> I want to build a game called 'Hoops'. It should be built as a HTML + Javascript app using html canvas that can run as a standalone html in the browser. It is ok to pull in libraries for graphics and animation. For images and graphics, find them on the web. Use collections such as https://ansimuz.itch.io/gothicvania-patreon-collection or whatever works.
>
> It should be a basketball game.
> * one can choose between different basketballs that have different colors, like golden, hot pink, purple, turquoise etc.
> * one can pick how the player looks: girl or boy, jersey with different WNBA and NBA team logos and colors
> * game play: half court game, 3 vs 3. one of your team is controlled by the player, all others are controlled by the computer. first to 20 wins. regular NBA rules, regular basket 2 points, from behind the 3 point line is 3 points. fouling a player shooting gives 2 free throws, otherwise throw in from the sideline.
> * style: go for pixel art. the courts are outdoors in different locations that define the background (like in street fighter), for example Paris with the Eiffeltower, San Francisco with the Golden Gate bridge, Berlin with the Brandenburg Gate, and similar.

---

## 2. Plan Feedback & Modifications

After the initial implementation plan was drafted, the user refined the approach:

> only use chatgpt image generation when you can't find an image on the web, and for special images... swap steps 5 and 6. the player should first select the character, then the ball. add the Golden State Valkyries to the list of teams. change the game controls so that it also works on a touch device (iphone and ipad)... add a help screen explaining controls for each. For verification, please test automatically in Chrome using the claude chrome extension

Key changes from this feedback:
- Asset strategy: prefer web sources, ChatGPT only as fallback
- Menu flow reordered: character select before ball select
- Added Golden State Valkyries (WNBA) to the team roster
- Touch controls required (virtual joystick + buttons)
- Help screen for both keyboard and touch controls
- Testing via Chrome extension (Claude in Chrome MCP)

---

## 3. The Original Implementation Plan

The approved plan had 6 phases with 22 steps:

### Phase 1: Project Setup & Asset Acquisition
- Set up single-file HTML structure with Phaser 3 via CDN
- Generate all pixel art procedurally using Canvas API (balls, players, courts, logos)
- No external sprite files needed

### Phase 2: Menu Screens
- BootScene: generate all textures
- TitleScene: animated title with background cycling
- PlayerCustomizeScene: boy/girl selection + team picker
- BallSelectScene: 6 ball color grid
- CourtSelectScene: preview with city backgrounds

### Phase 3: Core Gameplay
- GameScene: top-down half-court with arcade physics
- Player movement, shooting (hold-to-charge), passing
- Pseudo-3D ball height with shadow

### Phase 4: AI System
- FSM per AI player with roles: guard, wing, big
- Offense: cuts, screens, shooting decisions
- Defense: man-to-man, closeouts, steals

### Phase 5: Rules & Flow
- Scoring: 2pt inside arc, 3pt outside
- 12-second shot clock
- Fouls, free throws, sideline inbounds
- First to 20 wins

### Phase 6: HUD & Polish
- Score display, shot clock, team names
- Sound effects via Web Audio API synthesis
- Game over screen with trophy/sad face
- Portrait mode support for mobile

---

## 4. Game Over Screen Iterations

The game over screen went through several rounds of feedback:

> make the winning team hold a trophy that has the winning team logo on it

> only show the trophy if you win and if you lose show a sad face

> make it so you can see the sad face

> make sure the text does not overlap with the player

---

## 5. Git Setup & README

> can you git commit the initial state. and push to my github, with repo name 'hoops'. make it a private repo for now.

> add a readme with a short description and screenshots of the game and commit and push

> for the team screenshot please use the Warriors instead. also in the game, make it show Warriors and Valkyries first. then commit and push

---

## 6. Background Improvement — Real Photos with Pixel Art Filter

> now make the backgrounds nicer. find real pictures and make them pixel art

### Approved Plan
Create a Python script (`tools/pixelate_backgrounds.py`) that:
1. Downloads real city photos from Unsplash (free, no API key)
2. Applies pixel art filter via Pillow:
   - Crop to 16:9 aspect ratio
   - Boost saturation (1.2-1.3x) and contrast (1.1x)
   - Downscale to 160x90 using LANCZOS (creates pixel blocks)
   - Quantize to 48-64 colors using MEDIANCUT
   - Upscale back to 480x270 with nearest-neighbor (crisp edges)
3. Save 6 PNGs to `assets/backgrounds/`

### Background Refinements

After the initial backgrounds were generated, specific cities were refined:

> I do not see the updated background images in the game. but I see some in the assets/backgrounds folder. also these look a bit too small/too pixelated

*Fixed by reducing `pixel_size` from 6 to 3 and bumping SW cache version.*

> these look nice, but let's improve on some:
> * Tokyo should have that TV tower be more visible. or find a pic of a buzzing street intersection in shibuya or whatever is famous for that. or something with the emperor's park/palace
> * New York should include the Statue of Liberty and the skyline

*Tokyo changed to Shibuya 109 crossing at night. New York changed to Statue of Liberty with Manhattan skyline.*

---

## 7. iPhone Portrait Mode

> on an iphone make sure the game fills the screen in portrait mode. you can verify in Chrome by enabling iphone screen simulation

*Implemented CSS rotation of 90 degrees for touch devices in portrait orientation, with input coordinate remapping.*

---

## 8. Difficulty Selection

> add a difficulty selection screen

*Added Easy vs Hard modes affecting defense speed, steal rates, contest radius, help defense, and pass interception.*

---

## 9. Four Bug Fixes

> create team agents to make these changes:
> * on an iphone 17 pro the ENTER/PLAY button shown at the bottom is not visible and not clickable. similarly the left and right selection buttons. please add some margin on those screens.
> * the app on an iphone (when stored as app using 'add to homescreen') seems to be stuck in an older cached version. we serve it using github pages at https://lonski67.github.io/hoops/. maybe some setting could be done to have it hard refresh
> * the yellow selection box on the boy-girl screen is overlapping with the player pictures. make it go around them
> * the game screen shows some 'F:0' text underneath the team. not sure what it does, please remove

### Approved Plan

**Fix 1: iPhone button visibility**
- Move SELECT/PLAY buttons from y=258 to y=245 (25px margin from bottom instead of 12px)
- Affected scenes: PlayerCustomizeScene, CourtSelectScene

**Fix 2: Remove fouls display**
- Foul counter was cosmetic only (no bonus/foul-out rule implemented)
- Removed `foulsA`/`foulsB` text and their update logic from HUDScene
- Kept underlying foul-tracking logic for potential future use

**Fix 3: Enlarge selection box**
- Changed yellow box from 60x80 at y=120 to 70x110 at y=130
- Now fully surrounds player sprite + label with padding

**Fix 4: PWA auto-update**
- Added `self.skipWaiting()` in install event
- Added `self.clients.claim()` in activate event
- Changed HTML fetch to network-first with cache fallback
- Added `controllerchange` listener that reloads the page
- Added periodic update check every 60 seconds
- Bumped cache from v7 to v8

---

## 10. Project Documentation

> can you please add a CLAUDE.md and MEMORY.md to this repo with the important information from this session and the code

*Created both files with dev workflow instructions, code conventions, Phaser gotchas, project architecture, file map, controls reference, team/court data, and bug history.*

---

## 11. This File

> can you export all the prompts of this conversation, especially the first one, and the original plan, into a nicely formated markdown file into the repo (PROMPTS.md)
