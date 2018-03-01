import heapq
import sys

from collections import defaultdict

class Ride:
    def __init__(self, ride_id, r_start, c_start, r_end, c_end, t_start, t_end):
        self.ride_id = ride_id
        self.r_start = r_start
        self.c_start = c_start
        self.r_end = r_end
        self.c_end = c_end
        self.t_start = t_start
        self.t_end = t_end

class City:
    def __init__(self, rows, cols, vehicles, rides, bonus, simulation_steps):
        self.rows = rows
        self.cols = cols
        self.vehicles = vehicles
        self.rides = rides
        self.bonus = bonus
        self.simulation_steps = simulation_steps

class Car:
    def __init__(self, car_id, row, col):
        self.car_id = car_id
        self.row = row
        self.col = col

    def __lt__(self, other):
        return self.car_id < other.car_id

def read_file(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        rows, cols, vehicles, rides, bonus, simulation_steps = [int(n) for n in line.split()]

        ride_list = []
        i = 0
        for row in f:
            r_start, c_start, r_end, c_end, t_start, t_end = [int(n) for n in row.split()]
            ride_list.append(Ride(i, r_start, c_start, r_end, c_end, t_start, t_end))
            i += 1

    return City(rows, cols, vehicles, rides, bonus, simulation_steps), ride_list

def manhattan_distance(r_start, c_start, r_end, c_end):
    return abs(r_end - r_start) + abs(c_end - c_start)

def distance_to_ride(car, ride):
    return manhattan_distance(car.row, car.col, ride.r_start, ride.c_start)

def ride_distance(ride):
    return manhattan_distance(ride.r_start, ride.c_start, ride.r_end, ride.c_end)

def ride_score(car, ride, current_time, city):
    points = 0

    distance = distance_to_ride(car, ride)

    if current_time + distance <= ride.t_start:
        points += city.bonus

    if ride_finish_time(car, ride, current_time) < city.simulation_steps and \
       ride_finish_time(car, ride, current_time) < ride.t_end:
        points += ride_distance(ride)
    else:
        points = 0

    return points

def ride_finish_time(car, ride, current_time):
    time = current_time + distance_to_ride(car, ride)

    if time <= ride.t_start:
        time = ride.t_start

    time += ride_distance(ride)

    return time

def priority_queue_init(city):
    priority_queue = []

    for i in range(city.vehicles):
        heapq.heappush(priority_queue, (0, Car(i, 0, 0)))

    return priority_queue

def main_algo(city, rides):
    priority_queue = priority_queue_init(city)
    solutions = defaultdict(list)

    while True:
        time, car = heapq.heappop(priority_queue)

        if time >= city.simulation_steps or not rides:
            return solutions

        max_score = -1
        max_ride = None
        for ride in rides:
            score = float(ride_score(car, ride, time, city)) / (ride_finish_time(car, ride, time) - time)
            if score > max_score:
                max_score = score
                max_ride = ride

        # Delete ride as it was completed already
        rides.remove(max_ride)

        solutions[car.car_id].append(max_ride.ride_id)
        heapq.heappush(priority_queue, (ride_finish_time(car, max_ride, time),
                        Car(car.car_id, max_ride.r_end, max_ride.c_end)))

    return solutions

def print_solution(filename, solutions):
    with open(filename, 'w+') as f:
        for key, value in solutions.items():
            line = str(len(value)) + ' ' + ' '.join(str(x) for x in value) + '\n'
            f.write(line)

def main():
    filename = sys.argv[-1]
    city, rides = read_file(filename)
    output = filename.replace('input', 'output').replace('.in', '.out')
    print_solution(output, main_algo(city, rides))

if __name__ == '__main__':
    main()
