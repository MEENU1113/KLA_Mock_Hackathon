import networkx as nx
import json

def parse_input(input_data):
    distances = {}
    neighborhoods = input_data.get("neighbourhoods", {})
    for n_id, n_info in neighborhoods.items():
        distances[n_id] = n_info["distances"]

    return distances

def tsp_solver(distance_matrix, start_node):
    graph = nx.Graph()
    for node, distances in distance_matrix.items():
        for other_node, distance in enumerate(distances):
            if node != other_node:
                graph.add_edge(node, f"n{other_node}", weight=distance)

    
    tsp_path = nx.approximation.greedy_tsp(graph, source=start_node)

    return tsp_path

def format_output(tsp_path):
    output = {"v0": {"path": tsp_path}}
    return output

if __name__ == "__main__":
    input_file_path = "C:\\Users\\Administrator\\Documents\\KLA_Mock_Hackathon\\level 0\\level0.json" 
    with open(input_file_path, 'r') as f:
        input_data = json.load(f)
    
    
    start_node = "n0"

    distance_matrix = parse_input(input_data)
    tsp_path = tsp_solver(distance_matrix, start_node)
    output_data = format_output(tsp_path)

    print(output_data)


    output_path = 'level0_output.json'
    with open(output_path, 'w') as output_file:
        json.dump(output_data, output_file)

    print(f"Output saved to {output_path}")
