"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of the classes you'll define for Part 2
of this assignment. As with Part 1, you may, but are not required to, add
doctest examples to help test your work. We strongly encourage you to do so!

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
from a3_network import Channel, Packet, NodeAddress, Node
from a3_part1 import AbstractRing, AbstractStar, AbstractTorus


# @check_contracts
class AlwaysRightRing(AbstractRing):
    """An implementation of the Always-Right Ring Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractRing and the other useful methods
    from AbstractNetwork!
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

        else:
            if current_address != len(self._nodes) - 1:
                return self._nodes[current_address].channels[current_address + 1]
            else:
                return self._nodes[current_address].channels[0]


# @check_contracts
class ShortestPathRing(AbstractRing):
    """An implementation of the Shortest-Path Ring Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractRing and the other useful methods
    from AbstractNetwork!
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
        radix = len(self._nodes)
        destination = packet.destination

        if current_address == destination:
            return None

        else:
            direction = determine_direction(current_address, destination, radix)

        if direction == 1:
            if current_address != radix - 1:
                return self._nodes[current_address].channels[current_address + 1]
            else:
                return self._nodes[current_address].channels[0]

        else:
            if current_address != 0:
                return self._nodes[current_address].channels[current_address - 1]
            else:
                return self._nodes[current_address].channels[radix - 1]


# @check_contracts
def determine_direction(current_address: NodeAddress, destination: int, radix: int) -> Optional[int]:
    """A helper function that determines the direction of the channel that the packet should be moved to.
    """
    if current_address == destination:
        return None

    elif current_address < destination:
        path_one_len = destination - current_address
        path_two_len = radix - (destination - current_address)

    else:
        path_one_len = radix - (current_address - destination)
        path_two_len = current_address - destination

    if path_one_len <= path_two_len:
        return 1

    else:
        return 2


# @check_contracts
class ShortestPathTorus(AbstractTorus):
    """An implementation of the Shortest-Path Torus Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractTorus and the other useful methods
    from AbstractNetwork!
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

        Implementation notes:
            - To determine the next node address, you'll need to recover the radix of this torus.
              There are a few different approaches for this, but if you want to calculate a square
              root, we haven't allowed you to import math.sqrt, but you can use "** 0.5" instead.
        """
        radix = int(len(self._nodes) ** 0.5)

        if current_address == packet.destination:
            return None

        else:
            direction = determine_direction(current_address[0], packet.destination[0], radix)
            left_right = True

            if direction is None:
                direction = determine_direction(current_address[1], packet.destination[1], radix)
                left_right = False

        if direction == 1 and left_right and current_address[0] != radix - 1:
            return self._nodes[current_address].channels[(current_address[0] + 1, current_address[1])]

        elif direction == 1 and left_right and current_address[0] == radix - 1:
            return self._nodes[current_address].channels[(0, current_address[1])]

        elif direction != 1 and left_right and current_address[0] != 0:
            return self._nodes[current_address].channels[(current_address[0] - 1, current_address[1])]

        elif direction != 1 and left_right and current_address[0] == 0:
            return self._nodes[current_address].channels[(radix - 1, current_address[1])]

        elif direction == 1 and not left_right and current_address[1] != radix - 1:
            return self._nodes[current_address].channels[(current_address[0], current_address[1] + 1)]

        elif direction == 1 and not left_right and current_address[1] == radix - 1:
            return self._nodes[current_address].channels[(current_address[0], 0)]

        elif direction != 1 and not left_right and current_address[1] != 0:
            return self._nodes[current_address].channels[(current_address[0], current_address[1] - 1)]

        elif direction != 1 and not left_right and current_address[1] == 0:
            return self._nodes[current_address].channels[(current_address[0], radix - 1)]

        else:
            return None


# @check_contracts
class ShortestPathStar(AbstractStar):
    """An implementation of the Shortest-Path Star Network.

    Note that you only need to implement the route_packet method for this class.
    It will inherit the initializer from AbstractStar and the other useful methods
    from AbstractNetwork!
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

        if current_address <= self._num_central - 1 or packet.destination <= self._num_central - 1:
            return self._nodes[current_address].channels[packet.destination]

        else:
            random_central_node_address = random.randint(0, self._num_central - 1)
            return self._nodes[current_address].channels[random_central_node_address]


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
