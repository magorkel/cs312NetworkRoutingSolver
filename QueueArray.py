# from NetworkRoutingSolver import Node
from abc import ABC

from QueueInterface import QueueInterface, Node


class QueueArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Queue Array")

    def deleteMin(self, H: list, lookupTable: list):
        H.sort(key=lambda v: v.dist)
        nodeToReturn = H[0]
        H.pop(0)
        return nodeToReturn, H

    def sortNeighbors(self, neighbors: list) -> list:
        neighbors.sort(key=lambda v: v.length, reverse=True)
        return neighbors

    def makeNode(self, id, prev, dist, location):
        node = Node()
        node.id = id
        node.prev = prev
        node.dist = dist
        node.location = location
        return node

    def getVisitorIndex(self, H: list, nodeID) -> int:
        for i in range(len(H)):
            if H[i].id == nodeID:
                return i
        return None

    def initList(self, srcIndex: int, network) -> list:
        sourceNode = None
        H = []
        for vertex in range(len(network)):
            if network[vertex].node_id == srcIndex:
                sourceNode = self.makeNode(network[vertex].node_id, None, 0, network[vertex].loc)
                H.append(sourceNode)
            else:
                node = self.makeNode(network[vertex].node_id, -1, 10000, network[vertex].loc)
                H.append(node)

        return H
