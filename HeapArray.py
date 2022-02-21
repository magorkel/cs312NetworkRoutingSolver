import math
from abc import ABC

from QueueInterface import QueueInterface, Node


class HeapArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Heap Array")
        self.length = 0
        self.pointers = []  # tree of node IDs

    def insert(self, item, distances):
        self.pointers.append(item)
        self.length = len(self.pointers)
        self.bubbleUp(self.length - 1, distances)

    def bubbleUp(self, index, distances):
        if len(self.pointers) > 1:
            child = self.pointers[index]
            parent = self.getParent(index)
            if parent is not None and child is not None:
                parent_weight = distances[parent].dist
                child_weight = distances[child].dist
                while parent_weight > child_weight:
                    child = self.pointers[index]
                    parent = self.getParent(index)
                    if parent is not None and child is not None:
                        child_weight = distances[child].dist
                        parent_weight = distances[parent].dist
                        self.pointers[self.getParentIndex(index)] = child
                        self.pointers[index] = parent
                        index = self.getParentIndex(index)
                    else:
                        break

    def bubbleDown(self, index, distances):
        # recursively moves down the heap
        while True:
            parent = self.pointers[index]
            left_child = self.getLeftChild(index)
            right_child = self.getRightChild(index)
            # gets the weights of the parent and its children
            left_child_weight = 0
            right_child_weight = 0
            if left_child is not None:
                left_child_weight = distances[left_child].dist
            if right_child is not None:
                right_child_weight = distances[right_child].dist
            parent_weight = distances[parent].dist
            if left_child is not None:
                if right_child is not None:
                    # compare left and right child to get smallest weight
                    if left_child_weight <= right_child_weight:
                        if left_child_weight < parent_weight:
                            self.pointers[index] = left_child
                            self.pointers[(index * 2) + 1] = parent
                            index = (index * 2) + 1
                        elif right_child_weight < parent_weight:
                            self.pointers[index] = right_child
                            self.pointers[(index * 2) + 2] = parent
                            index = (index * 2) + 2
                        else:
                            break
                    # if left child isn't less than or equal to right, right is smaller, so switch with parent
                    elif right_child_weight < parent_weight:
                        self.pointers[index] = right_child
                        self.pointers[(index * 2) + 2] = parent
                        index = (index * 2) + 2
                    else:
                        break
                # no right child, so compare left child
                elif left_child_weight < parent_weight:
                    self.pointers[index] = left_child
                    self.pointers[(index * 2) + 1] = parent
                    index = (index * 2) + 1
                else:
                    break
            elif right_child is not None:
                # only right child, so compare it with parent
                if right_child_weight < parent_weight:
                    self.pointers[index] = right_child
                    self.pointers[(index * 2) + 2] = parent
                    index = (index * 2) + 2
                else:
                    break
            else:
                break

    # get the parent node of a given node in the min heap
    def getParent(self, index):
        if index != 0:
            return self.pointers[math.floor((index - 1) / 2)]
        else:
            return None

    # get the left child of the given node in the min heap
    def getLeftChild(self, index):
        if ((index * 2) + 1) < len(self.pointers):
            return self.pointers[(index * 2) + 1]
        else:
            return None

    # get the right child of the given node in the min heap
    def getRightChild(self, index):
        if ((index * 2) + 2) < len(self.pointers):
            return self.pointers[(index * 2) + 2]
        else:
            return None

    # get the index of the parent of a given node
    def getParentIndex(self, index):
        if index != 0:
            return math.floor((index - 1) / 2)
        else:
            return None

    # Interface Methods vvv

    def deleteMin(self, H: list, lookupTable: list):
        nodeIndex = self.pointers.pop(0)

        if len(self.pointers) > 0:
            self.pointers.insert(0, self.pointers[-1])
            self.pointers.pop()
            self.bubbleDown(0, lookupTable)

        return lookupTable[nodeIndex], self.pointers

    def decreaseKey(self, nodeId, lookupTable: list):
        if len(self.pointers) > 0:
            try:
                index = self.pointers.index(nodeId)
                self.bubbleUp(index, lookupTable)
            except ValueError:
                pass

    def sortNeighbors(self, neighbors: list) -> list:
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
                node = self.makeNode(network[vertex].node_id, -1, math.inf, network[vertex].loc)
                H.append(node)

            self.pointers.append(network[vertex].node_id)
            self.bubbleUp(len(self.pointers) - 1, H)

        return H
