
=============================
 Mine Squad Pi v1.0 (C) 2025
=============================
For Raspberry Pi / Windows *

* and other systems compatible with pygame 2.6.1 (SDL 2.28.4, Python 3.13.6) or higher.
  (Windows and Raspberry Pi installers and executables in the /PUB folder)


Join an elite squad of sappers in the Second World War.
Your mission: defuse all minefields across three crucial battlefronts without triggering a single mine.
Use your wits and numerical clues to locate hidden mines, mark them with beacons, and clear each sector to advance.


CHARACTERS
==========

At the start of the game you can choose between two members of the sapper squad:
BLAZE: Veteran sergeant, expert in Explosive Ordnance Disposal.
PIPER: Non-commissioned officer, specialist in reconnaissance across dangerous terrain.


SCENARIOS
=========

The game takes place across three historical Second World War theatres of operations, each with 3 levels of increasing difficulty:

BATTLE OF EL ALAMEIN (Egypt – October 1942)
-------------------------------------------
Hostile North African desert during the Allied offensive.
Enemies: Scorpions, snakes, Afrika Korps troops.
Obstacles: Cacti that cause damage on contact.

D-DAY INVASION (Normandy – June 1944)
-------------------------------------
Normandy beaches during the historic Allied landings.
Enemies: Crabs, enemy projectiles, German soldiers.
Obstacles: Barbed wire that causes injury.

BATTLE OF THE BULGE (Belgium – January 1945)
--------------------------------------------
Snowy forest during the German winter offensive.
Enemies: Skiers, boars, mountain soldiers.
Obstacles: Hidden traps that cause injury.


GAME MECHANICS
==============

The battlefield is a rectangular grid of 30×40 cells.
Some cells contain hidden mines that you must locate without stepping on them.

As you move across the terrain, adjacent cells reveal information:
- If there’s no mine, a NUMBER appears indicating how many mines are in the 8 surrounding cells.
- If there’s a mine, you’ll step on it and lose health.

Your objective is to mark ALL mines with beacons to complete the level.

WARNING: The number of beacons is limited. At higher levels, there are more mines and fewer beacons available. Use minesweeper logic to deduce where the mines are before placing your beacons.


OBJECTS AND POWER-UPS
=====================

BEACON/FLAG: Place it on a cell you believe contains a mine. Beacons are limited.
The level is completed when all mines are correctly marked.
The number of remaining beacons/mines can be seen on the scoreboard at all times.

POWER-UPS:

EXTRA LIFE: Completely refills your health bar.

SHIELD: Makes you invincible for 30 seconds. Use this to explore dangerous zones.

AMMUNITION: Allows you to shoot at enemies (+10 bullets per reload).

SCORING OBJECTS*:

SWEET:       50 points
APPLE:       75 points
CHOCOLATE:  100 points
COIN:       200 points

*These objects appear randomly across the map. When collected, another is immediately generated at a different location. Lower-value items appear more frequently.


ENEMIES
=======

Enemies patrol the battlefield and represent a constant threat. Some move linearly, others erratically, and the most dangerous ones will pursue you.

Their number, speed and resistance increase with each level.

LEVEL 1-3: EL ALAMEIN (Desert)
------------------------------
SCORPION:        Linear movement       10 points    1 life
SNAKE:           Random movement       20 points    1 life
BROWN SOLDIER:   Chases the player     50 points    2 lives

LEVEL 4-6: NORMANDY (Beach)
---------------------------
PROJECTILE:      Linear movement       20 points    2 lives
CRAB:            Random movement       40 points    2 lives
GREY SOLDIER:    Chases the player    100 points    3 lives

LEVEL 7-9: ARDENNES (Snowy Forest)
----------------------------------
SKIER:           Linear movement       40 points    2 lives
BOAR:            Random movement       80 points    3 lives
WHITE SOLDIER:   Chases the player    200 points    4 lives

DEADLY OBSTACLES:
Cacti, barbed wire and traps are terrain obstacles that can be traversed, but will cause damage when doing so.


DIFFICULTY
==========

At the start of each game you can choose between three difficulty levels:

EASY:   Slower player, with full health available.
NORMAL: Balanced speed and health.
HARD:   Faster player, but less resistant.


MAIN MENU
=========

If no key is pressed, the menu automatically cycles through pages showing:
- High score table
- Brief help
- Game information

In the game menu you can:
- Start a new game
- Select character (BLAZE or PIPER)
- Choose difficulty level
- View high scores
- Exit the game

In the configuration menu you can adjust:

FULL SCREEN:
  - WINDOWED: Play in a window.
  - 4:3: Full screen for traditional monitors.
  - 16:9: Full screen for widescreen monitors (the game area appears centred without stretching).

SCANLINES:
  Simulates the look of classic arcade CRT screens.

GAME CONTROL:
  Select your preferred control scheme (see next section).


GAME CONTROL
============

            GAMER       RETRO       CLASSIC       JOYPAD
            --------------------------------------------------
up:         W           Q           cursor up     joy.up
down:       S           A           cursor down   joy.down
left:       A           O           cursor left   joy.left
right:      D           P           cursor right  joy.right
beacon:     B ,         B ,         B ,           L / R button
fire:       SPACE       SPACE       SPACE         X / Y button

MOUSE:
You can fire with the left mouse button.
You can place beacons with the right mouse button.

Keys common to all configurations:
M:      Music On/Off.
ESC:    Pause / Cancel game.

IMPORTANT: A short press makes the player face the cell corresponding to the key pressed, but does not move them.
Use this feature to place beacons without stepping on a mine.


TIPS AND TRICKS
===============

- Use minesweeper logic: if a cell shows “1” and there’s only one unrevealed adjacent cell, that cell definitely contains a mine.

- Beacons are limited. Don’t waste them marking cells at random. Deduce the exact location of mines using the numbers.

- Eliminate enemies when they pose a threat, but prioritise revealing safe cells and marking mines.

- The invincibility shield is ideal for exploring zones with many enemies.

- Avoid terrain obstacles (cacti, barbed wire, traps) whenever possible, as they reduce your health.

- At higher levels, pursuing enemies become very dangerous. Eliminate them before they corner you.

- Each scenario has different enemies. Learn their movement patterns to anticipate them.

- If you run out of beacons but there are still unmarked mines, the game ends. Plan carefully before placing them.


===================================
Mine Squad Pi  (C) PlayOnRetro 2025
===================================

PROGRAMME: salvaKantero
GRAPHICS: salvaKantero
MENU MUSIC: SigmaMusicArt
IN-GAME MUSIC:
  Spring Spring:
    - "Never Ceasing Militarism"
    - "March"
    - "National March of Quan and Raiku"
    - "Some Militaristic Tune"
  Jonathan Shaw:
    - "The Tread of War"
    - "Market on the Sea"
    - "Can’t Stop Winning"
  Otto Halmen:
    - "Thunderchild"
  HitCtrl:
    - "RPG Title"
  TheMightyRager:
    - "Ashen"
  Beau Buckley:
    - "Battle"
  Umplix:
    - "Game Over"
SOUND EFFECTS: Juhani Junkala
BETA TESTING: Luna_314

ACKNOWLEDGEMENTS*:
DaFluffyPotato (Font class, screen scaling)
Chris (Clear Code YT channel)
Rik Cross (Raspberry Pi Foundation)
Mark Vanstone (Raspberry Pi Press tutorials)
Ryan Lambie (Raspberry Pi Press tutorials)
Cesar Gomez (Mundo Python YT channel)
Kenney (keyboard/mouse graphics)

* Thanks to all of them for sharing their knowledge, techniques and resources.

PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/MineSquadPi
Mine Squad Pi is published under the GPL v3 licence. (see licence.txt)
