# PythonPong

A simple python pong game running with pygame, with a second version with more gameplay

## Requirements

- A working installation of either python version 2.* or python version 3.*
- The pygame library installed

## Usage

- Run the command "python3 ./ClassicPong.py" for a classic game, or "python3 ./Main.py" in the P.O.N.G folder for an enhanced experience

## Rules of P.O.N.G

- Controls :
	- Left player:
		Up = W
		Down = S
		Use power = D
	- Right player:
		Up = Arrow_up
		Down = Arrow_down
		Use power = Arrow_left

- Powers :
	- Powers spawn randomly one at a time on the game area
	- Hit the power with your ball to obtain the power, you can then use it !
	- Each player can hold one power at a time between three available :
		1. Green :	Reversal
			Change the ball direction to it's opposite
		2. Pink	:	Wall
			Make the middle of the game area a wall, for a short amount of time
		3.	Cyan : Curse
			Curse the other player, making his paddle smaller

- Rules :
	- The game loop indefinitely, the score is a work in progress

## Have fun
