from typing import Protocol
from abc import abstractmethod

class Node(object):
    id = -1
    prev = -1
    dist = 10000
    location = None
    edge = 0

class QueueInterface(Protocol):
    """
    Initialize the priority queue and set the source node at the top of the priority queue.

    :keyword {G}: the graph of all of the existing nodes
    :param srcIndex: the index of the source node in {G}

    :returns the initialized list.
    """

    @abstractmethod
    def initList(self, srcIndex: int, network) -> list: raise NotImplementedError

    @abstractmethod
    def insert(self): raise NotImplementedError

    @abstractmethod
    def bubbleUp(self): raise NotImplementedError

    """
    Pops the top of the stack.
    
    :param H: the priority queue
    :lookupTable: the table that has the updated values
    
    :returns {nodeToReturn, H} a tuple containing the popped node and the updated priority queue
    """

    @abstractmethod
    def deleteMin(self, H: list, lookupTable: list): raise NotImplementedError

    @abstractmethod
    def bubbleDown(self): raise NotImplementedError

    @abstractmethod
    def decreaseKey(self): raise NotImplementedError

    @abstractmethod
    def sortNeighbors(self, neighbors: list) -> list: raise NotImplementedError

    @abstractmethod
    def makeNode(self, id, prev, dist, location): raise NotImplementedError

    """
    Gets the index of the node with nodeID from the current state of H.
    
    :param H: the priority queue
    :param nodeID: the node id we are trying to find in H
    
    :returns the index of the nodes location in the priority queue
    """

    @abstractmethod
    def getVisitorIndex(self, H: list, nodeID) -> int: raise NotImplementedError
