import math
import random
import time
import os

RUNS = 1000

def execute_runs(dir, att = False):
    for filename in os.listdir(dir):
        coords = []
        line_count = 0
        with open(dir+filename) as file:
            for line in file:
                line = line.strip()
                if line == 'EOF':
                    break
                if line_count < 6:
                    line_count += 1
                else:
                    [_,  x, y] = line.split()
                    x = float(x)
                    y = float(y)
                    coords.append((x, y)) 
        distances_matrix = generate_distances_matrix(coords, att)

        distances_sum = 0.0
        time_sum = 0.0
        for _ in range(RUNS):
            start = time.time()
            result = run_nn_heuristic(distances_matrix)
            elapsed = time.time() - start
            distances_sum += result
            time_sum += elapsed

        print(filename, round(distances_sum/float(RUNS)), f'{((time_sum/float(RUNS))*float(RUNS) * 1000):.2f}', sep="\t")

def calc_distance(p1, p2, is_pseudo_euclidian):
    if is_pseudo_euclidian:
      xd = p1[0]-p2[0]
      yd = p1[1]-p2[1]
      r = math.sqrt((xd*xd + yd*yd)/10.0)
      t = int(round(r))
      if t < r:
          return t+1
      else:
          return t 
    else:
        xd = p1[0]-p2[0]
        yd = p1[1]-p2[1]
        return int(round(math.sqrt(xd*xd + yd*yd)))

def generate_distances_matrix(coordinates, is_pseudo_euclidian):
  distances_matrix = []
  numberOfEdges = len(coordinates)
  for i in range(numberOfEdges):
    distances_i = []
    for j in range(numberOfEdges):
      distance_ij = calc_distance(coordinates[i], coordinates[j], is_pseudo_euclidian)
      distances_i.append(distance_ij)
    distances_matrix.append(distances_i)
  return distances_matrix

def run_nn_heuristic(distances_matrix):
  starting_city = random.randint(0, len(distances_matrix) - 1)
  current_city = starting_city
  visited_cities_indexes = set()
  total_distance = 0

  for _ in range(len(distances_matrix) - 1):
    visited_cities_indexes.add(current_city)
    nearest_distance = math.inf

    for neighbor_index in range(len(distances_matrix)):
      distance_to_neighbor = distances_matrix[current_city][neighbor_index]
      if neighbor_index not in visited_cities_indexes and distance_to_neighbor < nearest_distance:
        nearest_city_index = neighbor_index
        nearest_distance = distance_to_neighbor

    total_distance += nearest_distance
    current_city = nearest_city_index

  total_distance += distances_matrix[current_city][starting_city]
  return total_distance

print('file_name', f'avg_result ({RUNS} runs)', f'avg_time ({RUNS} runs, ms)', sep="\t")
execute_runs("ATT/", True)
execute_runs("EUC_2D/")