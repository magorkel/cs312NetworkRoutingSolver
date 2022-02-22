import math
from abc import ABC

from QueueInterface import QueueInterface, Node


class HeapArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Heap Array")
        self.pointers = []

    """
    Time: O(log |v|) | Space: O(1)
    
    Bubbles up the minimum value to the top of the tree
    
    :param index: the node to be updated
    :param lookupTable: the lookupTable for referencing the nodes distance values
    """

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

    """
    Time: O(log |v|) | Space: O(1)
    
    Bubbles down the maximum value to the bottom of the tree
    
    :param index: the node to be updated
    :param lookupTable: the lookupTable for referencing the nodes distance values
    """

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

    # Time: O(1) | Space O(1)
    def getParent(self, index):
        if index != 0:
            return self.pointers[math.floor((index - 1) / 2)]
        else:
            return None

    # Time: O(1) | Space O(1)
    def getLeftChild(self, index):
        if ((index * 2) + 1) < len(self.pointers):
            return self.pointers[(index * 2) + 1]
        else:
            return None

    # Time: O(1) | Space O(1)
    def getRightChild(self, index):
        if ((index * 2) + 2) < len(self.pointers):
            return self.pointers[(index * 2) + 2]
        else:
            return None

    # Time: O(1) | Space O(1)
    def getParentIndex(self, index):
        if index != 0:
            return math.floor((index - 1) / 2)
        else:
            return None

    # Interface Methods vvv

    """
    Time: O(log |v|) | Space: O(1)
    
    Pop the top of the binary heap.
    
    :param H: N/A
    :param lookupTable: the array containing the Node objects
    
    :returns {lookupTable[nodeIndex], self.pointers} Tuple containing the popped Node object and updated table
    
    """

    def deleteMin(self, H: list, lookupTable: list):
        nodeIndex = self.pointers.pop(0)

        if len(self.pointers) > 0:
            self.pointers.insert(0, self.pointers[-1])  # Time: O(1) | Space: O(1) - Insert at the front of the list
            self.pointers.pop()
            self.bubbleDown(0, lookupTable)  # Time: O(log |v|) | Space: O(1)

        return lookupTable[nodeIndex], self.pointers

    """
    Time: O(log |v|) | Space: O(1)
    Updates a specific index in the array with the new key. Once the array is updated we bubbleUP to keep the
    heap sorted properly.
    
    :param nodeId: Node id to be updated
    :param lookupTable: reference table for the Node Id
    """

    def decreaseKey(self, nodeId, lookupTable: list):
        if len(self.pointers) > 0:
            try:
                index = self.pointers.index(nodeId)
                self.bubbleUp(index, lookupTable)  # Time: O(log |v|) | Space: O(1)
            except ValueError:
                pass

    """
    Time: O(n) | Space: O(1)
    
    Here we take the nodes from the network {G} and parse through them to collect their individual node ids.
    We insert these ids into the pointer list using Node objects initialize the heap.
    After H has all of the values transposed from {G} we bubbleUP the pointers to create the sorted heap.
    
    :param srcIndex: the index of the source node in the network
    :param network: the entire graph {G}
    
    returns H: the new list of nodes that will act as the priority queue when returned to the Dijkstra alg.
    """

    def initList(self, srcIndex: int, network) -> list:
        sourceNode = None
        H = []
        for vertex in range(len(network)):  # Time: O(n) | Space: O(1) - get node ids from network {G}
            if network[vertex].node_id == srcIndex:
                sourceNode = self.makeNode(network[vertex].node_id, None, 0, network[vertex].loc)  # Time/Space: O(1)
                H.append(sourceNode)  # Time: O(1) | Space: O(1) - insert nodes into H
            else:
                node = self.makeNode(network[vertex].node_id, -1, math.inf, network[vertex].loc)  # Time/Space: O(1)
                H.append(node)  # Time: O(1) | Space: O(1) - insert nodes into H

            self.pointers.append(network[vertex].node_id)  # Time: O(1) | Space: O(1) - insert nodes into pointer array
            self.bubbleUp(len(self.pointers) - 1, H)  # Time: O(log |v|) | Space: O(1)

        return H
