#!/usr/bin/env python

class Joltage:
    def sum(self, banks):
        "Return the sum of joltages produced by banks parameter"
        return sum([self.maxjoltage(bank) for bank in banks])

    def sum12(self, banks):
        "Return the sum of joltages produced by banks parameter"
        return sum([self.max12(bank) for bank in banks])

    def max12(self, bank):
        "Same as maxjoltage but for 12 batteries"
        # Ensure bank is a list
        bank = list(bank)

        selected_batteries = []

        popcount = 0
        poplimit = len(bank) - 12 # amount of selectable batteries
        
        for battery in bank:
            # always select the first battery
            if len(selected_batteries) == 0:
                selected_batteries = [bank[0]]
                continue

            # Is the current battery better than the last selected one?
            if battery > selected_batteries[-1] and popcount < poplimit:
                selected_batteries.pop()
                popcount += 1

            # Did we select too many batteries?
            while len(selected_batteries) >= 12 and popcount < poplimit:
                selected_batteries.pop()
                popcount += 1
                
            selected_batteries.append(battery)

        return int(''.join(selected_batteries))
            

    def maxjoltage(self, bank):
        "Returns the maximum of joltage a bank of batteries can produce"

        # find the largest number aslong as it is not the last
        # and its position in the bank
        left = max(list(bank[:-1]))
        left_index = bank.index(str(left))

        # we want to find the second number
        right = max(list(bank[left_index+1:]))
        
        return 10 * int(left) + int(right)

################################################################################
# pytest

# part 2
def est_part2_sum():
    banks = "987654321111111\n811111111111119\n234234234234278\n818181911112111"


    joltage = Joltage()
    
    assert 3121910778619 == joltage.sum12(banks.split("\n"))

def test_part2_bank1():
    joltage = Joltage()

    assert 987654321111 == joltage.max12("987654321111111")

def test_part2_bank2():
    joltage = Joltage()

    assert 811111111119 == joltage.max12("811111111111119")

def test_part2_bank3():
    joltage = Joltage()

    assert 434234234278 == joltage.max12("234234234234278")

def test_part2_bank4():
    joltage = Joltage()

    assert 888911112111 == joltage.max12("818181911112111")

def test_line1():
    j = Joltage()

    assert 443455384464 == j.max12("2224422232242212251325212222225221223222824142211222222122322216222332122423433242142132212224222232")

def test_bounds():
    with open("data.txt", "r") as f:
        lines = f.read().splitlines()

    j = Joltage()
    assert j.sum12(lines) > 98762499745125


# part 1
def test_sum():
    banks = "987654321111111\n811111111111119\n234234234234278\n818181911112111"


    joltage = Joltage()
    
    assert 357 == joltage.sum(banks.split("\n"))

def test_bank1():
    joltage = Joltage()

    assert 98 == joltage.maxjoltage("987654321111111")

def test_bank2():
    joltage = Joltage()

    assert 89 == joltage.maxjoltage("811111111111119")

def test_bank3():
    joltage = Joltage()

    assert 78 == joltage.maxjoltage("234234234234278")

def test_bank4():
    joltage = Joltage()

    assert 92 == joltage.maxjoltage("818181911112111")

    
################################################################################
# main

def main():
    with open("data.txt", "r") as f:
        lines = f.read().splitlines()

    j = Joltage()


    # Part 1 
    joltage = j.sum(lines)
    print(f"Joltage for part 1 = {joltage}")

    # Part 12
    joltage = j.sum12(lines)
    print(f"Joltage for part 2 = {joltage}")

    # 98762499745125 is too low

if __name__ == '__main__':
    main()
