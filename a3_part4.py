"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 4 of this assignment. You may, but are not required to, add doctest
examples to help test your work. We strongly encourage you to do so!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mario Badr and David Liu.
"""
import random
from typing import Optional

# from python_ta.contracts import check_contracts

# NOTE: Node and NodeAddress must be imported for check_contracts
# to work correctly, even if they aren't being used directly in this
# module. Don't remove them (even if you get a warning about them in PyCharm)!
from a3_network import Channel, NodeAddress, Node, Packet
from a3_part1 import AbstractRing, AbstractTorus, AbstractStar


# @check_contracts
class GreedyChannelRing(AbstractRing):
    """An implementation of the Greedy-Channel Ring Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        channels = []
        node = self._nodes[current_address]

        for neighbour_address in node.channels:
            shortest_path = self.get_distance(neighbour_address, packet.destination)
            connected_channel = node.channels[neighbour_address]
            channels.append((shortest_path, connected_channel))

        return greedy_channel_select(channels)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        if n1 == n2:
            return 0

        radix = len(self._nodes)
        path_one_len = 0
        path_two_len = 0

        if n1 < n2:
            path_one_len = n2 - n1
            path_two_len = radix - (n2 - n1)
        elif n1 > n2:
            path_one_len = radix - (n1 - n2)
            path_two_len = n1 - n2

        if path_one_len <= path_two_len:
            return path_one_len

        else:
            return path_two_len


# @check_contracts
class GreedyChannelTorus(AbstractTorus):
    """An implementation of the Greedy-Channel Torus Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        channels = []
        node = self._nodes[current_address]

        for neighbour_address in node.channels:
            shortest_path = self.get_distance(neighbour_address, packet.destination)
            connected_channel = node.channels[neighbour_address]
            channels.append((shortest_path, connected_channel))

        return greedy_channel_select(channels)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        if n1 == n2:
            return 0

        radix = len(self._nodes) ** 0.5
        h1 = n1[0]
        h2 = n2[0]
        v1 = n1[1]
        v2 = n2[1]

        # dimension 1
        if h1 < h2:
            path_one_len = h2 - h1
            path_two_len = radix - (h2 - h1)
        else:
            path_one_len = radix - (h1 - h2)
            path_two_len = h1 - h2

        if path_one_len <= path_two_len:
            horizontal_path_len = path_one_len

        else:
            horizontal_path_len = path_two_len

        # dimension 2
        if v1 < v2:
            path_one_len = v2 - v1
            path_two_len = radix - (v2 - v1)
        else:
            path_one_len = radix - (v1 - v2)
            path_two_len = v1 - v2

        if path_one_len <= path_two_len:
            vertical_path_len = path_one_len

        else:
            vertical_path_len = path_two_len

        return int(horizontal_path_len + vertical_path_len)


# @check_contracts
class GreedyChannelStar(AbstractStar):
    """An implementation of the Greedy-Channel Star Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        channels = []
        node = self._nodes[current_address]

        for neighbour_address in node.channels:
            shortest_path = self.get_distance(neighbour_address, packet.destination)
            connected_channel = node.channels[neighbour_address]
            channels.append((shortest_path, connected_channel))

        return greedy_channel_select(channels)

    def get_distance(self, n1: NodeAddress, n2: NodeAddress) -> int:
        """Return the shortest path distance between the two given node (addresses).

        Remember that path distance is measured as the number of channels/edges, not nodes.
        When n1 == n2, the shortest path distance is 0.

        Preconditions:
            - n1 in self._nodes
            - n2 in self._nodes
        """
        if n1 == n2:
            return 0

        elif n1 <= self._num_central - 1 or n2 <= self._num_central - 1:
            return 1

        else:
            return 2


# @check_contracts
def greedy_channel_select(channels: list[tuple[int, Channel]]) -> Channel:
    """Return the channel that minimizes the quantity described under "Greedy Channel Routing Algorithn"
    on the assignment handout.

    Each tuple in channels is of the form (d, channel), where d is the shortest-path distance
    from the neighbour to the packet's destination, and channel is the channel to that neighbour.

    Break ties as described on the assignment handout.

    Preconditions:
    - channels != []
    - all(tup[0] >= 0 for tup in channels)
    """
    # set the min score as the first neighbour's
    channel_tuple_selected = channels[0]
    min_neighbour_score_so_far = channel_tuple_selected[0] + channel_tuple_selected[1].total_occupancy()
    possible_ties = [channel_tuple_selected]

    # each channel is a tuple
    for channel_tuple in channels:
        channel = channel_tuple[1]
        shortest_path_distance = channel_tuple[0]
        occupancy = channel.total_occupancy()
        score = shortest_path_distance + occupancy

        if score < min_neighbour_score_so_far:
            min_neighbour_score_so_far = score
            channel_tuple_selected = channel_tuple
            possible_ties = [channel_tuple_selected]

        # if their scores are the same, add the possible tuple
        elif score == min_neighbour_score_so_far:
            possible_ties.append(channel_tuple)

    if len(possible_ties) == 1:
        chosen_neighbour_channel = possible_ties[0][1]
        return chosen_neighbour_channel

    # first tie
    channel_tuple_selected = possible_ties[0]
    min_shortest_path_so_far = channel_tuple_selected[0]
    possible_path_ties = [channel_tuple_selected]
    for channel_tuple in possible_ties:
        shortest_path_distance = channel_tuple[0]

        if shortest_path_distance < min_shortest_path_so_far:
            min_shortest_path_so_far = shortest_path_distance
            channel_tuple_selected = channel_tuple
            possible_path_ties = [channel_tuple_selected]

        elif shortest_path_distance == min_shortest_path_so_far:
            possible_path_ties.append(channel_tuple)

    if len(possible_path_ties) == 1:
        chosen_neighbour_channel = possible_path_ties[0][1]
        return chosen_neighbour_channel

    # second tie
    chosen_neighbour_channel = random.choice(possible_path_ties)[1]
    return chosen_neighbour_channel


###################################################################################################
# Question 2
###################################################################################################
# @check_contracts
class GreedyPathRing(AbstractRing):
    """An implementation of the Greedy-Path Ring Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        all_paths = self.find_paths(current_address, packet.destination)
        return greedy_path_select(all_paths)


# @check_contracts
class GreedyPathTorus(AbstractTorus):
    """An implementation of the Greedy-Path Torus Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        all_paths = self.find_paths(current_address, packet.destination)
        return greedy_path_select(all_paths)


# @check_contracts
class GreedyPathStar(AbstractStar):
    """An implementation of the Greedy-Path Star Network.
    """

    def route_packet(self, current_address: NodeAddress, packet: Packet) -> Optional[Channel]:
        """Return the channel that the packet should traverse next, given that it has
        just arrived at the node with address current_address.

        That is, the returned channel has the node corresponding to current_address as
        one of its endpoints. Ideally, but not necessarily, traversing the returned channel
        helps get the given packet closer to its destination.

        Return None if the current_address is equal to the packet's destination!

        Preconditions:
        - current_address in self._nodes
        - packet.source in self._nodes
        - packet.destination in self._nodes
        """
        if current_address == packet.destination:
            return None

        all_paths = self.find_paths(current_address, packet.destination)
        return greedy_path_select(all_paths)


# @check_contracts
def greedy_path_select(paths: list[list[Channel]]) -> Channel:
    """Return the first channel in the path that minimizes the quantity described under "Greedy Path Routing Algorithn"
    on the assignment handout.

    Break ties as described on the assignment handout.

    Preconditions:
    - paths != []
    - every element of paths is a valid path
    - every path in paths starts at the same node
    - every path in paths ends at the same node
    """
    # set the min path score as the first path's
    path_selected = paths[0]
    min_path_score = compute_path_score(path_selected)
    possible_ties = [path_selected]

    for path in paths:
        path_score = compute_path_score(path)
        if path_score < min_path_score:
            min_path_score = path_score
            path_selected = path
            possible_ties = [path]

        elif path_score == min_path_score:
            possible_ties.append(path)

    if len(possible_ties) == 1:
        return path_selected[0]

    # first tie
    path_selected = possible_ties[0]
    min_length = len(path_selected)
    possible_length_ties = [path_selected]

    for path in possible_ties:
        if len(path) < min_length:
            min_length = len(path)
            path_selected = path
            possible_length_ties = [path_selected]
        elif len(path) == min_length:
            possible_length_ties.append(path)

    if len(possible_length_ties) == 1:
        return path_selected[0]

    # second tie
    path_selected = random.choice(possible_length_ties)
    return path_selected[0]


# @check_contracts
def compute_path_score(path: list[Channel]) -> int:
    """Return the "Greedy Path Routing Algorithm" path score for the given path.

    See assignment handout for details.

    Preconditions:
        - path is a valid path
        - path != []
    """
    k = len(path)
    path_score = k

    for i in range(0, k):
        channel = path[i]
        path_score += max(channel.total_occupancy() - i, 0)

    return path_score


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['random', 'a3_network', 'a3_part1'],
    #     'disable': ['unused-import']
    # })
