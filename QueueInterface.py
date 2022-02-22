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

    """
    Pops the top of the stack.
    
    :param H: the priority queue
    :lookupTable: the table that has the updated values
    
    :returns {nodeToReturn, H} a tuple containing the popped node and the updated priority queue
    """

    @abstractmethod
    def deleteMin(self, H: list, lookupTable: list): raise NotImplementedError

    @abstractmethod
    def decreaseKey(self, nodeId, lookupTable: list): raise NotImplementedError

    def makeNode(self, id, prev, dist, location):
        node = Node()
        node.id = id
        node.prev = prev
        node.dist = dist
        node.location = location
        return node
