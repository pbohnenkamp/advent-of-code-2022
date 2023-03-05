from sys import stdin

from src.TunnelNetwork import TunnelNetwork

if __name__ == '__main__':
    lines = stdin.readlines()
    tunnel_network = TunnelNetwork(lines)
    max_release_alone, ordered_list = tunnel_network.find_max_flow_alone()
    print(f'The maximum pressure that can be released alone is {max_release_alone}')
    print(f'With the set of nodes: {tunnel_network.nodes_to_node_names(ordered_list)}')
    # this next line takes almost 10 minutes to finish, but it does!
    max_release_with_help, help_lists = tunnel_network.find_max_flow_with_elephant()

    print(f'The maximum pressure that can be released with elephant help is {max_release_with_help}\nWith node sets:')
    print(f'({tunnel_network.nodes_to_node_names(help_lists[0])}), ({tunnel_network.nodes_to_node_names(help_lists[1])})')