# Board Games
The following is a set of board games implemented in Python, with inbuilt Artificially Intelligent opponents.

The list of currently supported games includes:
- Connect Four

### Playing the games
##### Getting started
- You'll need Python 3.5+

##### Running a game
The scripts to run the games are located in the base directory of the project.
```
python connect_four.py
```

### The AI
The AI players for these games use a single layer neural network to evaluate a board state, and an iterative deepening Alpha-Beta search to plan their moves. The AI code is written in a generic way so that new board games can get an AI player up and running just by implementing:
- `get_legal_moves`
- `apply_move`
- `undo_move`
- `evaluate_board_state`
