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


class ArrayQueue:
    nodes = []

    def insert(self, node):
        self.nodes.append(node)

    def deleteMin(self):
        nodeToReturn = self.nodes[0]
        self.nodes.remove(nodeToReturn)
        return nodeToReturn

    def findV(self, nodeID):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == nodeID:
                return i
        return None  # this is bad


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

        priorityQueue = ArrayQueue()
        sourceNode = None

        for vertex in range(len(self.network.nodes)):
            if self.network.nodes[vertex].node_id == srcIndex:
                sourceNode = makeNode(self.network.nodes[vertex].node_id, self.network.nodes[vertex].node_id, 0)
            else:
                node = makeNode(self.network.nodes[vertex].node_id, -1, 10000)
                priorityQueue.insert(node)

        priorityQueue.nodes.insert(0, sourceNode)

        while priorityQueue.nodes:
            u = priorityQueue.deleteMin()
            print(f"Popped: {u.id}")
            neighbors = self.network.nodes[u.id].neighbors
            print(f"Neighbors for {u.id}: {neighbors}")
            for v in neighbors:
                # Find where v lives in the priority queue
                vIndex = priorityQueue.findV(v.dest.node_id)
                if vIndex is not None:
                    combinedDistanceOfUandV = u.dist + v.length
                    if priorityQueue.nodes[vIndex].dist > combinedDistanceOfUandV:
                        # Update the node that we're visiting
                        priorityQueue.nodes[vIndex].dist = combinedDistanceOfUandV
                        priorityQueue.nodes[vIndex].prev = u

                        # Move the node we are visiting to the front of the priority queue
                        priorityQueue.nodes.insert(0, priorityQueue.nodes.pop(vIndex))

        t2 = time.time()
        return t2 - t1
