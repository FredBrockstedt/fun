#!/usr/bin/env python
# -*- coding: utf-8 -*-

# run this script with: ptw -c -w

import pytest
import re

class Cafeteria:
    "See https://adventofcode.com/2025/day/5"

    def __init__(self):
        """
        Setup the cafeteria
        """
        self.freshids = list() # IDs that are considered to be fresh

    def add_freshid(self, start, end):
        """
        Add a range of fresh ids

        Args:
            start: Start of the range of fresh ids
            end:   The end of the range of fresh ids
        """
        self.freshids.append(range(start, end+1))

    def isfresh(self, ingredient):
        """
        Is the ingredient fresh?

        Args:
            ingredient (int): The id of the ingredient

        Returns:
            True: The ingredient is fresh
            False: The ingredient has expired
        """
        for ran in self.freshids:
            if ingredient in ran:
                return True

        return False

    def parse_range(self, ingredients):
        """
        Parse a string of ingredients 

        Args:
            ingredients (str): Something like "1-10"

        Returns:
            start (int), end (int): The start aka 1 and the end aka 10
       
        """
        start, end = ingredients.split("-")
        return int(start), int(end)
        
@pytest.fixture
def caf():
    return Cafeteria()

def test_isfresh(caf):
    caf.add_freshid(1, 10)
    assert caf.isfresh(3)
    assert caf.isfresh(1)
    not caf.isfresh(11)

def test_parse_range(caf):
    assert (1, 10) == caf.parse_range("1-10")


def test_example(caf):
    lines = """
    3-5
    10-14
    16-20
    12-18
    
    1
    5
    8
    11
    17
    32
    """

    freshcount = 0

    for line in lines.splitlines():
        line = line.lstrip(' ')

        if "-" in line:
            start, end = caf.parse_range(line)
            caf.add_freshid(start, end)

        if line.isdigit():
            if caf.isfresh(int(line)):
                freshcount += 1

    # This example, 3 of the available ingredient IDs are fresh.
    assert freshcount == 3

    # Ingredient ID 1 is spoiled because it does not fall into any range.
    not caf.isfresh(1)

    # Ingredient ID 5 is fresh because it falls into range 3-5.
    assert caf.isfresh(5)

    # Ingredient ID 8 is spoiled.
    not caf.isfresh(8)

    # Ingredient ID 11 is fresh because it falls into range 10-14.
    assert caf.isfresh(11)

    # Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
    assert caf.isfresh(17)

    # Ingredient ID 32 is spoiled.
    not caf.isfresh(32)

def main():

    caf = Cafeteria()
    freshcount = 0

    print("* Part 1")
    with open("data.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip("\n")

        if "-" in line:
            start, end = caf.parse_range(line)
            caf.add_freshid(start, end)

        if line.isdigit():
            if caf.isfresh(int(line)):
                print(line, "is fresh")
                freshcount += 1
            else:
                print(line, "is spoiled")

    print(f"Freshcount: {freshcount}")

    
if __name__ == '__main__':
    main()
