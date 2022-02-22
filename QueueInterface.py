from typing import Protocol
from abc import abstractmethod


class Node(object):
    id = -1
    prev = -1
    dist = 10000
    location = None
    edge = 0


class QueueInterface(Protocol):
    @abstractmethod
    def initList(self, srcIndex: int, network) -> list: raise NotImplementedError

    @abstractmethod
    def deleteMin(self, H: list, lookupTable: list): raise NotImplementedError

    @abstractmethod
    def decreaseKey(self, nodeId, lookupTable: list): raise NotImplementedError

    """
    Time: O(1) | Space: O(1)
    
    Create a new node and return it with the assigned values.
    
    :param id: the id of the node
    :param prev: the previous node id that this node points to
    :param dist: the distance between this node and it's previous node
    :param location: the location of where this node lives in {G}, (x,y) point values
    
    :returns node: the new Node object containing the assigned properties
    """

    def makeNode(self, id, prev, dist, location):
        node = Node()
        node.id = id
        node.prev = prev
        node.dist = dist
        node.location = location
        return node
