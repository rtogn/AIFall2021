import random, math


class Node:
    def __init__(self, value):
        self.value = value
		
		
def init_node_list(value_list):
    # Converts list of values into nodes. This is just to be prompt really as they only hold a heuristic value here.
    node_list = []
    for item in value_list:
        node_list.append(Node(item))
    return node_list

	
def init_temp_map(increment, iterations, start_temp, reduction):
    '''
    Creates a time to temperature dictionary based on the following parameters:
        iterations: number of iterations map will go through
        increment: number to decrement by each iteration
        start_temp: starting temperature (eg 100.0)
        reduction: value each iteration will divide by (eg, divide by half every iteration)
    Example:    print(InitTempmap(100, 1000, 100.0, 2.0))
    Output: {0: 100.0, 100: 50.0, 200: 25.0, 300: 12.5, 400: 6.25, 500: 3.125, 600: 1.5625, 700: 0.78125, 800: 0.390625, 900: 0.1953125}
    '''
    # Type conversions for ease of use.
    start_temp = float(start_temp)
    reduction = float(reduction)
    # Number of times the temp will be changed.
    temp_changes = int(iterations / increment)
    # Init current_temp to starting temperature
    current_temp = start_temp
    # set initial state of map at time 0 wtih temp 100.0.
    temp_map = {0: current_temp}
    for i in range(1, temp_changes):
        current_temp = current_temp * reduction
        temp_map[i * increment] = current_temp
    return temp_map


def get_neighbors(node, node_list):
    neighbors = []

    if not isinstance(node, Node):
        print("Object passed is not a Node")
    else:
        index = node_list.index(node)
        # Hokey way to make neighbors circular. Error thrown when last index reaches for next node.
        # Will add index -1 and then error. Except will give a reference to node 0.
        try:
            neighbors.append(node_list[index - 1])
            neighbors.append(node_list[index + 1])
        except:
            neighbors.append(node_list[0])

    return neighbors


def simulated_annealing(temp_schedule, iterations, value_list, initial_state):
    '''
    Run simulated annealing for a given set of data points and a given temperature schedule.
    :param temp_schedule: Dictionary containing temp schedule (key=time: val=temp)
    :param iterations: Number of iterations selected (should match temp schedule)
    :param value_list: List of values to create nodes with.
    :param initial_state: Location of initial node.
    :return: best choice of node.
    '''
    # Initialize list of nodes based on passed data vals
    node_list = init_node_list(value_list)
	# Initialize holder for histogram data at 0s 
	# (You know what they say: give a man a hashmap and every problem looks like a key, value pair)
    hist_data = init_histogram_data(value_list)
	
    # Select initial node based on passed value
    current_node = node_list[initial_state]
    cur_temp = 0
    # Main loop. Run from 1 to max iterations. Breaks on final time.
    for i in range(0, iterations):

        # Update temp if current iteration matches a point where the temp changes.
        if i in temp_schedule:
            cur_temp = temp_schedule[i]

        neighbors = get_neighbors(current_node, node_list)
        # Select random neighbor and set deltaE.
        next_node = random.choice(neighbors)
        delta_e = next_node.value - current_node.value

        if delta_e > 0:
            current_node = next_node
        else:
            # Create probability e^deltaE / temp and roll a random float between 0 and 1
            prob_range = math.exp(delta_e / cur_temp)
            roll = random.random()
            #print("range: " + str(prob_range) + " roll: " + str(roll) + " current temp: " + str(cur_temp))

            # If rolled number is <= than the determined range force move to next node. 
            if roll <= prob_range:
                current_node = next_node
		
		# Increments histogram data for the specified value
        hist_data[current_node.value] += 1   
        #print("Current node value: " + str(current_node.value))
    print(hist_data)
    return current_node
        # print(str(i) + ":" + str(cur_temp))

		
def init_histogram_data(value_list):
	hist_data = {}
	for value in value_list:
		hist_data[value] = 0
	return hist_data
		
	

def main():
    # run your code for 1000iterations.
    # Start with a temperature ofT= 100 and reduce it in half every 100iterations.
    # SoT= 50 for iterations 101 { 200,T= 25 for iterations 201 - 300, etc.

    increment = 100
    iterations = 1000
    start_temp = 100
    reduction = 0.50
    temp_schedule = init_temp_map(increment, iterations, start_temp, reduction)
    heuristic_values = [45, 8, 23, 91, 15, 83, 54, 100, 8, 44]
    initial_state = 2 #position 3
    #print(temp_schedule)
    print(simulated_annealing(temp_schedule, iterations, heuristic_values, initial_state).value)


if __name__ == '__main__':
    main()
