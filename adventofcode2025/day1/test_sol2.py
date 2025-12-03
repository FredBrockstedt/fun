# run this programm with the command: pytest

from math import floor

class Safe:
    "Model a safe as found in https://adventofcode.com/2025/day/1/"
    # what is the wheels dial pointing at
    dial = 50
    # how often was the wheel turned across 0?
    passed_zero = 0

    def set_dial(self, value):
        "Set the dial of the safe to a value"
        self.dial = (self.dial + value) % 100
        if self.dial == 0:
            self.passed_zero += 1

    def rotate_left(self, x):
        "Rotate the dial to the left x times"
        x = int(x)
        for i in range(x):
            self.set_dial(-1)

    def rotate_right(self, x):
        "rotate the dial to the left x times"
        x = int(x)
        for i in range(x):
            self.set_dial(1)

    def __str__(self):
        return f" dial = {self.dial} \n passed_zero = {self.passed_zero}"



def test_safe():
    # The dial starts by pointing at 50.
    safe = Safe()
    
    # The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
    safe.rotate_left(68)
    assert safe.dial == 82
    assert safe.passed_zero == 1

    # The dial is rotated L30 to point at 52.
    safe.rotate_left(30)
    assert safe.dial == 52

    # The dial is rotated R48 to point at 0.
    safe.rotate_right(48)
    assert safe.dial == 0
    assert safe.passed_zero == 2

    # The dial is rotated L5 to point at 95.
    safe.rotate_left(5)
    assert safe.dial == 95

    # The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
    safe.rotate_right(60)
    assert safe.dial == 55
    assert safe.passed_zero == 3

    # The dial is rotated L55 to point at 0.
    safe.rotate_left(55)
    assert safe.dial == 0
    assert safe.passed_zero == 4

    # The dial is rotated L1 to point at 99.
    safe.rotate_left(1)
    assert safe.dial == 99

    # The dial is rotated L99 to point at 0.
    safe.rotate_left(99)
    assert safe.dial == 0
    assert safe.passed_zero == 5
    
    # The dial is rotated R14 to point at 14.
    safe.rotate_right(14)
    assert safe.dial == 14

    # The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.
    safe.rotate_left(82)
    assert safe.dial == 32
    assert safe.passed_zero == 6

def main():
    safe = Safe()
    lines = []

    with open("data.txt", "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        if line[0] == "R":
            safe.rotate_right(line[1:])

        if line[0] == "L":
            safe.rotate_left(line[1:])

    print(safe)

if __name__ == '__main__':
    main()
    
