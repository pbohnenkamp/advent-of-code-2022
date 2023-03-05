import unittest

from day16_proboscidea_volcanium.src.TunnelNetwork import TunnelNetwork, Node


class TestTunnelNetwork(unittest.TestCase):
    def test_node(self):
        node_a1 = Node('AA')
        node_a2 = Node('AA')
        self.assertEqual(node_a1, node_a2)
        node_set = {node_a1, node_a2}
        self.assertIn(node_a1, node_set)
        self.assertIn(node_a2, node_set)

    def test_parse_input(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        tunnel_network = TunnelNetwork(lines)
        fo.close()
        self.assertIn('AA', tunnel_network.nodes_map)
        self.assertIn('BB', tunnel_network.nodes_map)
        self.assertIn('CC', tunnel_network.nodes_map)
        self.assertIn('DD', tunnel_network.nodes_map)
        self.assertIn('EE', tunnel_network.nodes_map)
        self.assertIn('FF', tunnel_network.nodes_map)
        self.assertIn('GG', tunnel_network.nodes_map)
        self.assertIn('HH', tunnel_network.nodes_map)
        self.assertIn('II', tunnel_network.nodes_map)
        self.assertIn('JJ', tunnel_network.nodes_map)
        self.assertEqual(tunnel_network.nodes_map['AA'].flow_rate, 0)
        self.assertEqual(tunnel_network.nodes_map['BB'].flow_rate, 13)
        self.assertEqual(tunnel_network.nodes_map['CC'].flow_rate, 2)
        self.assertEqual(tunnel_network.nodes_map['DD'].flow_rate, 20)
        self.assertEqual(tunnel_network.nodes_map['EE'].flow_rate, 3)
        self.assertEqual(tunnel_network.nodes_map['FF'].flow_rate, 0)
        self.assertEqual(tunnel_network.nodes_map['GG'].flow_rate, 0)
        self.assertEqual(tunnel_network.nodes_map['HH'].flow_rate, 22)
        self.assertEqual(tunnel_network.nodes_map['II'].flow_rate, 0)
        self.assertEqual(tunnel_network.nodes_map['JJ'].flow_rate, 21)
        self.assertIn(tunnel_network.nodes_map['DD'], tunnel_network.nodes_map['AA'].connections)
        self.assertIn(tunnel_network.nodes_map['II'], tunnel_network.nodes_map['AA'].connections)
        self.assertIn(tunnel_network.nodes_map['BB'], tunnel_network.nodes_map['AA'].connections)
        self.assertIn(tunnel_network.nodes_map['CC'], tunnel_network.nodes_map['BB'].connections)
        self.assertIn(tunnel_network.nodes_map['AA'], tunnel_network.nodes_map['BB'].connections)
        self.assertIn(tunnel_network.nodes_map['DD'], tunnel_network.nodes_map['CC'].connections)
        self.assertIn(tunnel_network.nodes_map['BB'], tunnel_network.nodes_map['CC'].connections)
        self.assertIn(tunnel_network.nodes_map['AA'], tunnel_network.nodes_map['DD'].connections)
        self.assertIn(tunnel_network.nodes_map['CC'], tunnel_network.nodes_map['DD'].connections)
        self.assertIn(tunnel_network.nodes_map['EE'], tunnel_network.nodes_map['DD'].connections)
        self.assertIn(tunnel_network.nodes_map['DD'], tunnel_network.nodes_map['EE'].connections)
        self.assertIn(tunnel_network.nodes_map['FF'], tunnel_network.nodes_map['EE'].connections)
        self.assertIn(tunnel_network.nodes_map['EE'], tunnel_network.nodes_map['FF'].connections)
        self.assertIn(tunnel_network.nodes_map['GG'], tunnel_network.nodes_map['FF'].connections)
        self.assertIn(tunnel_network.nodes_map['FF'], tunnel_network.nodes_map['GG'].connections)
        self.assertIn(tunnel_network.nodes_map['HH'], tunnel_network.nodes_map['GG'].connections)
        self.assertIn(tunnel_network.nodes_map['GG'], tunnel_network.nodes_map['HH'].connections)
        self.assertIn(tunnel_network.nodes_map['AA'], tunnel_network.nodes_map['II'].connections)
        self.assertIn(tunnel_network.nodes_map['JJ'], tunnel_network.nodes_map['II'].connections)
        self.assertIn(tunnel_network.nodes_map['II'], tunnel_network.nodes_map['JJ'].connections)

    def test_split_set(self):
        orig_set = {Node('A'), Node('B'), Node('C')}
        tunnel_network = TunnelNetwork([])
        new_sets = tunnel_network.split_valve_sets(set(), orig_set, len(orig_set) // 2)
        self.assertEqual(3, len(new_sets))

        orig_set.add(Node('D'))
        new_sets = tunnel_network.split_valve_sets(set(), orig_set, len(orig_set) // 2)
        self.assertEqual(7, len(new_sets))

        orig_set.add(Node('E'))
        new_sets = tunnel_network.split_valve_sets(set(), orig_set, len(orig_set) // 2)
        self.assertEqual(15, len(new_sets))

    def test_split_valves_all_ways(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        tunnel_network = TunnelNetwork(lines)
        fo.close()
        split_sets = tunnel_network.split_valves_all_ways()
        self.assertEqual(((2**6)/2)-1, len(split_sets))
        for split_set in split_sets:
            print(f'({tunnel_network.nodes_to_node_names(split_set[0])}), ({tunnel_network.nodes_to_node_names(split_set[1])})')

    def test_max_flow_alone(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        tunnel_network = TunnelNetwork(lines)
        fo.close()
        max_flow = tunnel_network.find_max_flow_alone()[0]
        self.assertEqual(1651, max_flow)
        print(f'Total traversal count: {tunnel_network.total_graph_traversal_count}')

    def test_max_flow_with_elephant(self):
        fo = open('../sample_input.txt', 'r')
        lines = fo.readlines()
        tunnel_network = TunnelNetwork(lines)
        fo.close()
        max_flow, ordered_list = tunnel_network.find_max_flow_with_elephant()
        self.assertEqual(1707, max_flow)
        print(f'Total traversal count: {tunnel_network.total_graph_traversal_count}')
        tunnel_network.print_node_tuples(ordered_list)
        print(f'Entries in calculated paths: {len(tunnel_network.node_tuple_calcs)}')


if __name__ == '__main__':
    unittest.main()
