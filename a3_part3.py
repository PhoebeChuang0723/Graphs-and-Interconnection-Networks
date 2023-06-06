"""CSC111 Winter 2023 Assignment 3: Graphs and Interconnection Networks

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 3 of this assignment. You may, but are not required to, add doctest
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
import csv
from typing import Optional

import plotly.graph_objects as go

# from python_ta.contracts import check_contracts

# NOTE: Node and NodeAddress must be imported for check_contracts
# to work correctly, even if they aren't being used directly in this
# module. Don't remove them (even if you get a warning about them in PyCharm)!
from a3_network import AbstractNetwork, Packet, NodeAddress, Node
from a3_simulation import NetworkSimulation, PacketStats

# The different networks you're implementing on this assignment. Don't worry if
# the a3_part4 networks are unused right now; you'll use them in this file after
# completing Part 4.
from a3_part2 import AlwaysRightRing, ShortestPathRing, ShortestPathTorus, ShortestPathStar
from a3_part4 import GreedyChannelRing, GreedyChannelTorus, GreedyChannelStar, \
    GreedyPathRing, GreedyPathTorus, GreedyPathStar


def run_example() -> list[PacketStats]:
    """Run an example simulation.

    You may, but are not required to, change the code in this example to experiment with the simulation.
    """
    network = AlwaysRightRing(5)
    simulation = NetworkSimulation(network)
    packets = [(0, Packet(1, 0, 4))]
    return simulation.run_with_initial_packets(packets, print_events=True)


# @check_contracts
def read_packet_csv(csv_file: str) -> tuple[AbstractNetwork, list[tuple[int, Packet]]]:
    """Load network and packet data from a CSV file.

    Return a tuple of two values:
        - the first element is the network created from the specification in the first line
          of the CSV file
        - the second element is a list of tuples, where each tuple is of the form (timestamp, packet),
          created from all other lines of the CSV file

    Preconditions:
        - csv_file refers to a valid CSV file in the format described on the assignment handout

    Implementation hints:
        - Since it's the last assignment, we've deliberately not given you *any* startter code
          for reading CSV files! Refer back to past assignments/tutorials. Hint: treat the first
          line differently than all other lines.
        - You *may* use a big if statement to handle each different network type separately.
        - Remember to convert entries into ints where appropriate.
    """
    packet_list = []
    with open(csv_file) as selected_file:
        reader = csv.reader(selected_file)
        network_info = next(reader)

        if network_info[0] == 'AlwaysRightRing':
            network = AlwaysRightRing(int(network_info[1]))
        elif network_info[0] == 'ShortestPathRing':
            network = ShortestPathRing(int(network_info[1]))
        elif network_info[0] == 'ShortestPathTorus':
            network = ShortestPathTorus(int(network_info[1]))
        elif network_info[0] == 'ShortestPathStar':
            network = ShortestPathStar(int(network_info[1]), int(network_info[2]))
        elif network_info[0] == 'GreedyChannelRing':
            network = GreedyChannelRing(int(network_info[1]))
        elif network_info[0] == 'GreedyChannelTorus':
            network = GreedyChannelTorus(int(network_info[1]))
        elif network_info[0] == 'GreedyChannelStar':
            network = GreedyChannelStar(int(network_info[1]), int(network_info[2]))
        elif network_info[0] == 'GreedyPathRing':
            network = GreedyPathRing(int(network_info[1]))
        elif network_info[0] == 'GreedyPathTorus':
            network = GreedyPathTorus(int(network_info[1]))
        elif network_info[0] == 'GreedyPathStar':
            network = GreedyPathStar(int(network_info[1]), int(network_info[2]))
        else:
            network = None

        identifier = 0
        for row in reader:
            timestamp = int(row[0])
            if network_info[0] != 'ShortestPathTorus' and network_info[0] != 'GreedyChannelTorus' and \
                    network_info[0] != 'GreedyPathTorus':
                source = int(row[1])
                destination = int(row[2])
            else:
                source = (int(row[1]), int(row[2]))
                destination = (int(row[3]), int(row[4]))

            packet = Packet(identifier, source, destination)
            packet_list.append((timestamp, packet))
            identifier += 1

        return (network, packet_list)


def plot_packet_latencies(packet_stats: list[PacketStats]) -> None:
    """Use plotly to plot a histogram of the packet latencies for the given stats.

    The packet latency is defined as the difference between the arrived_at and created_at times.
    It represents the total amount of time the packet spent in the network.

    We have provided some starter code for you.

    Preconditions:
        - packet_stats != []
        - all(stats.arrived_at is not None for stats in packet_stats)
    """
    packet_latencies_list = []
    for packet in packet_stats:
        latency = packet.arrived_at - packet.created_at
        packet_latencies_list.append(latency)

    fig = go.Figure(data=[
        go.Histogram(
            x=packet_latencies_list,
        )
    ])
    # Set the graph title and axis labels
    fig.update_layout(
        title='Packet Latency Histogram',
        xaxis_title_text='Packet Latency',
        yaxis_title_text='Count'
    )
    fig.show()


def plot_route_lengths(packet_stats: list[PacketStats]) -> None:
    """Use plotly to plot a histogram of the route lengths for the given stats.

    The route length is defined as the number of channels traversed by the packet to arrive at its destination.

    We have not provided any code, but your implementation should be pretty similar to plot_packet_latencies.
    Remember to update the histogram title and axis labels!

    Preconditions:
        - packet_stats != []
        - all(stats.route != [] for stats in packet_stats)
    """
    packet_route_lengths_list = []
    for packet in packet_stats:
        route_length = len(packet.route) - 1
        packet_route_lengths_list.append(route_length)

    fig = go.Figure(data=[
        go.Histogram(
            x=packet_route_lengths_list,
        )
    ])
    # Set the graph title and axis labels
    fig.update_layout(
        title='Packet Route Length Histogram',
        xaxis_title_text='Packet Route Length',
        yaxis_title_text='Count'
    )
    fig.show()


# @check_contracts
def part3_runner(csv_file: str, plot_type: Optional[str] = None) -> dict[str, float]:
    """Run a simulation based on the data from the given csv file.

    If plot_type == 'latencies', plot a histogram of the packet latencies.
    If plot_type == 'route-lengths', plot a histogram of the packet route lengths.

    Return a dictionary with two keys:
        - 'average latency', whose associated value is the average packet latency
        - 'average route length', whose associated value is the average route length

    Preconditions:
        - csv_file refers to a valid CSV file in the format described on the assignment handout
        - plot_type in {None, 'latencies', 'route-lengths'}
    """
    network_tuple = read_packet_csv(csv_file)
    packet_stats = NetworkSimulation(network_tuple[0]).run_with_initial_packets(network_tuple[1])

    if plot_type == 'latencies':
        plot_packet_latencies(packet_stats)

    elif plot_type == 'route-lengths':
        plot_route_lengths(packet_stats)

    else:
        pass

    latency_sum = 0
    route_length_sum = 0
    num_packet = len(packet_stats)

    for packet in packet_stats:
        latency_sum += packet.arrived_at - packet.created_at
        route_length_sum += (len(packet.route) - 1)

    return {
        'average latency': latency_sum / num_packet,
        'average route length': route_length_sum / num_packet
    }


# @check_contracts
# def part3_runner_optional(network: AbstractNetwork, plot_type: Optional[str] = None) -> dict[str, float]:
#     """An optional runner. You may use this function to experiment with using
#     a3_simulation.generate_random_initial_events, for example. You may modify
#     the function header (e.g., by adding parameters or changing the return type)
#     however you like.
#
#     Your work in this function will not be graded (though it will still be checked
#     by PythonTA).
#     """
#     return {
#         'average latency': ...,
#         'average route length': ...
#     }


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    # Here is a sample call to part3_runner. Feel free to change it or add new calls!
    part3_runner('data/star_small.csv', 'latencies')

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['csv', 'plotly.graph_objects', 'a3_network', 'a3_simulation', 'a3_part2', 'a3_part4'],
    #     'disable': ['unused-import', 'too-many-branches'],
    #     'allowed-io': ['read_packet_csv', 'part3_runner_optional']
    # })
