# Spoilers ahead!

# Advent of Code 2025 Solutions

Advent of Code is an Advent calendar of small programming puzzles for a variety 
of skill levels that can be solved in any programming language you like. People 
use them as interview prep, company training, university coursework, practice 
problems, a speed contest, or to challenge each other.

You can find it [here](https://adventofcode.com/2025).

## Getting started

At the moment I like to use the [uv](https://pypi.org/project/uv/) utility to manage python dependencies.

The quickest way to get the code running is by

Cloning the repository

	git clone git@github.com:FredBrockstedt/fun.git
	cd fun/adventofcode2025

Syncing the project dependencies with uv. You can also use make dependencies

	uv sync

Activate the virtual environment

	source .venv/bin/activate

Test driven is my preferred approch to problem solving, so the constant feedback from pytest-watch is very helpful for me.

	cd day1-12
	ptw -c -w

Good luck!
