# Gomoku
# Gomoku Starter Code
# Authors: Anthony Salgado & Harry Nguyen
# Date Completed: November 13, 2022

This repository contains a basic implementation of Gomoku (Five in a Row). It includes various functions to handle board manipulation, move detection, scoring, and game analysis.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)


## Introduction

Gomoku is a strategy board game where the objective is to align five consecutive stones on a grid. This code provides a framework to implement a playable version of Gomoku, where the computer makes intelligent moves, and players can analyze game states.

## Features

- Functions to check board status (e.g., if it's full or empty).
- Functions to detect sequences of stones and check if a player has won.
- Basic AI that makes the computer select optimal moves.
- A play loop that allows a user to compete against the computer.
- Analysis tools to count the number of open and semi-open sequences for both black and white stones.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/gomoku-starter.git
cd gomoku-starter

2. Ensure you have Python installed on your system (version 3.x recommended).

3. Run the Python script:

python gomoku.py

No external libraries are required for this project.

Usage

1. Launch the game using the provided play_gomoku function:

from gomoku import play_gomoku

play_gomoku(board_size=8)

During the game:

  - The computer will move first.

  - You'll be prompted to enter your move by specifying the x and y coordinates.

  - The game continues until one player wins or the board is full (resulting in a draw).

*0|1|2|3|4|5|6|7*
0 | | | | |w|b| *
1 | | | | | | | *
2 | | | | | | | *
3 | | | | |b| | *
4 | | | |b| | | *
5 | |w|b| | | | *
6 | |w| | | | | *
7 | |w| | | | | *
*****************
Your move:
y coord: 3
x coord: 5

3. The game will display the current board after each move and show the number of open and semi-open rows for each player.

Tests

Run the provided test cases to ensure the code functions correctly. You can run the tests in the easy_testset_for_main_functions function, which will verify key parts of the code.

To run the test cases:

from gomoku import easy_testset_for_main_functions

easy_testset_for_main_functions()

Test Functions:

  - test_is_empty(): Verifies if the board is correctly identified as empty.

  - test_is_bounded(): Tests if sequences are correctly detected as open, semi-open, or closed.

  - test_detect_row(): Checks if the function detects individual rows accurately.

  - test_detect_rows(): Tests row detection across the board for a specific color.

  - test_search_max(): Ensures the AI correctly picks the optimal move.
