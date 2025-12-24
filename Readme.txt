=============================
 Mine Squad Pi v1.0 (C) 2025
=============================
For Raspberry Pi / Windows *

*and other systems compatible with python/pygame.
*(Compiled program for Windows, Linux and Raspberry Pi in the "/dist" folder)


You are part of an elite sapper squad during the Second World War. 
Your mission: Defuse all minefields located across three crucial battle fronts without triggering any mines. 
Use your wits and numerical clues to locate hidden mines, mark them with beacons, and clear each sector to advance.


CHARACTERS
==========

At the start of the game you can choose between two members of the sapper squad:
BLAZE: Veteran sergeant, expert in explosive ordnance disposal.
PIPER: Non-commissioned officer, specialist in hazardous terrain reconnaissance.


SCENARIOS
=========

The game takes place across three scenarios from historical Second World War operations, each with 3 levels of increasing difficulty:

BATTLE OF EL ALAMEIN (Egypt - October 1942)
-------------------------------------------
Hostile North African desert during the Allied offensive.
Enemies: Scorpions, snakes, Afrika Korps soldiers.
Obstacles: Cacti that cause damage on contact.

D-DAY INVASION (Normandy - June 1944)
-------------------------------------
Normandy beaches during the historic Allied landing.
Enemies: Crabs, enemy projectiles, German soldiers.
Obstacles: Anti-tank barriers that cause injuries.

BATTLE OF THE BULGE (Belgium - January 1945)
--------------------------------------------
Snow-covered forest during the German winter offensive.
Enemies: Skiers, wild boars, mountain soldiers.
Obstacles: Semi-buried clamps.


GAME MECHANICS
==============

The battlefield is a rectangular grid of 30x40 cells. 
Some cells contain hidden mines that you must locate without stepping on them.

As you move across the terrain, adjacent cells reveal information:
- If there is no mine, a NUMBER appears indicating how many mines are in the 8 surrounding cells.
- If there is a mine, you will step on it and lose vital energy.

Your objective is to mark ALL mines with beacons to complete the level.

WARNING: The number of beacons is limited. At higher levels, more mines. 
Use minesweeper logic to deduce where the mines are before placing your beacons.


ITEMS AND POWER-UPS
===================

BEACON/FLAG: Use it on a cell you believe contains a mine. Beacons are limited.
Beacons placed incorrectly on a cell without a mine will turn reddish.
The level is completed when all mines are correctly marked.
You can see the number of remaining beacons/mines on the scoreboard at all times.

POWER-UPS:

EXTRA LIFE: Completely refills your energy bar.

SHIELD: Makes you invincible for 30 seconds. Take advantage to explore dangerous areas. 
If you step on a mine, it will hurt less!

AMMUNITION: Allows you to shoot at enemies (+10 bullets per reload).

BEACON PACK: 5 additional beacons.

SCORING ITEMS*:

SWEET:       50 points
APPLE:       75 points
CHOCOLATE:  100 points
COIN:       200 points

*These items appear at random positions. Two items per map. 
When collected, another is immediately generated at a different location. Lower value items appear more frequently.
Energy is increased by +1 unit.


ENEMIES
=======

Enemies patrol the battlefield and represent a constant threat. 
Some move linearly, others erratically, and the most dangerous ones chase you when you're nearby.
Their number, speed, and resistance increase with each level.

LEVEL 1-3: EL ALAMEIN (Desert)
------------------------------
SCORPION:        Linear movement       10 points   1 life
SNAKE:           Random movement       20 points   1 life
BROWN SOLDIER:   Chases player         50 points   2 lives

LEVEL 4-6: NORMANDY (Beach)
---------------------------
PROJECTILE:      Linear movement       20 points   2 lives
CRAB:            Random movement       40 points   2 lives
GREY SOLDIER:    Chases player        100 points   3 lives

LEVEL 7-9: ARDENNES (Snowy Forest)
----------------------------------
SKIER:           Linear movement       40 points   2 lives
WILD BOAR:       Random movement       80 points   3 lives
WHITE SOLDIER:   Chases player        200 points   4 lives

DEADLY OBSTACLES:
Cacti, clamps, and anti-tank barriers are terrain obstacles you can traverse, but they will cause damage when doing so.


DIFFICULTY
==========

At the start of each game you can choose between three difficulty levels:

EASY:   Slow player, with full energy available.
NORMAL: Balance between speed and available energy for the player.
HARD:   Faster player and less resistant.


MAIN MENU
=========

If no key is pressed, the menu automatically displays pages with:
  - High score table
  - Summary help
  - Game information

In the game menu you can:
  - Start a new game
  - Select character (BLAZE or PIPER)
    - Choose difficulty level
  - Exit the game

In the settings menu you can adjust:
  - WINDOWED: Play in windowed mode.
  - 4:3: Full screen for traditional monitors.*
  - 16:9: Full screen for widescreen monitors. (centred play area without squashing) *
  *only available on Windows.

SCANLINES:
  Simulates the effect of CRT screens from classic arcade machines.

GAME CONTROL:
  Select your preferred control scheme (see following section).


GAME CONTROLS
=============

            GAMER       RETRO       CLASSIC       JOYPAD
            --------------------------------------------------
up:         W           Q           cursor up     joy up
down:       S           A           cursor down   joy down
left:       A           O           cursor left   joy left
right:      D           P           cursor right  joy right
beacon:     B ,         B ,         B ,           L / R button
shoot:      SPACE       SPACE       SPACE         X / Y button

MOUSE:
You can shoot with the left mouse button.
You can place beacons with the right mouse button.

Keys common to all configurations:
M:      Music On/Off.
ESC:    Pause / Cancel game.

IMPORTANT: A short press to move faces the player towards the cell corresponding to the pressed key, but no movement occurs.
Use this system to place beacons without stepping on the mine.


TIPS AND TRICKS
===============

- Use minesweeper logic: if a cell shows "1" and there is only one unrevealed adjacent cell, that cell definitely contains a mine.

- Beacons are limited. Don't waste them by marking cells at random. Deduce the exact location of mines using the numbers.

- Eliminate enemies when they are a threat, but prioritise revealing safe cells and marking mines.

- The invincibility shield is ideal for exploring areas with many enemies or chasing enemies.

- Avoid terrain obstacles (cacti, clamps, etc.) whenever possible, as they reduce energy.

- In advanced levels, chasing enemies are very dangerous. Eliminate them before they corner you.

- Each scenario has different enemies. Learn their movement patterns to anticipate them.


===================================
Mine Squad Pi  (C) PlayOnRetro 2025
===================================

PROGRAMMING: salvaKantero
GRAPHICS: salvaKantero
MENU MUSIC: SigmaMusicArt
IN-GAME MUSIC: 
  Spring Spring:
    - "Never Ceasing Militarism"
    - "March"
    - "National March of Quan and Raiku"
    - "Some militaristic tune"
  Jonathan Shaw:
    - "The Tread of War"
    - "Market on the Sea"
    - "Cant Stop Winning"
  Otto Halmen:
    - "Thunderchild"
  HitCtrl:
    - "RPG title"
  TheMightyRager:
    - "Ashen"
  Beau Buckley:
    - "Battle"
  Umplix:
    - "Game Over"
SOUND EFFECTS: Juhani Junkala
BETA TESTING: lou_314

ACKNOWLEDGEMENTS*: 
DaFluffyPotato (Font class, screen scaling)
Chris (Clear Code YT channel)
Rik Cross (Raspberry Pi Foundation)
Mark Vanstone (Raspberry Pi Press Tutorials)
Ryan Lambie (Raspberry Pi Press Tutorials)
Cesar Gomez (Mundo Python YT channel)
Kenney (keyboard/mouse graphics)

* Thanks to all of them for sharing their knowledge, techniques, and resources 

PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/MineSquadPi
Mine Squad Pi is published under GPL v3 licence. (see license.txt)
