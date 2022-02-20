#!/usr/bin/python3


from CS312Graph import *
import time


class Node(object):
    id = -1
    prev = -1
    dist = 10000


def makeNode(id, prev, dist):
    node = Node()
    node.id = id
    node.prev = prev
    node.dist = dist
    return node


# noinspection PyMethodMayBeStatic
class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)

        # Initialize the priority queue and get the source node
        pQueue = self.initList(srcIndex)
        lookupTable = pQueue

        while pQueue:
            u, pQueue = self.deleteMin(pQueue)
            print(f"Popped: {u.id}")
            neighbors = self.network.nodes[u.id].neighbors
            print(f"Neighbors for {u.id}: {neighbors}")
            for v in neighbors:
                # Find where v lives in the priority queue
                vIndex = self.getVisitorIndex(pQueue, v.dest.node_id)

                # If v lives inside the priority queue then visit it
                if vIndex is not None:
                    combinedDistanceOfUandV = u.dist + v.length
                    if pQueue[vIndex].dist > combinedDistanceOfUandV:
                        # Update the node that we're visiting
                        pQueue[vIndex].dist = combinedDistanceOfUandV
                        pQueue[vIndex].prev = u

                        # Move the node we are visiting to the front of the priority queue
                        pQueue.insert(0, pQueue.pop(vIndex))

            #todo
            """
            currently the priority queue is getting updated, but is also getting deleted at the same time.
            All of the values are looking correct, but when the loop is finished the queue is empty.
            Just need to be able to run deleteMin and still update the table at the same time.
            Brain is tired so I need chips and salsa 👍🏽
            """


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
                sourceNode = makeNode(self.network.nodes[vertex].node_id, self.network.nodes[vertex].node_id, 0)
            else:
                node = makeNode(self.network.nodes[vertex].node_id, -1, 10000)
                H.append(node)

        H.insert(0, sourceNode)
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
    
    :returns {nodeToReturn, H} a tuple containing the popped node and the updated priority queue
    """

    def deleteMin(self, H: list) -> {Node, list}:
        nodeToReturn = H[0]
        H.remove(nodeToReturn)
        return nodeToReturn, H
