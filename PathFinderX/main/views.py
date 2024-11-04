from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request,'main.html')

class Graph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.edges = {}
        for row in range(self.rows):
            for col in range(self.cols):
                if matrix[row][col] == 0:
                    self.edges[(row, col)] = []
                    for delta_row, delta_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        neighbor_row, neighbor_col = row + delta_row, col + delta_col
                        if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and matrix[neighbor_row][neighbor_col] == 0:
                            self.edges[(row, col)].append((neighbor_row, neighbor_col))

def bellman_ford(graph, start):
    distance = {node: float('inf') for node in graph.edges}
    distance[start] = 0
    for _ in range(len(graph.edges) - 1):
        for node in graph.edges:
            for neighbor in graph.edges[node]:
                distance[neighbor] = min(distance[neighbor], distance[node] + 1)
    return distance

def shortest_path(matrix):
    graph = Graph(matrix)
    start = (0, 0)
    end = (len(matrix) - 1, len(matrix[0]) - 1)
    if matrix[0][0] == 1 or matrix[end[0]][end[1]] == 1:
        return float('inf'), []
    
    distance = bellman_ford(graph, start)
    
    if distance[end] == float('inf'):
        return distance[end], []

    path = []
    current = end
    while current != start:
        path.append(current)
        for node in graph.edges:
            if current in graph.edges[node] and distance[node] + 1 == distance[current]:
                current = node
                break
    path.append(start)
    path.reverse()
    return distance[end], path

@csrf_exempt
def find_shortest_path(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        matrix = data.get('matrix')
        if not matrix:
            return JsonResponse({'error': 'No matrix provided'}, status=400)

        distance, path = shortest_path(matrix)
        return JsonResponse({'distance': distance, 'path': path})
