#!/usr/bin/env python
# see: https://adventofcode.com/2025/day/2
from math import floor, ceil

class GiftShop:
    "Model the gift shop"

    def check_id(self, identifier):
        "Check if an identifier is good"
        # uneven numbers can't repeat
        if len(str(identifier)) % 2 == 1:
            return True

        # where do we split the string in half?
        id_middle = floor(len(str(identifier))/2)

        # first part of the identifier should not match the second half
        return not identifier[:id_middle] == identifier[id_middle:]

    def split_range(self, idrange):
        "Return the list of a range defined by a string of start and endpoint"
        "  example: '1-10' returns ['1', '2', ..., '10']"

        startid, endid = idrange.split("-")

        return [str(x) for x in range(int(startid), int(endid)+1)]

    def bad_ids(self, ids):
        "Return a generator of bad ids from a string of ids"
        idrange = ids.split(",")
        for i in idrange:
            idlist = self.split_range(i)

            for id1 in idlist:
                # Id is not good?
                if not self.check_id(id1):
                    yield id1

class GiftShopPartTwo(GiftShop):
    "Model part two of the gift shop"

    def check_id(self, identifier):
        "Check if an identifier is valid"

        # Ensure identifier is a string
        identifier = str(identifier)

        # Identifiers of length 1 are always valid
        if len(identifier) <= 1:
            return True

        for r in range(1, floor(len(identifier)/2)+1):
            # we want to nibble parts from left side of the identifier
            # to see if whatever we nibbled off, is a pattern?
            pattern   = identifier[:r]

            # if our pattern is valid, it replaces everything inside the identifier
            # string, leaving the remainder empty
            if '' == identifier.replace(pattern, ''):
                return False
        
        return True

################################################################################
# this is part is run by the command pytest / pytest-watch / ptw -c -n -w

# Tests for part 1
def test_id():
    "Test if a id is valid"

    gs = GiftShop()
    
    bad_ids = ["11", "1010", "1188511885", "222222", "446446", "38593859"]

    for bad_id in bad_ids:
        assert gs.check_id(bad_id) == False

def test_idrange():
    "Test a range of ids"
    
    gs = GiftShop()

    assert gs.split_range("1-3") == ["1", "2", "3"]
    
def test_badids():
    "Test bad ids"

    gs = GiftShop()

    # 11-22 has two invalid IDs, 11 and 22.
    assert "11" in gs.bad_ids("11-22")
    assert "22" in gs.bad_ids("11-22")

    # 95-115 has one invalid ID, 99.
    assert "99" in gs.bad_ids("95-115")

    # 998-1012 has one invalid ID, 1010.
    assert "1010" in gs.bad_ids("998-1012")

    # 1188511880-1188511890 has one invalid ID, 1188511885.
    assert "1188511885" in gs.bad_ids("1188511880-1188511890")

    # 222220-222224 has one invalid ID, 222222.
    assert "222222" in gs.bad_ids("222220-222224")

    # 1698522-1698528 contains no invalid IDs.
    #assert gs.bad_ids("1698522-1698528") is []

    # 446443-446449 has one invalid ID, 446446.
    assert "446446" in gs.bad_ids("446443-446449")

    # 38593856-38593862 has one invalid ID, .
    assert "38593859" in gs.bad_ids("38593856-38593862")

def test_moreids():
    "Pretty much the same as test_badids() but in one go"
    ids = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    gs = GiftShop()
    
    assert list(gs.bad_ids(ids)) == ["11", "22", "99", "1010", "1188511885", "222222", "446446", "38593859"]

def test_sum():
    "Test summing the bad ids up"

    ids = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    gs = GiftShop()
    assert sum([int(x) for x in gs.bad_ids(ids)]) == 1227775554

# Tests for part 2
def test_invalid_numbers():
    gs = GiftShopPartTwo()

    not gs.check_id("12341234")
    not gs.check_id("123123123") 
    not gs.check_id("1212121212")
    not gs.check_id("1111111")


def test_valid_numbers():
     numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

     gs = GiftShopPartTwo()

     for number in numbers:
         assert gs.check_id(str(number))

def test_number999():
    "998-1012 now has two invalid IDs, 999 and 1010."
    gs = GiftShopPartTwo()

    not gs.check_id("999")

    assert "999" in gs.bad_ids("998-1012")
    assert "1010" in gs.bad_ids("998-1012")

def test_number565656():
    "565653-565659 now has one invalid ID, 565656."
    gs = GiftShopPartTwo()

    bad_ids = list(gs.bad_ids("565653-565659"))
    assert "565656" in bad_ids
    assert "565657" not in bad_ids
    
def test_number824824824():
    "824824821-824824827 now has one invalid ID, 824824824"
    gs = GiftShopPartTwo()

    assert "824824824" in gs.bad_ids("824824821-824824827")

def test_sum_part2():
    "Adding up all the invalid IDs in this example produces 4174379265"
    line = "11-22 ,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    gs = GiftShopPartTwo()
    
    assert sum([int(x) for x in gs.bad_ids(line)]) == 4174379265


def test_bounds():
    "33832678425 as answer is too high"
    gs = GiftShopPartTwo()

    with open("data.txt", "r") as f:
        line = f.read()

        #print([int(x) for x in gs.bad_ids(line)])
        assert sum([int(x) for x in gs.bad_ids(line)]) < 33832678425
        assert sum([int(x) for x in gs.bad_ids(line)]) > 4174379265
 

################################################################################
# this will be run when the file is executed as a program

def main():
    line = ""

    with open("data.txt", "r") as f:
        line = f.read()

    print("* Solving part 1")
    gs = GiftShop()

    print("Sum for Part1:", sum([int(x) for x in gs.bad_ids(line)]))
    
    print("* Solving part 2")
    gs = GiftShopPartTwo()
    print("Sum for Part2:", sum([int(x) for x in gs.bad_ids(line)]))


if __name__ == '__main__':
    main()
