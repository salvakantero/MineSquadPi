
================================
RED PLANET Pi v1.0 (C) 2015/2023
================================                
  for Raspberry Pi / Windows *

*and other systems supporting pygame 2.1.2 (SDL 2.0.18, Python 3.9.12) or higher.
 (Windows and Raspberry Pi installers and executables in the /PUB folder)


Lead our hero into the underground of the old space station to blow up the entire complex and wipe out its evil inhabitants.
But beware, the environment is dangerous. Avoid coming into contact with the aliens, and falling into the lava or radioactive waste pits.


ITEMS
=====

EXPLOSIVES: To successfully complete the mission you must obtain the 15 explosives scattered around the station and place them in the explosives depot, deep inside the Martian base.
Once deposited, you must return to the control centre and activate the detonator.

KEY CARD: Sometimes you will have to access locked areas with access cards, so you will have to locate these cards before you can continue your mission.

GATES: You will only be able to open them if you have a card. 
The cards are for single use only, but the door will remain open.

AMMO: You have the possibility to fire plasma bullets at your enemies, but be careful not to waste ammunition, which is scarce.
There are reloads scattered throughout the complex.

OXYGEN: Keep an eye on the condition of your oxygen cylinders and find new ones before they run out or you will die on the spot.

DISKETTE: Save the current game situation to continue the game at another time.
You will be able to locate them on the screens where there were previously cards. 

BURGER, CAKE, DONUT: Yes, Martians like them too. 
Eat them if you want to see your score go up.


ENEMIES
=======

INFECTED: Previous companions who attempted the mission and failed. 
The bite of the arachnoviruses keeps them in an undead state.
They move in a linear fashion and can be very fast. 
Take them out before they infect you.

ARACHNOVIRUS/PELUSOID: Erratic and fast moving.
They usually move through the air. 
They are the most numerous aliens that have colonised the base.

FANTY: They are very intelligent. They can lie low and wait for your arrival.
If they see or hear you, they will pounce on you. 
In that case, finish them off as soon as possible. 


SCORE
=====

INFECTED	 25 points
ARACHNOVIRUS	 50 points
PELUSOID	 75 points
FANTY		100 points
----------------------------
TNT		 50 points
AMMO		 75 points
OXYGEN		100 points
KEYCARD		125 points
GATE		150 points
----------------------------
DONUT		200 points
CAKE		350 points
HAMBURGER	500 points


MAIN MENU
=========

After a short intro or after each game, the main menu is displayed. 
This consists of a screen with the game options and a screen with the configuration options. 
If no key is pressed, sliding pages with the highscore table, help and summary information from this manual are displayed every few seconds.

-In the main menu we can start a new game or continue a previous game from the last floppy disk we took.
We can also change the configuration or exit to the operating system.

-In the configuration menu you can change various features of the programme.
	-The "Full Screen" option allows us to view the game in a window, or in full screen. 
	In addition, there are two options available in full screen.
		-The "4:3" option allows us to enjoy the game occupying the entire screen of a non-widescreen monitor or TV with the correct aspect ratio.
		-If our screen is widescreen we will probably see the game very flattened. To correct this problem we must select the next option, which is "16:9". This option shows the game in the central part of the screen with the correct aspect ratio.
	- "Scanlines" simulates the image provided by ARCADE machines of the time on their tube screens, showing them with visible dark lines.
	- "Map Transition" deactivated shows the new screens immediately. If this option is activated it will show the next screen sliding along with the previous one. It is slower but shows the game map as a whole...
	- "Game Control" ...


GAME CONTROL
============

		GAMER		RETRO		CLASSIC		JOYPAD
		--------------------------------------------------------------------
jump:		W		Q		cur.up	button A / button B / joy.up	
action:		S		A		cur.down	joy.down
left:		A		O		cur.left	joy.left
right:		D		P		cur.right	joy.right
fire*:		SPACE		SPACE		SPACE		button X / button Y	 		
* also left mouse button

Keys common to all configurations:
M: 	Music Yes/No.
ESC:	Pause / Cancel game.


TIPS AND TRICKS
===============

- Reserve some ammunition and oxygen for when you have placed the explosives and returned to the control centre.
In the event of an oxygen shortage, an alarm will sound during which the priority is to search for new cylinders.

- Use extreme caution in the vertical corridors. These are the most treacherous areas.

- Whenever possible, it is best not to disturb the FANTYS.

- Use the save game when the game situation is appropriate, i.e. with enough lives and oxygen to finish the game.
Remember that selecting a DISKETTE overwrites the previous game.

- To place the explosives in their final location and use the detonator, press the ACTION key (below), otherwise nothing will happen.


===================================
RED PLANET Pi  (C) PlayOnRetro 2023
===================================

PROGRAM: salvaKantero
GRAPHICS: salvaKantero
COVER ILLUSTRATION: Masterklown 
MENU MUSIC: Masterklown
IN-GAME MUSIC: Centurion of war
SOUND EFFECTS: Juhani Junkala
16/9 MODE BACKGROUND IMAGE: NASA (Hubble, Dec 2 2022)

BETA TESTERS: Danielito Dorado, Dany Cantero, Laura Cantero, Lucas Cantero, Marina Cantero

RED PLANET Pi is released under GPL v3 for all software components* (see license.txt).
* However, please note that the illustrations used for the cover artwork are NOT released under the GPL v3 license. 
These illustrations are the intellectual property of Masterklown and are subject to separate licensing terms. 
Any use, reproduction, or distribution of the illustrations must be authorized by Masterklown. 

PYTHON SOURCE CODE AND RESOURCES AVAILABLE AT https://github.com/salvakantero/RedPlanetPi

ACKNOWLEDGEMENTS*: 
Mojon Twins (MK1 8bit game engine)
DaFluffyPotato (Font class, screen scaling)
Chris (Clear Code YT channel)
Rik Cross (Raspberry Pi Foundation)
Mark Vanstone (Raspberry Pi Press tutorials)
Ryan Lambie (Raspberry Pi Press tutorials)
Cesar Gomez (Mundo Python YT channel)
Kenney (Keyboard/Mouse Graphics)

* Thanks to all of them for sharing their knowledge, techniques and resources. 


AUTHOR'S NOTE
=============

This project was programmed entirely on Raspberry Pi computers and Python language, thinking about the large number of academies and users who use these computers around the world to learn computer science and programming.
If any of these students or casual gamers, access the source code to study it, improve it, make their own game, or simply review and understand it, then it will have been worth the effort.

