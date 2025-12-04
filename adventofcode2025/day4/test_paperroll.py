#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run this script with: ptw -c -w

import numpy as np
# Show the full matrix without truncation
np.set_printoptions(threshold=80)

import pytest


class PaperRolls:
    def __init__(self, elfpuzzle):
        self.basematrix = self.elfpuzzel2matrix(elfpuzzle)        

        # create 8 offset matrizies
        # to count the sourroundin 8 fields of each spot

        self.north = self._shift_north(self.basematrix)
        self.south = self._shift_south(self.basematrix)
        self.east  = self._shift_east(self.basematrix)
        self.west  = self._shift_west(self.basematrix)

        self.northeast  = self._shift_north(self._shift_east(self.basematrix))
        self.northwest  = self._shift_north(self._shift_west(self.basematrix))
        self.southeast  = self._shift_south(self._shift_east(self.basematrix))
        self.southwest  = self._shift_south(self._shift_west(self.basematrix))

        no_paperroll = self.basematrix
        no_paperroll[self.basematrix == 0] = 4
        no_paperroll[no_paperroll == 1] = 0

        self.addmat = self.north + self.south \
            + self.east + self.west \
            + self.northeast + self.northwest \
            + self.southeast + self.southwest \
            + no_paperroll

    def forklift_reachable(self):
        return np.count_nonzero(self.addmat < 4)

            
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
def elfpuzzle():
    "Elf puzzle "
    return  ["..@@.@@@@.",
             "@@@.@.@.@@",
             "@@@@@.@.@@",
             "@.@@@@..@.",
             "@@.@@@@.@@",
             ".@@@@@@@.@",
             ".@.@.@.@@@",
             "@.@@@.@@@@",
             ".@@@@@@@@.",
             "@.@.@@@.@."]

def test_class():
    pr = PaperRolls("@")

    assert hasattr(pr, 'basematrix')
    assert hasattr(pr, 'north')
    assert hasattr(pr, 'south')
    assert hasattr(pr, 'east')
    assert hasattr(pr, 'west')    

def test_direction_matrixes(elfpuzzle):
    pr = PaperRolls(elfpuzzle)

    print(pr.north)

    # Assert all values are zero
    not np.any(pr.north[-1])

    assert pr.north.shape == (10, 10)
    assert pr.south.shape == (10, 10)
    assert pr.east.shape == (10, 10)
    assert pr.west.shape == (10, 10)

def test_13places_forklift_reachable(elfpuzzle):
    pr = PaperRolls(elfpuzzle)

    assert pr.forklift_reachable() == 13
    #print(pr.addmat)

def test_matrixcreation(elfpuzzle):
    "Load file and convert to NumPy array"

    pr = PaperRolls(elfpuzzle)
    assert pr.basematrix.shape == (10, 10)

################################################################################
# main
if __name__ == '__main__':


    with open("data.txt", "r") as f:
        lines = f.readlines()
        pr = PaperRolls(lines)

        print(f"Forklift reachable paper rolls = {pr.forklift_reachable()}")
