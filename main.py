import time
import requests
import copy
from dataclasses import dataclass


@dataclass()
class Node:

    count : int
    weight : int 
    total_weight : int
    available_weights : list
    previous : int 
    index : int = None

    def __post_init__(self):
        self.total_weight += self.count * self.weight


def get_weigts():
    url = 'https://bwinf.de/fileadmin/user_upload/gewichtsstuecke3.txt'
    result = requests.get(url)
    doc = result.content.decode("utf-8").split()
    start_weights = []
    for i in range(1, len(doc), 2):
        start_weights.append([int(doc[i]), int(doc[i + 1])]) 
    return start_weights

def get_closesed_weight(visited):
    closesed_weight = visited[0]
    for node in visited:
        if abs(closesed_weight.total_weight - searched_weight) > abs(node.total_weight - searched_weight):
            closesed_weight = node
    return closesed_weight

def remove_one_weight(weights, index):
    del weights[index]
    return weights

def get_path(end, visited, path=[]):
    path = [end] + path
    if  end.previous is None:
        return path
    return get_path(visited[end.previous], visited, path)

def find_combination(weights):
    visited = []
    queue = [Node(0, 0, 0, weights, None)]
    while queue:
        node = queue[0]
        node.index = len(visited)
        if node.total_weight == searched_weight:
            return get_path(node, visited)
        if node.available_weights:
            for count in range(1 ,node.available_weights[0][1] + 1):
                queue.append(Node(count, +node.available_weights[0][0], node.total_weight, remove_one_weight(copy.deepcopy(node.available_weights), 0), node.index)) 
                queue.append(Node(count, -node.available_weights[0][0], node.total_weight, remove_one_weight(copy.deepcopy(node.available_weights), 0), node.index)) 
        visited.append(queue[0])
        del queue[0]
    return get_path(get_closesed_weight(visited), visited)

def print_path_for_weight(path):
    print(f'weight {searched_weight}:')
    for node in path:
        for count in range(node.count):
            print(node.weight)
    print(f'reached weight{node.total_weight}')

def main():
    global searched_weight
    weights = get_weigts()
    start = time.time() 
    for searched_weight in range(10, 10010, 10):
        path = find_combination(weights)
        print_path_for_weight(path) 
    print(f'time: {time.time() - start}')
    return

if __name__ == '__main__':
    main()