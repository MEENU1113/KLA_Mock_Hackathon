import json

def calculate_distance(point1, point2):
    return abs(point1 - point2)

def clark_wright_savings(neighbourhood, restaurant_distance, vehicle_capacity):
    orders = []

    for node, data in neighbourhood.items():
        orders.append({
            'node': node,
            'order_quantity': data['order_quantity'],
            'distances': data['distances']
        })

    savings = []
    for i, order_i in enumerate(orders):
        for j, order_j in enumerate(orders):
            if i != j:
                savings.append({
                    'order_i': order_i,
                    'order_j': order_j,
                    'savings': order_i['distances'][0] + order_j['distances'][0] - restaurant_distance[0]
                })

    savings.sort(key=lambda x: x['savings'], reverse=True)

    routes = []
    for order in orders:
        routes.append({'orders': [order], 'total_quantity': order['order_quantity'], 'total_distance': 2 * order['distances'][0]})

    for saving in savings:
        for route in routes:
            if saving['order_i'] in route['orders'] and saving['order_j'] not in route['orders']:
                if route['total_quantity'] + saving['order_j']['order_quantity'] <= vehicle_capacity:
                    route['orders'].append(saving['order_j'])
                    route['total_quantity'] += saving['order_j']['order_quantity']
                    route['total_distance'] += saving['order_j']['distances'][0]
                    break
            elif saving['order_j'] in route['orders'] and saving['order_i'] not in route['orders']:
                if route['total_quantity'] + saving['order_i']['order_quantity'] <= vehicle_capacity:
                    route['orders'].append(saving['order_i'])
                    route['total_quantity'] += saving['order_i']['order_quantity']
                    route['total_distance'] += saving['order_i']['distances'][0]
                    break

    return routes

def solve_delivery_problem(data):
    vehicles = data['vehicles']
    output = {}

    for vehicle_id, vehicle_data in vehicles.items():
        start_point = vehicle_data['start_point']
        vehicle_capacity = vehicle_data['capacity']
        speed = vehicle_data['speed']

        neighbourhood = data['neighbourhoods']
        restaurant_distance = data['restaurants'][start_point]['neighbourhood_distance']

        routes = clark_wright_savings(neighbourhood, restaurant_distance, vehicle_capacity)

        output[vehicle_id] = {'path{}'.format(i + 1): [start_point] + [order['node'] for order in route['orders']] + [start_point] for i, route in enumerate(routes)}

    return output

if __name__ == "__main__":
    # Load input data from a file
    path = 'C:\\Users\\Administrator\\Documents\\KLA_Mock_Hackathon\\level1a\\level1a.json'
    with open(path, 'r') as file:
        input_data = json.load(file)

    # Solve the delivery problem
    output_result = solve_delivery_problem(input_data)

    # Convert output to the desired format
    formatted_output = {}
    for vehicle_id, paths in output_result.items():
        formatted_output[vehicle_id] = {f'path{i + 1}': path for i, path in enumerate(paths.values())}
print(output_result)
# Output the result to a file
with open('output_result.json', 'w') as f:
    json.dump(formatted_output, f, indent=2)
