import random

from car import Car
from passenger import Passenger

class GridMap:
    def __init__(self, rnd_seed, size, num_cars, num_passengers):
        self.rnd_seed = rnd_seed
        self.size = size # (row, col)
        self.num_cars = num_cars
        self.num_passengers = num_passengers

        self.cars = []
        self.passengers = []
        self.map_cost = dict()

        random.seed(rnd_seed)
        self.add_cars(self.num_cars)
        self.add_passengers(self.num_passengers)
        self.init_map_cost()

    """
    Test if `p` is a valid coordinate in grid map.
    """
    def is_valid(self, p):
        return (0 <= p[0] < self.size[0]) and (0 <= p[1] < self.size[1])

    """
    Test if `p1` is adjacent to `p2`.
    """
    def is_adjacent(self, p1, p2):
        assert self.is_valid(p1), "map point p1 is out of boundary"
        assert self.is_valid(p2), "map point p2 is out of boundary"

        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1

    """
    Set the weight of edges in the grid map with random value
    """
    def init_map_cost(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                p = (row, col)

                p_down = (row + 1, col)
                if self.is_valid(p_down):
                    self.map_cost[(p_down, p)] = self.map_cost[(p, p_down)] = random.randint(1, 9)

                p_right = (row, col + 1)
                if self.is_valid(p_right):
                    self.map_cost[(p_right, p)] = self.map_cost[(p, p_right)] = random.randint(1, 9)

    """
    Similar to init_map_cost(), but the weight is set to 1
    """
    def init_one_map_cost(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                p = (row, col)

                p_down = (row + 1, col)
                if self.is_valid(p_down):
                    self.map_cost[(p_down, p)] = self.map_cost[(p, p_down)] = 1

                p_right = (row, col + 1)
                if self.is_valid(p_right):
                    self.map_cost[(p_right, p)] = self.map_cost[(p, p_right)] = 1

    """
    Add `num_cars` cars with random state
    state: (current_x, current_y)
    """
    def add_cars(self, num_cars):
        assert num_cars <= self.size[0] * self.size[1], "number of cars is larger than number of grids"

        car_set = set()
        while len(car_set) < num_cars:
            p = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
            car_set.add(p)

        for s in car_set:
            self.cars.append(Car(s, self))

    """
    Add `num_passengers` passengers with random state
    state: (start_x, start_y, target_x, target_y)
    """
    def add_passengers(self, num_passengers):
        assert num_passengers <= self.size[0] * self.size[1], "number of passengers is larger than number of grids"

        passenger_set = set()
        while len(passenger_set) < num_passengers:
            p = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
            passenger_set.add(p)

        for sx, sy in passenger_set:
            # generate destination point
            dx = (sx + random.randint(1, self.size[0] - 1)) % self.size[0]
            dy = (sy + random.randint(1, self.size[1] - 1)) % self.size[1]

            self.passengers.append(Passenger((sx, sy), (dx, dy)))

    """
    Calcute Manhattan distance between `p1` and `p2`
    """
    @classmethod
    def dist_between(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    """
    Find the shortest path from `start_point` to `end_point`.

    Notes that the length of path here is measured by Manhattan distance between points
    instead of the weight of edges on the path.

    Returned path: (start_point, end_point]
    """
    def plan_path_two_points(self, start_point, end_point):
        x, y = start_point
        path = []

        step = 1 if x <= end_point[0] else -1

        while x != end_point[0]:
            x += step
            path.append((x, y))

        step = 1 if y <= end_point[1] else -1

        while y != end_point[1]:
            y += step
            path.append((x, y))

        return path

    """
    Find the shortest path going through every point in `points`.

    Notes that the length of path here is measured by Manhattan distance between points
    instead of the weight of edges on the path.
    """
    def plan_path(self, points):
        path = []
        for i in range(1, len(points)):
            path += self.plan_path_two_points(points[i - 1], points[i])

        return path

if __name__ == "__main__":
    pass
