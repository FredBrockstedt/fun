#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run this script with: ptw -c -w

import numpy as np
# Show the full matrix without truncation
np.set_printoptions(threshold=80)

import pytest


class PaperRolls:
    def __init__(self, elfpuzzle):
        # the elf puzzle in matrix form
        self.basematrix = self.elfpuzzel2matrix(elfpuzzle)

        # helper matrix
        self.addmat = None

        # computation of the helpermatrix
        self.calc()

    def calc(self):
        "Create 8 offset matrizies and add them up"
        # to count the surrounding 8 fields of each spot

        # we don't want to count already empty fields
        # so we add atleast 4 to them
        no_paperroll = self.basematrix.copy()
        no_paperroll[self.basematrix == 0] = 4
        no_paperroll[no_paperroll == 1] = 0

        # add every thing up
        self.addmat = self._shift_north(self.basematrix) \
            + self._shift_south(self.basematrix) \
            + self._shift_east(self.basematrix) \
            + self._shift_west(self.basematrix) \
            + self._shift_north(self._shift_east(self.basematrix)) \
            + self._shift_north(self._shift_west(self.basematrix)) \
            + self._shift_south(self._shift_east(self.basematrix)) \
            + self._shift_south(self._shift_west(self.basematrix)) \
            + no_paperroll
        
    def set(self, matrix):
        "Set the basematrix, required for part 2"
        self.basematrix = matrix.copy()
        self.calc()

    def forklift_reachable(self):
        "Count how many paper rolls are forklift reachable"
        return np.count_nonzero(self.addmat < 4)

    def remove_paperrolls(self):
        "Return a matrix where forklift reachable paper rolls where removed"

        # simulate forklifts by matrix
        forklift = self.addmat.copy()

        # Any elements with less than four paper rolls
        # will be moved away
        forklift[forklift < 4 ] = 1
        
        # everything else stays the same
        forklift[forklift >= 4 ] = 0

        # let the forklifts work
        removed = self.basematrix - forklift
        
        # since these are mathematical forklifts
        # we have to clean up the negative paper rolls
        # they leave behind
        removed[removed < 0] = 0

        return removed
            
    def __str__(self):
        return str(self.basematrix)

    def _shift_north(self, matrix):
        "compute a matrix that is shifted to the north"

        matrix = np.pad(matrix, ((0,  1), (0, 0)), mode='constant')
        matrix = np.delete(matrix, 0, 0)

        return matrix

    def _shift_south(self, matrix):
        "compute a matrix that is shifted to the south"

        matrix = np.pad(matrix, ((1,  0), (0, 0)), mode='constant')
        matrix = np.delete(matrix, matrix.shape[0]-1, 0)

        return matrix

    def _shift_east(self, matrix):
        "compute a matrix that is shifted to the east"

        matrix = np.pad(matrix, ((0,  0), (1, 0)), mode='constant')
        matrix = np.delete(matrix, matrix.shape[1]-1, 1)

        return matrix

    def _shift_west(self, matrix):
        "compute a matrix that is shifted to the west"

        matrix = np.pad(matrix, ((0,  0), (0, 1)), mode='constant')
        matrix = np.delete(matrix, 0, 1)

        return matrix

    def elfpuzzel2matrix(self, elfpuzzle):
        "Turns an elf puzzle into a matrix of 1 and 0"
        return np.array([[1 if ch == '@' else 0 for ch in line.strip()] for line in elfpuzzle])

################################################################################
# pytest

@pytest.fixture
def pr():
    "Paper Roll Puzzle Object"
    elfpuzzle =  ["..@@.@@@@.",
                  "@@@.@.@.@@",
                  "@@@@@.@.@@",
                  "@.@@@@..@.",
                  "@@.@@@@.@@",
                  ".@@@@@@@.@",
                  ".@.@.@.@@@",
                  "@.@@@.@@@@",
                  ".@@@@@@@@.",
                  "@.@.@@@.@."]

    return PaperRolls(elfpuzzle)
    
def test_class():
    pr = PaperRolls("@")

    assert hasattr(pr, 'basematrix')
    assert hasattr(pr, 'addmat')

def test_13places_forklift_reachable(pr):
    assert pr.forklift_reachable() == 13

def test_remove_matrix(pr):
    removemat = pr.remove_paperrolls()
    # assert that after removeing 13 paper rolls from 71
    # we are left with 58 rolls
    assert np.count_nonzero(removemat == 1) == 58

def test_matrixcreation(pr):
    "Load file and convert to NumPy array"
    assert pr.basematrix.shape == (10, 10)

################################################################################
# main
#
# run with: python test_paperroll.py

if __name__ == '__main__':

    with open("data.txt", "r") as f:
        lines = f.readlines()

    pr = PaperRolls(lines)

    print("* Part 1 ")
    print(f"Forklift reachable paper rolls = {pr.forklift_reachable()}")

    print("* Part 2 ")

    tally = 0

    while pr.forklift_reachable() > 0:
        removemat = pr.remove_paperrolls()
        tally += pr.forklift_reachable()
        pr.set(removemat)

    print(f"Removed paper rolls for part 2 = {tally}")
