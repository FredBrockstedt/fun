#!/usr/bin/env python
from pprint import pprint
import pytest

import operator
from functools import reduce

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

from io import StringIO
import numpy as np

class Circuit:
    """
    A circuit is a connection between two or more junction boxes

    Args:
        jboxes: A set of junction boxes
    """

    def __init__(self):
        self.jboxes = set()

    def add(self, jbox):
        """
        Add a junction box to the circuit

        Args:
            jbox: Index of the junction box to add
        """
        self.jboxes.add(jbox)

    def contains(self, jbox):
        """
        Does the curcuit contain the jbox?

        Args:
            jbox: Index of the junction box to find in the circuit
        """
        return jbox in self.jboxes

    def __len__(self):
        "Return the amount of junction boxes contained in this circuit"
        return len(self.jboxes)

    def __str__(self):
        "Return a string of the indexes of junction boxes contained in this circuit"
        return str(self.jboxes)

class Circuits:
    def __init__(self):
        self.circuits = []
        self.used_jboxes = set()

    def add_connection(self, jbox1, jbox2):
        """
        Add a jbox to the circuits

        Args:
            jbox1: Start of the connection
            jbox2: End of the connection
        """

        # Both junction boxes are completly new
        if jbox1 not in self.used_jboxes and jbox2 not in self.used_jboxes:
            # Create a new circuit
            logging.debug(f"Creating a new circuit for {jbox1} and {jbox2}")
            circuit = Circuit()
            circuit.add(jbox1)
            circuit.add(jbox2)
            self.circuits.append(circuit)

            self.used_jboxes.add(jbox1)
            self.used_jboxes.add(jbox2)


        # Jbox 1 is in a circuit, to which we want to add jbox2
        elif jbox1 in self.used_jboxes and jbox2 not in self.used_jboxes:
            logging.debug(f"jbox1 = {jbox1} is already known")
            for circuit in self.circuits:
                if circuit.contains(jbox1):
                    logging.debug(f"Adding jbox2 = {jbox2} to circuit = {circuit}")
                    circuit.add(jbox2)
                    self.used_jboxes.add(jbox2)

        # Jbox 2 is in a circuit, to which we want to add jbox1
        elif jbox1 not in self.used_jboxes and jbox2 in self.used_jboxes:
            logging.debug(f"jbox2 = {jbox2} is already known")
            for circuit in self.circuits:
                if circuit.contains(jbox2):
                    logging.debug(f"Adding jbox1 = {jbox1} to circuit = {circuit}")
                    circuit.add(jbox1)
                    self.used_jboxes.add(jbox1)

        # Both junction boxes are already in use and we have to join two circuits
        elif jbox1 in self.used_jboxes and jbox2 in self.used_jboxes:
            logging.debug(f"jbox1 = {jbox1} and jbox2 = {jbox2} are already known")
            for circuit1 in self.circuits:
                if circuit1.contains(jbox1):
                    # Find jbox1 circuit and ...
                    logging.debug(f"jbox1 = {jbox1} found in {circuit1}")
                    for circuit2 in self.circuits:
                        if circuit2.contains(jbox2):
                            # we need to check if both jboxes are in the same circuit
                            if circuit1 == circuit2:
                                # we do nothing, as both junction boxes are already in the same circuit
                                logging.debug("Both boxes are in {circuit1}, skipping")
                                return

                            # they are in different circuits that need to be joined
                            logging.debug(f"jbox2 = {jbox2} found in {circuit2}")
                            for jbox in circuit2.jboxes:
                                # ... add all the junction boxes of jbox2 circuit
                                logging.debug(f"{circuit2} - {jbox} -> {circuit1}")
                                circuit1.add(jbox)

                            # remove circuit2
                            self.circuits.remove(circuit2)
        
        else:
            logging.debug("This case should not exist!")


    def __len__(self):
        "Return the length of the circuits"
        return len(self.circuits)

    def __str__(self):
        s = f"There are {len(self.circuits)} cicuits"
        return s


class JBox:
    """
    Represent a junction boxes as found in
    https://adventofcode.com/2025/day/8

    Attributes:
        matrix:    A matrix describing the positions of the junction boxes
        distances: A matrix where position (i, j) is the distance from junction box i to box j
        circuits:  A list of lists which contains the circuits formed between the junction boxes, each list contains the indexes to the junctino boxes in matrix which are connected together
    """

    def __init__(self):
        "Setup the JBox object"
        self.matrix = None
        self.distances = None
        self.circuits = Circuits()


    def from_stringio(self, string):
        """
        Parse a matrix from a StringIO object

        Args:
            string: StringIO object with columns seperated by , and lines by \n
        """
        self.matrix = np.loadtxt(string, delimiter=',')

    def calc_distances(self):
        """
        Compute the distances between the junction boxes 
        """
        #diff = self.matrix - self.matrix
        self.distances = np.zeros((max(self.matrix.shape), max(self.matrix.shape)))

        rows, columns = self.distances.shape
        for j in range(rows):
            # the distance from j to k is the distance from k to j
            for k in range(j, columns):
                # euclidean distance between a and b
                diff = np.abs(self.matrix[j] - self.matrix[k])
                self.distances[j, k] = np.sqrt(diff @ diff.T)

    def closest(self):
        """
        Return the closes junction boxs

        Returns:
            jboxes: A list of tuples that contain (<distance>, <from junction box>, <to junction box>)
        """
        jboxes = []
        for j,_ in enumerate(self.distances):
            for k,_ in enumerate(self.distances):
                jboxes.append((self.distances[j][k], j, k))

        # smallest distances first
        jboxes = sorted(jboxes, reverse=False)

        # remove zeros
        return list(filter(lambda x: x[0] != 0, jboxes))

    def create_circuits(self, amount):
        """
        Create circuits

        Args:
            amount: How many circuits to create
        """
        cables = self.closest()

        for cable in cables[0:amount]:
            self.circuits.add_connection(cable[1], cable[2])


    def part1_sum(self):
        """
        Return the sum for part 1
        """
        # get the 3 largest circuits
        sorted_circuits = sorted(self.circuits.circuits, key=len, reverse=True)
        return reduce(operator.mul, [len(circuit) for circuit in sorted_circuits[0:3]])


################################################################################
# pytest

@pytest.fixture
def example():
    data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    return StringIO(data)
    


def test_inputoutput(example):
    jbox = JBox()
    jbox.from_stringio(example)

    #assert jbox.matrix != None
    assert jbox.matrix.shape == (20, 3)

def test_distances(example):
    jbox = JBox()
    jbox.from_stringio(example)

    jbox.calc_distances()
    print(jbox.distances)
    assert jbox.distances[0][0] == 0
    assert jbox.distances.shape == (20, 20)


def test_euclidean_distance(example):
    jbox = JBox()
    jbox.from_stringio(example)

    j = 7
    k = 19

    diff = np.abs(jbox.matrix[j] - jbox.matrix[k])
    result = int(np.sqrt(diff @ diff.T))

    assert 328 == result

    jbox.calc_distances()

    assert int(jbox.distances[j][k]) == result

    
def test_jbox_distances(example):
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    lst = jbox.closest()
    
    #print(np.argsort(jbox.distances, axis=1))
    #print(np.sort(jbox.distances, axis=1))

    #for dist, jbox1, jbox2 in lst:
    #    print(int(dist), jbox.matrix[jbox1], jbox.matrix[jbox2], jbox1, jbox2)

    # In this example, the two junction boxes which are closest together are 162,817,812 and 425,690,689
    assert lst[0][1] == 0
    assert lst[0][2] == 19

    # Now, the two junction boxes which are closest together but aren't already directly connected are 162,817,812 and 431,825,988.
    assert lst[1][1] == 0
    assert lst[1][2] == 7

    # The next two junction boxes to connect are 906,360,560 and 805,96,715.
    assert lst[2][1] == 2
    assert lst[2][2] == 13

    # The next two junction boxes are 431,825,988 and 425,690,689.
    print(f"{jbox.matrix[lst[3][1]]} == 431,825,988")
    print(f"{jbox.matrix[lst[3][2]]} == 425,690,689")
    print(f"{jbox.distances[7][19]}")
    assert lst[3][1] == 7
    assert lst[3][2] == 19

def test_1junction(example):
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    jbox.create_circuits(1)

    assert 1 == len(jbox.circuits)
    assert 2 == len(jbox.circuits.circuits[0])


def test_2junction(example):
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    jbox.create_circuits(2)

    assert 1 == len(jbox.circuits)
    assert 3 == len(jbox.circuits.circuits[0])

def test_3junction(example):
    "The next two junction boxes to connect are 906,360,560 and 805,96,715. After connecting them, there is a circuit containing 3 junction boxes, a circuit containing 2 junction boxes"
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    jbox.create_circuits(3)

    assert 2 == len(jbox.circuits)
    assert 3 == len(jbox.circuits.circuits[0])
    assert 2 == len(jbox.circuits.circuits[1])

def test_4junction(example):
    "The next two junction boxes are 431,825,988 and 425,690,689. Because these two junction boxes were already in the same circuit, nothing happens!"
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    jbox.create_circuits(4)

    assert 2 == len(jbox.circuits)
    assert 3 == len(jbox.circuits.circuits[0])
    assert 2 == len(jbox.circuits.circuits[1])

    
def test_junctions(example):
    """
    After making the ten shortest connections, there are 11 circuits:
    one circuit which contains 5 junction boxes, one circuit which
    contains 4 junction boxes, two circuits which contain 2 junction
    boxes each, and seven circuits which each contain a single junction box.
    """
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()

    # for dist, jbox1, jbox2 in jbox.closest()[0:10]:
    #     print(f"{jbox.matrix[jbox1]} - {int(dist)} -> {jbox.matrix[jbox2]}")
    
    jbox.create_circuits(10)

    assert 4 == len(jbox.circuits)

    logging.debug(f"circuit[1] = {jbox.circuits.circuits[0]}")
    assert 4 == len(jbox.circuits.circuits[0])

    logging.debug(f"circuit[1] = {jbox.circuits.circuits[1]}")
    assert 5 == len(jbox.circuits.circuits[1])

    logging.debug(f"circuit[2] = {jbox.circuits.circuits[2]}")
    assert 2 == len(jbox.circuits.circuits[2])

    logging.debug(f"circuit[3] = {jbox.circuits.circuits[3]}")
    assert 2 == len(jbox.circuits.circuits[3])


def test_sum(example):
    jbox = JBox()
    jbox.from_stringio(example)
    jbox.calc_distances()
    
    jbox.create_circuits(10)

    assert 40 == jbox.part1_sum()
