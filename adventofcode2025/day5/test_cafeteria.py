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
        self.freshcount = 0 # how many fresh ids are there

    def add_freshid(self, start, end):
        """
        Add a range of fresh ids

        Args:
            start: Start of the range of fresh ids
            end:   The end of the range of fresh ids
        """
        # is the start already included?
        if self.isfresh(start):
            # find what range the ingredient was in
            idx = self.get_range_index(start)

            oldstart, oldend = self.freshids[idx]
            
            # expand the old range
            if oldend < end:
                # don't touch any other ranges
                if self.isfresh(end):
                    a, b = self.get_range(end)
                    end = a - 1
                
                self.freshids[idx] = (oldstart, end)

        # is the end already listed?
        elif self.isfresh(end):
            ## find what range the ingredient was in
            idx = self.get_range_index(end)

            oldstart, oldend = self.freshids[idx]
            
            # expand the old range
            if start < oldstart:
                self.freshids[idx] = (start, oldend)


        # Is it a completly new range?
        else:
            # Maybe not?
            for oldstart, oldend in self.freshids:
                if start <= oldstart <= end and start <= oldend <= end:
                    print("* DEBUG: smaller ranger exists")
                    self.freshids.remove((oldstart, oldend))

            self.freshids.append((start, end))

    def isfresh(self, ingredient):
        """
        Is the ingredient fresh?

        Args:
            ingredient (int): The id of the ingredient

        Returns:
            True: The ingredient is fresh
            False: The ingredient has expired
        """
        for start, end in self.freshids:
            if start <= ingredient and ingredient <= end:
                return True

        return False

    def get_range(self, ingredient):
        "Return the range that includes the ingredient"
        for start, end in self.freshids:
            if start <= ingredient and ingredient <= end:
                return (start, end)

    def get_range_index(self, ingredient):
        "Return the index of the range that includes the ingredient"
        for idx, ran in enumerate(self.freshids):
            start, end = ran
            if start <= ingredient and ingredient <= end:
                return idx
    
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

    def count(self):
        """
        Count fresh ids

        Returns:
            count (int): Exact amount of fresh ids
        """
        count = 0

        for start, end in self.freshids:
            count += (end - start) + 1
            print(f"{end - start} += {end} - {start}")

        return count

    def load_file(self, filepath):
        """
        Load data from a file located at filepath
        """
        with open(filepath, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip("\n")

            if "-" in line:
                start, end = self.parse_range(line)
                self.add_freshid(start, end)

            if line.isdigit():
                if self.isfresh(int(line)):
                    self.freshcount += 1
        
@pytest.fixture
def caf():
    return Cafeteria()

def test_double_overlap(caf):
    caf.add_freshid(1, 3)
    caf.add_freshid(7, 10)
    caf.add_freshid(2, 8)
    
    assert len(caf.freshids) == 2

    assert caf.freshids[0][0] == 1
    assert caf.freshids[0][1] == 6
    assert caf.freshids[1][0] == 7
    assert caf.freshids[1][1] == 10

    assert caf.count() == 10

def test_get_range(caf):
    caf.add_freshid(1, 10)
    caf.add_freshid(100, 200)

    assert caf.get_range(9) == (1, 10)
    assert caf.get_range(150) == (100, 200)

def test_overlapping_ranges(caf):
    caf.add_freshid(1, 10)
    caf.add_freshid(8, 20)

    assert len(caf.freshids) == 1
    assert caf.freshids[0] == (1, 20)

def test_overlapping_ranges_reverse(caf):
    caf.add_freshid(8, 20)
    caf.add_freshid(1, 10)

    assert len(caf.freshids) == 1
    assert caf.freshids[0] == (1, 20)

def test_smaller(caf):
    caf.add_freshid(1, 10)
    caf.add_freshid(5, 7)

    assert caf.freshids[0] == (1, 10)
    assert len(caf.freshids) == 1

def test_bigger(caf):
    caf.add_freshid(5, 7)
    caf.add_freshid(1, 10)

    assert caf.freshids[0] == (1, 10)
    assert len(caf.freshids) == 1

def test_inbetween(caf):
    caf.add_freshid(1, 10)
    caf.add_freshid(20, 30)

    caf.add_freshid(12, 18)
    
    assert len(caf.freshids) == 3
    assert caf.freshids[0] == (1, 10)
    assert caf.freshids[1] == (20, 30)
    assert caf.freshids[2] == (12, 18)

# part 1
def test_isfresh(caf):
    caf.add_freshid(1, 10)
    assert caf.isfresh(3)
    assert caf.isfresh(1)
    not caf.isfresh(11)


def test_example_part1(caf):
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

def test_wierd12(caf):
    caf.add_freshid(10, 14) # 4
    caf.add_freshid(16, 20) # 4
    caf.add_freshid(12, 18) # 6

    assert caf.freshids[0] == (10, 15)
    assert caf.freshids[1] == (16, 20)

    assert len(caf.freshids) == 2

    assert caf.count() == 11

def test_3to5(caf):
    caf.add_freshid(3, 5)   # 2

    assert caf.count() == 3


def test_example_part2(caf):
    caf.add_freshid(3, 5)   # 2
    caf.add_freshid(10, 14) # 4
    caf.add_freshid(16, 20) # 4
    caf.add_freshid(12, 18) # 6


    # The ingredient IDs that these ranges consider to be fresh are
    # 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20.
    # So, in this example, the fresh ingredient ID ranges consider
    # a total of 14 ingredient IDs to be fresh.
    assert caf.count() == 14


def test_lines(caf):
    caf.add_freshid(291687894568177, 292172488078380)
    caf.add_freshid(427870047590103, 428717994993731)
    caf.add_freshid(265654071674500, 266942022274189)

 
    lines = ["291687894568177-292172488078380",
             "427870047590103-428717994993731",
             "265654071674500-266942022274189",
             "153971257711624-156206755538956",
             "533206775741152-538581383901374",
             "513693225083242-518339086307594",
             "81406311055957-87395321431072",
             "517429407132374-522476734966169"]

    for line in lines:
        start, end = caf.parse_range(line)
        caf.add_freshid(start, end)

    assert len(caf.freshids) == 7


def test_bounds(caf):
    caf.load_file("data.txt")
    count = caf.count()
    assert 350980967982847 < count  # answer is too low
    assert count < 363860846655307  # answer is too high

def main():

    caf = Cafeteria()
    caf.load_file("data.txt")
    print(f"Freshcount: {caf.freshcount}")

    print("* Part 2")
    c = caf.count()
    print(f"Total ingredients fresh: {c}")
    
if __name__ == '__main__':
    main()
