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

    """
    Time: O((|v| + |e|) * log(|v|) with a heap as it iterates over all of the nodes in {G} and the edges for each edge
    node {E}. This iterates over all of them using a priority queue, with a heap queue having a worst run time of 
    log(|v|. If the priority queue was to only use an array our time complexity would jump up drastically to O(|v^2|).
    
    Space: O(|v|) since we create lists as big as {G}
    """

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        arrayBase = None

        if use_heap:
            arrayBase = HeapArray()
        else:
            arrayBase = QueueArray()

        # Initialize the priority queue and get the source node
        lookupTable = arrayBase.initList(srcIndex, self.network.nodes)
        pQueue = lookupTable.copy()

        # Loop through the priority queue
        while pQueue:
            # Pop the first node off of the queue and update the priority queue
            u, pQueue = arrayBase.deleteMin(pQueue, lookupTable)

            # Get the neighbors for the node we are visiting
            neighbors = self.network.nodes[u.id].neighbors
            # Loop through all the neighbors and run the comparison against them
            for v in neighbors:
                # Grab the index of the neighbor we are visiting
                vIndex = v.dest.node_id
                # Compute the combined dist of u.dist from the lookup table, and v.length from the graph
                uvDist = u.dist + v.length
                if lookupTable[vIndex].dist > uvDist:
                    # Update the node that we're visiting
                    lookupTable[vIndex].dist = uvDist
                    lookupTable[vIndex].edge = v.length
                    lookupTable[vIndex].prev = u
                    arrayBase.decreaseKey(vIndex, lookupTable)

        self.shortestPaths = lookupTable

        t2 = time.time()
        return t2 - t1
