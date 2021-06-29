# python_chess

This is my simple implementation of text based chess.
## first time set up...
python3 crypto.py 
\# this generates the key for saving a loading

## start the game
python3 game_text.py

## game play
currently only 2 player
select an x and y index of a piece
if there is a piece at selection with at least one valid move
select an x and y destination for the piece
if the piece was chosen in error leave the destination field blank and try again
Normal chess rules are implemented.

## commands
q: Exit the game
n: Start a new game
s: Save current game
l: Load a saved game
r: Redraws the board
h: Show list of available commands

## env
This was created using python 3.8.5 on Ubuntu 20.04

## libraries
numpy
os
random
sys

experimental GUI version does not work at the moment
PIL
PyQt5
threading
