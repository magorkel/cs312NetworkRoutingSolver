#!/usr/bin/python3

from CS312Graph import *
import time

from HeapArray import HeapArray
from QueueArray import QueueArray


# noinspection PyMethodMayBeStatic
class NetworkRoutingSolver:
    shortestpaths = ''

    def __init__(self):
        self.shortestPaths = None

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        shortestPaths = self.shortestPaths
        destNode = ''
        for n in shortestPaths:
            if n.id == destIndex:
                destNode = n
                if destNode.prev == -1:
                    return {'cost': float('inf'), 'path': []}

        hasPrev = True
        currentNode = destNode
        path_edges = []
        total_length = 0
        while hasPrev:
            hasPrev = False
            if currentNode.prev:
                hasPrev = True
                path_edges.append((currentNode.location, currentNode.prev.location, '{:.0f}'.format(currentNode.edge)))
                total_length += currentNode.edge
                currentNode = currentNode.prev
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        arrayBase = None

        if use_heap:
            arrayBase = HeapArray()
        else:
            arrayBase = QueueArray()

        # Initialize the priority queue and get the source node
        lookupTable = QueueArray.initList(arrayBase, srcIndex, self.network.nodes)
        pQueue = lookupTable.copy()

        # Loop through the priority queue
        while pQueue:
            # Pop the first node off of the queue and update the priority queue
            u, pQueue = arrayBase.deleteMin(pQueue, lookupTable)

            # Get the neighbors for the node we are visiting
            neighbors = self.network.nodes[u.id].neighbors

            # Loop through all the neighbors and run the comparison against them
            neighbors = arrayBase.sortNeighbors(neighbors)
            for v in neighbors:
                # Find where v lives in the lookup table
                vIndex = arrayBase.getVisitorIndex(lookupTable, v.dest.node_id)
                # Find where v lives in the priority queue
                pIndex = arrayBase.getVisitorIndex(pQueue, v.dest.node_id)

                # If v lives inside the priority queue then visit it
                if vIndex is not None and pIndex is not None:
                    uvDist = u.dist + v.length
                    if lookupTable[vIndex].dist > uvDist:
                        # Update the node that we're visiting
                        lookupTable[vIndex].dist = uvDist
                        lookupTable[vIndex].edge = v.length
                        lookupTable[vIndex].prev = u

        self.shortestPaths = lookupTable

        t2 = time.time()
        return t2 - t1
