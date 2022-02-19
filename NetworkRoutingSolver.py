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

    def deletemin(self):
        return self.nodes.pop()


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
        priorityQueue.listOfNodes = []

        for vertex in range(len(self.network.nodes)-1):
            if self.network.nodes[vertex].node_id == srcIndex:
                node = makeNode(self.network.nodes[vertex].node_id, self.network.nodes[vertex].node_id, 0)
                priorityQueue.insert(node)

            else:
                node = makeNode(self.network.nodes[vertex].node_id, -1, 10000)
                priorityQueue.insert(node)

        while priorityQueue.nodes:  # checks to see if it's empty
            u = priorityQueue.deletemin()
            for v in self.network.nodes[u.id]:
                newDistance = priorityQueue.nodes[u].dist + v.length
                if newDistance < priorityQueue.nodes[v].dist:
                    priorityQueue.nodes[v].dist = newDistance
                    priorityQueue.nodes[v].prev = u

        t2 = time.time()
        return t2 - t1
