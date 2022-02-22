from abc import ABC

from QueueInterface import QueueInterface, Node


class QueueArray(QueueInterface, ABC):

    def __init__(self):
        print("Init Queue Array")

    """
    Time: O(1) | Space O(1)
    
    Return the first value inside of H
    
    :param H the incoming priority queue values
    :param lookupTable: N/a
    
    :returns {nodeToReturn, H} tuple containing the popped node and the newly updated list H
    """

    def deleteMin(self, H: list, lookupTable: list):
        nodeToReturn = H[0]
        H.pop(0)
        return nodeToReturn, H

    """
    N/A
    """

    def decreaseKey(self, nodeId, lookupTable: list):
        pass

    """
    Time: O(n) | Space: O(1)
    
    Here we take the nodes from the network {G} and parse through them to collect their individual node ids.
    We insert these ids into the list H using Node objects.
    
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
                node = self.makeNode(network[vertex].node_id, -1, 10000, network[vertex].loc)  # Time/Space: O(1)
                H.append(node)  # Time: O(1) | Space: O(1) - insert nodes into H

        return H
