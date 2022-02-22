import math
from abc import ABC

from QueueInterface import QueueInterface, Node


class HeapArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Heap Array")
        self.pointers = []

    def bubbleUp(self, index, lookupTable):
        if len(self.pointers) > 1:
            childIndex = self.pointers[index]
            parentIndex = self.getParent(index)
            if parentIndex is not None and childIndex is not None:
                parentDist = lookupTable[parentIndex].dist
                childDist = lookupTable[childIndex].dist
                while parentDist > childDist:
                    childIndex = self.pointers[index]
                    parentIndex = self.getParent(index)
                    if parentIndex is not None and childIndex is not None:
                        childDist = lookupTable[childIndex].dist
                        parentDist = lookupTable[parentIndex].dist
                        self.pointers[self.getParentIndex(index)] = childIndex
                        self.pointers[index] = parentIndex
                        index = self.getParentIndex(index)
                    else:
                        break

    def bubbleDown(self, index, lookupTable):
        while True:
            parentIndex = self.pointers[index]
            leftChild = self.getLeftChild(index)
            rightChild = self.getRightChild(index)
            leftChildDist = 0
            rightChildDist = 0
            if leftChild is not None:
                leftChildDist = lookupTable[leftChild].dist
            if rightChild is not None:
                rightChildDist = lookupTable[rightChild].dist
            parentDist = lookupTable[parentIndex].dist

            if leftChild is not None:
                if rightChild is not None:
                    if leftChildDist <= rightChildDist:
                        if leftChildDist < parentDist:
                            self.pointers[index] = leftChild
                            self.pointers[(index * 2) + 1] = parentIndex
                            index = (index * 2) + 1
                        elif rightChildDist < parentDist:
                            self.pointers[index] = rightChild
                            self.pointers[(index * 2) + 2] = parentIndex
                            index = (index * 2) + 2
                        else:
                            break
                    elif rightChildDist < parentDist:
                        self.pointers[index] = rightChild
                        self.pointers[(index * 2) + 2] = parentIndex
                        index = (index * 2) + 2
                    else:
                        break
                elif leftChildDist < parentDist:
                    self.pointers[index] = leftChild
                    self.pointers[(index * 2) + 1] = parentIndex
                    index = (index * 2) + 1
                else:
                    break
            elif rightChild is not None:
                if rightChildDist < parentDist:
                    self.pointers[index] = rightChild
                    self.pointers[(index * 2) + 2] = parentIndex
                    index = (index * 2) + 2
                else:
                    break
            else:
                break

    def getParent(self, index):
        if index != 0:
            return self.pointers[math.floor((index - 1) / 2)]
        else:
            return None

    def getLeftChild(self, index):
        if ((index * 2) + 1) < len(self.pointers):
            return self.pointers[(index * 2) + 1]
        else:
            return None

    def getRightChild(self, index):
        if ((index * 2) + 2) < len(self.pointers):
            return self.pointers[(index * 2) + 2]
        else:
            return None

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
