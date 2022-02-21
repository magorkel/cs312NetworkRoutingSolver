#!/usr/bin/python3


from CS312Graph import *
import time


class Node(object):
    id = -1
    prev = -1
    dist = 10000
    location = None
    edge = 0


def makeNode(id, prev, dist, location):
    node = Node()
    node.id = id
    node.prev = prev
    node.dist = dist
    node.location = location
    return node


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
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE
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
        # path_edges.append(destNode)
        while hasPrev:
            hasPrev = False
            if currentNode.prev:
                hasPrev = True
                path_edges.append((currentNode.location, currentNode.prev.location, '{:.0f}'.format(currentNode.edge)))
                total_length += currentNode.edge
                currentNode = currentNode.prev

        # node = self.network.nodes[self.source]
        # edges_left = 3
        # while edges_left > 0:
        #     edge = node.neighbors[2]
        #     path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
        #     total_length += edge.length
        #     node = edge.dest
        #     edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        # Initialize the priority queue and get the source node
        lookupTable = self.initList(srcIndex)
        pQueue = lookupTable.copy()

        # Loop through the priority queue
        while pQueue:
            # Pop the first node off of the queue and update the priority queue
            u, pQueue = self.deleteMin(pQueue, lookupTable)

            # Get the neighbors for the node we are visiting
            neighbors = self.network.nodes[u.id].neighbors

            # Loop through all the neighbors and run the comparison against them
            neighbors = self.sortNeighbors(neighbors)
            for v in neighbors:
                # Find where v lives in the lookup table
                vIndex = self.getVisitorIndex(lookupTable, v.dest.node_id)
                # Find where v lives in the priority queue
                pIndex = self.getVisitorIndex(pQueue, v.dest.node_id)

                # If v lives inside the priority queue then visit it
                if vIndex is not None and pIndex is not None:
                    uvDist = u.dist + v.length
                    if lookupTable[vIndex].dist > uvDist:
                        # Update the node that we're visiting
                        lookupTable[vIndex].dist = uvDist
                        lookupTable[vIndex].edge = v.length
                        lookupTable[vIndex].prev = u

                        # Move the node we are visiting to the front of the priority queue
                        # lookupTable.insert(0, lookupTable.pop(vIndex))
                        # pQueue.insert(0, pQueue.pop(pIndex))

        self.shortestPaths = lookupTable

        t2 = time.time()
        return t2 - t1

    # Helper Methods
    #################################################################

    """
    Initialize the priority queue and set the source node at the top of the priority queue.
    
    :keyword {G}: the graph of all of the existing nodes
    :param srcIndex: the index of the source node in {G}
    
    :returns the initialized list.
    """

    def initList(self, srcIndex: int) -> list:
        sourceNode = None
        H = []
        for vertex in range(len(self.network.nodes)):
            if self.network.nodes[vertex].node_id == srcIndex:
                sourceNode = makeNode(self.network.nodes[vertex].node_id, None, 0, self.network.nodes[vertex].loc)
                H.append(sourceNode)
            else:
                node = makeNode(self.network.nodes[vertex].node_id, -1, 10000, self.network.nodes[vertex].loc)
                H.append(node)

        # H.insert(0, sourceNode)
        return H

    """
    Gets the index of the node with nodeID from the current state of H.
    
    :param H: the priority queue
    :param nodeID: the node id we are trying to find in H
    
    :returns the index of the nodes location in the priority queue
    """

    def getVisitorIndex(self, H: list, nodeID) -> int:
        for i in range(len(H)):
            if H[i].id == nodeID:
                return i
        return None  # this is bad

    """
    Pops the top of the stack.
    
    :param H: the priority queue
    :lookupTable: the table that has the updated values
    
    :returns {nodeToReturn, H} a tuple containing the popped node and the updated priority queue
    """

    def deleteMin(self, H: list, lookupTable: list) -> {Node, list}:
        H.sort(key=lambda v: v.dist)
        nodeToReturn = H[0]
        #
        # for v in lookupTable:
        #         if v.id == H[0].id:
        #             nodeToReturn = v

        H.pop(0)
        return nodeToReturn, H

    def sortNeighbors(self, neighbors: list) -> list:
        neighbors.sort(key=lambda v: v.length, reverse=True)
        return neighbors
