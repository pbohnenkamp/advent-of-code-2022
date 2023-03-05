import re
from sys import maxsize


class Node:
    def __init__(self, name, flow_rate=0) -> None:
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.connections: set['Node'] = set()

    def add_connection(self, other_node: 'Node') -> None:
        self.connections.add(other_node)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False

        return o.name == self.name

    def __hash__(self):
        return hash(self.name)


class TunnelNetwork:
    def __init__(self, network_input_lines) -> None:
        self.nodes_map: dict[str, Node] = {}
        self.node_distances_map: dict[str, dict[str, int]] = {}
        self.total_graph_traversal_count = 0
        self.node_tuple_calcs: dict[((Node, Node), (int, int), list[str]): (int, list[Node, Node])] = {}
        self._parse_network(network_input_lines)

    def find_max_flow_alone(self):
        self._create_root_and_value_distance_matrix()
        return self._calc_max_flow(self._find_start_node(), self.get_all_working_valve_nodes(), 0)

    def find_max_flow_with_elephant(self):
        self._create_root_and_value_distance_matrix()
        # We have a set of all valves that can release pressure. It seems to reason if I
        # break up that set into all possible ways to make two distinct sets, one for me
        # and one for the elephant, and iterate through calculating the sum of the max flow for
        # each set and then taking the max value of that iteration, I will get the max flow
        # with the help of an elephant
        print('Calculating splits')
        all_distinct_split_sets: list[(set[Node], set[Node])] = self.split_valves_all_ways()
        count_of_distinct_sets = len(all_distinct_split_sets)
        print(f'Finding max of {count_of_distinct_sets} split sets')
        start_node = self._find_start_node()

        max_tuple = None
        max_flow = 0
        percent_done = 0
        for count, split_set in enumerate(all_distinct_split_sets):
            if count_of_distinct_sets % (count_of_distinct_sets // 100) == 0:
                percent_done += 10
            my_flow, my_nodes = self._calc_max_flow(start_node, split_set[0], 0, max_time=26)
            elephant_flow, elephant_nodes = self._calc_max_flow(start_node, split_set[1], 0, max_time=26)
            current_max_flow = my_flow + elephant_flow
            if current_max_flow > max_flow:
                max_flow = current_max_flow
                max_tuple = (my_nodes, elephant_nodes)
        print(f'Max flow: {max_flow}')
        print(f'({self.nodes_to_node_names(max_tuple[0])}), ({self.nodes_to_node_names(max_tuple[1])})')

        return max_flow, max_tuple

    def _parse_network(self, lines):
        for line in lines:
            self._parse_network_line(line)

    def _parse_network_line(self, line):
        line = line.strip()
        [node_name, flow_rate, connection_list] = re.search(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]*)", line).groups()
        current_node = self._find_or_create_node(node_name)
        current_node.flow_rate = int(flow_rate)
        for connection in connection_list.split(', '):
            current_node.add_connection(self._find_or_create_node(connection))

    def _find_or_create_node(self, node_name):
        if node_name in self.nodes_map:
            return self.nodes_map[node_name]
        else:
            new_node = Node(node_name)
            self.nodes_map[node_name] = new_node
            return new_node

    def _create_root_and_value_distance_matrix(self):
        # Version of Dijkstra's algorithm to find the shortest path to all the other nodes from each node

        # Dictionary to hold the results
        distances_matrix: dict[str, dict[str, int]] = {}

        # Outer loop uses every node as the source node
        for source_node in self.nodes_map.values():
            # This is where Dijkstra's algorithm starts
            distances: dict[str, int] = {}
            prev: dict[str, Node | None] = {}
            unvisited_nodes = set()
            # initialize the matrices used by the algorithm
            for target in self.nodes_map.values():
                # distances start at infinity
                distances[target.name] = maxsize
                # previous starts with none
                prev[target.name] = None
                # unvisited nodes start with all nodes
                unvisited_nodes.add(target)
            # correct the distance from the source to itself
            distances[source_node.name] = 0

            while len(unvisited_nodes) > 0:
                # choose the nodes from the distance map that are in the unvisited nodes set and sort them by distance
                name_dist_tuples = [name_dist_tuple for name_dist_tuple in distances.items() if
                                    name_dist_tuple[0] in [node.name for node in unvisited_nodes]]
                # sort them by distance
                name_dist_tuples.sort(key=lambda name_dist_tuple: name_dist_tuple[1])
                # get the corresponding node from the unvisited set from the name of the first tuple
                least_distance_node = None
                for unvisited_node in unvisited_nodes:
                    if unvisited_node.name == name_dist_tuples[0][0]:
                        least_distance_node = unvisited_node
                        break
                unvisited_nodes.remove(least_distance_node)

                # for all the neighbors of least_distance_node that haven't been visited yet
                for unvisited_neighbor in [neighbor for neighbor in least_distance_node.connections if
                                           neighbor in unvisited_nodes]:
                    # calculate the distance to this neighbor
                    # since all the distances between nodes is 1 minute, just add 1
                    alt_dist = distances[least_distance_node.name] + 1
                    # if the new distance is less than the old
                    if alt_dist < distances[unvisited_neighbor.name]:
                        # use it
                        distances[unvisited_neighbor.name] = alt_dist
                        # track the path
                        prev[unvisited_neighbor.name] = least_distance_node

            # we now should have the min distances from the source node to all other nodes in the distance map
            # Add it to the matrix
            distances_matrix[source_node.name] = distances

        # The matrix should be populated now
        # Remove the non valve nodes excluding AA and account for opening the valve for the others
        rows_to_del = []
        for k_row in distances_matrix:
            if self.nodes_map[k_row].flow_rate > 0 or k_row == "AA":
                cols_to_del = []
                for k_col in distances_matrix[k_row]:
                    if self.nodes_map[k_col].flow_rate > 0 or k_col == "AA":
                        if distances_matrix[k_row][k_col] > 0:
                            distances_matrix[k_row][k_col] += 1
                    else:
                        cols_to_del.append((k_row, k_col))
                for col_to_del in cols_to_del:
                    del distances_matrix[col_to_del[0]][col_to_del[1]]
            else:
                rows_to_del.append(k_row)
        for row_to_del in rows_to_del:
            del distances_matrix[row_to_del]

        self._print_valve_nodes(self.nodes_map)
        self.print_distance_matrix(distances_matrix)
        self.node_distances_map = distances_matrix

    def _find_start_node(self):
        return self.nodes_map['AA']

    def _find_valve_nodes(self):
        return [node for node in self.nodes_map.values() if node.flow_rate > 0]

    @staticmethod
    def print_distance_matrix(distances_matrix: dict[str, dict[str, int]]):
        # Print the top label row
        top_row = "    "
        for key in sorted(distances_matrix.keys()):
            top_row += key + "  "
        print(top_row)
        for row_key in sorted(distances_matrix.keys()):
            row = row_key + "  "
            for col_key in sorted(distances_matrix[row_key].keys()):
                if distances_matrix[row_key][col_key] == maxsize:
                    row += "X   "
                else:
                    row += str(distances_matrix[row_key][col_key]).ljust(4, " ")

            print(row)

    def _calc_max_flow(self, current_node, working_valve_nodes, minutes_elapsed, visited_valves=None, max_time=30):
        if visited_valves is None:
            visited_valves = set()

        # check to see that minutes elapsed hasn't passed max time
        if minutes_elapsed >= max_time:
            return 0, []

        # push this node on the visited set
        visited_valves.add(current_node)

        # get all the valve nodes minus the visited ones
        valves_to_turn_on = self.get_unvisited_valve_nodes(visited_valves, working_valve_nodes)

        if len(valves_to_turn_on) > 0:
            # if more than 1 left
            # sort them by highest potential first. Potential = (time_remaining - dist_to_child) * child_flow
            valves_sorted_by_potential = self.sort_by_potential(valves_to_turn_on, current_node,
                                                                minutes_elapsed, max_time)
            # for each sorted child
            current_max_flow = 0
            max_flow_ordered_list = []
            for valve_node in valves_sorted_by_potential:
                self.total_graph_traversal_count += 1
                # _calc_max_flow of child with this node and new time_elapsed
                flow, ordered_node_list = self._calc_max_flow(valve_node, working_valve_nodes,
                                                              minutes_elapsed +
                                                              self.node_distances_map[current_node.name][
                                                                  valve_node.name], visited_valves, max_time=max_time)
                if flow > current_max_flow:
                    current_max_flow = flow
                    max_flow_ordered_list = ordered_node_list

            # pop this node from visited set
            visited_valves.remove(current_node)
            max_flow_ordered_list.insert(0, current_node)
            # return the highest max flow of the children plus this nodes
            return current_max_flow + self._calculate_flow_from_valve_at_time(max_time, current_node,
                                                                              minutes_elapsed), max_flow_ordered_list
        else:
            self.total_graph_traversal_count += 1
            # last node
            # pop this node from visited set
            visited_valves.remove(current_node)
            # return flow = (30 - time_elapsed) * flow
            return self._calculate_flow_from_valve_at_time(max_time, current_node, minutes_elapsed), [current_node]

    def split_valves_all_ways(self):
        # first get all valves with flow
        all_valves = set(self.get_all_working_valve_nodes())

        # split them into all combinations of 2 sets
        split_sets = self.split_valve_sets(set(), all_valves, len(all_valves) // 2)
        return split_sets

    def split_valve_sets(self, left: set, right: set, max_len_left, running_split_sets=None):
        if running_split_sets is None:
            running_split_sets = []
        if len(left) < max_len_left:
            split_sets = []
            for item in right:
                new_left = left.copy()
                new_left.add(item)
                new_right = right.copy()
                new_right.remove(item)
                # we can further optimize because the max of ([a, b], [c, d]) == ([b, a], [d, c]) == ([c, d], [b, a])...
                if not self._split_set_is_duplicate((new_left, new_right), running_split_sets):
                    split_sets.append((new_left, new_right))
                    running_split_sets.append((new_left, new_right))
                    split_sets += self.split_valve_sets(new_left, new_right, max_len_left, running_split_sets)
            return split_sets
        else:
            return []

    def sort_by_potential(self, valves_to_turn_on, current_node, minutes_elapsed, max_time):
        return sorted(valves_to_turn_on, key=lambda sort_valve: (max_time - minutes_elapsed -
                                                                 self.node_distances_map[current_node.name][
                                                                     sort_valve.name]) * sort_valve.flow_rate,
                      reverse=True)

    @staticmethod
    def get_unvisited_valve_nodes(visited_valves, all_valves):
        return [valve_node for valve_node in all_valves if
                valve_node not in visited_valves]

    def get_all_working_valve_nodes(self):
        return [valve_node for valve_node in self.nodes_map.values() if
                valve_node.flow_rate > 0]

    @staticmethod
    def nodes_to_node_names(nodes):
        names = []
        for node in nodes:
            names.append(node.name)
        return names

    @staticmethod
    def print_node_tuples(node_tuples):
        for node_tuple in node_tuples:
            print(f'{node_tuple[0].name}({node_tuple[0].flow_rate}), {node_tuple[1].name}({node_tuple[1].flow_rate})')

    @staticmethod
    def _print_valve_nodes(nodes_map):
        for (node_name, node) in sorted(nodes_map.items(), key=lambda item: item[0]):
            if node.flow_rate > 0:
                print(f'{node_name}: {node.flow_rate}')

    @staticmethod
    def _split_set_is_duplicate(split_set, existing_split_sets: list[tuple[set[Node], set[Node]]]):
        for existing_split_set in existing_split_sets:
            if set(existing_split_set[0]) == set(split_set[0]) and set(existing_split_set[1]) == set(split_set[1]):
                return True
            if set(existing_split_set[1]) == set(split_set[0]) and set(existing_split_set[0]) == set(split_set[1]):
                return True

        return False

    @staticmethod
    def _calculate_flow_from_valve_at_time(max_time, valve, minutes_elapsed):
        return (max(max_time - minutes_elapsed, 0)) * valve.flow_rate
