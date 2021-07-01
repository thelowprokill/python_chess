# python_chess

This is my simple implementation of text based chess.
## first time set up...
python3 crypto.py 
\# this generates the key for saving a loading

## start the game
python3 game_text.py<br />
or<br />
python3 game_gui.py

## game play text
currently only 2 player<br />
select an x and y index of a piece<br />
if there is a piece at selection with at least one valid move<br />
select an x and y destination for the piece<br />
a list of legal moves for that piece is provided<br />
if the piece was chosen in error leave the destination field blank and try again<br />
Normal chess rules are implemented.<br />

## game play gui
select a piece with the mouse.<br />
selected piece is has a green boarder.<br />
available moves have a blue boarder.<br />
opponents previous move has a purple boarder.<br />
pieces that have no legal move cannot be selected.<br />

## commands
q: Exit the game<br />
n: Start a new game<br />
s: Save current game<br />
l: Load a saved game<br />
r: Redraws the board<br />
m: Main Menu<br />
h: Show list of available commands<br />

## env
This was created using python 3.8.5 on Ubuntu 20.04

## libraries
numpy<br />
os<br />
random<br />
sys<br />
<br />
experimental GUI version does not work at the moment<br />
PIL<br />
PyQt5<br />
threading<br />
