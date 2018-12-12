# Term-Project

A zombie arcade game built for CMU course 15112 (Fundamentals of Programming)

Project Description

In my project I will make a zombie based game which will be round based, with infinite rounds. Game will end when the player dies. Zombies will move towards the players location. Player dies when contact with a zombie is made. The player will have a limited amount of time between rounds to buy/upgrade weapons and buy bullets. I will also implement a health system for zombies, so different weapons will do different amounts of damage. Each round, the zombies’ health increases, and the number of total zombies also increases. 

Libraries: Pygame

User Interface:
At start-up, there will be a Play, Options, and Exit button. Play will start the game at round 1. Options will give display controls. Exit will exit the game. In-game, I will also have a pause menu, with resume, restart, and end-game options. End-game takes you back to main menu(startup menu), restart will restart the game from round 1, resume will resume from where the game was paused. When you have died, the game will return to start menu. 
The game itself will have the player in the center, with the zombies spawning at certain locations on the map. The map will be an extended image, so as the player moves, the map shifts, keeping the player centered. Bullet lines will be shown as well.
