from priority_queue import PriorityQueue

class Environment:
    def __init__(self, grid_map):
        self.grid_map = grid_map

    """
    Reset the cars and passengers on the grid map
    """
    def reset(self):
        self.grid_map.passengers = []
        self.grid_map.add_passengers(self.grid_map.num_passengers)

    def step(self, action, mode):
        action = action[0]

        grid_map = self.grid_map
        cars = grid_map.cars
        passengers = grid_map.passengers

        reward = None

        for i, act in enumerate(action):
            cars[act].assign_passenger(passengers[i])

        """
        `pq` will only store the serving car.

        Element of this priority queue should be
        (Time to arrive next position, car),
        and here we only compare the time when handling
        priority queue.
        """
        pq = PriorityQueue(lambda lhs, rhs: lhs[0] < rhs[0])

        """
        `duration` will be the total required time units
        for the following while loop to finish.
        """
        duration = 0

        for car in cars:
            car.pair_passengers()
            if car.status == "picking_up":
                """
                `cost` equals to 0 if and only if
                the car and first passenger is at
                the same position.
                """
                cost = 0
                if len(car.path) > 0:
                    cost += grid_map.map_cost[(car.position, car.path[0])]

                pq.push((duration + cost, car))

        while len(pq) > 0:
            duration = pq.top()[0]

            while len(pq) > 0:
                d, car = pq.top()

                if d != duration:
                    break

                pq.pop()

                car.move_to_next_position(duration)
                if len(car.path) == 0:
                    if car.status == "picking_up":
                        car.plan_drop_off_path()
                    elif car.status == "dropping_off":
                        car.pair_passengers()

                        if car.status == "idle": # No pending passenger, thus no need to push to `pq`
                            continue

                cost = 0
                if len(car.path) > 0:
                    cost += grid_map.map_cost[(car.position, car.path[0])]
                pq.push((duration + cost, car))

        if mode == "dqn":
            reward = [-passenger.waiting_steps for passenger in passengers]
        elif mode == "qmix":
            reward = -duration

        return reward, duration

if __name__ == "__main__":
    from gridmap import GridMap
    import random

    size = (100, 100)
    num_cars = 4
    num_passengers = 6

    g = GridMap(10, size, num_cars, num_passengers)
    g.init_one_map_cost()

    e = Environment(g)

    action = [[random.randint(0, num_cars - 1) for _ in range(num_passengers)]]

    for c in g.cars:
        print(c)
    print()

    for p in g.passengers:
        print(p)
    print()

    print(action[0])

    r, d = e.step(action, "dqn")

    print(f"reward: {r}")
    print(f"duration: {d}")
