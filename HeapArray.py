from abc import ABC

from QueueInterface import QueueInterface, Node


class HeapArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Heap Array")

    def insert(self):
        pass

    def bubbleUp(self):
        pass

    def bubbleDown(self):
        pass

    def decreaseKey(self):
        pass

    # Interface Methods vvv

    def deleteMin(self, H: list, lookupTable: list):
        pass

    def sortNeighbors(self, neighbors: list) -> list:
        pass

    def makeNode(self, id, prev, dist, location):
        pass

    def getVisitorIndex(self, H: list, nodeID) -> int:
        pass

    def initList(self, srcIndex: int, network) -> list:
        pass
