from priority_queue import PriorityQueue

class Car:
    # Seats of the car
    capacity = 2

    def __init__(self, position, grid_map):
        self.position = position
        self.grid_map = grid_map

        # Possible status:
        # 1. idle
        # 2. picking_up
        # 3. dropping_off
        self.status = "idle"

        self.serving = [] # Serving passengers
        self.pending = [] # Pending passengers
        self.path = []

    def __repr__(self):
        msg = ""
        msg += f"cls: {type(self).__name__}"
        msg += f", id: {hex(id(self))}"
        msg += f", status: {self.status}"
        msg += f", position: {str(self.position)}"
        msg += f", path: {str(self.path)}"

        return msg

    def assign_passenger(self, passenger):
        self.pending.append(passenger)

    def pair_passengers(self):
        if len(self.pending) == 0: # No pending passenger to serve
            self.status = "idle"
            return

        self.status = "picking_up"

        if len(self.serving) == 0: # Serve the first passenger
            self.serving.append(self.pending.pop(0))

        # Ride sharing
        for i in range(1, self.capacity):
            if len(self.pending) == 0:
                break

            Row_max, Col_max = self.serving[i - 1].pick_up_point
            Row_min, Col_min = self.serving[i - 1].drop_off_point

            if Row_max < Row_min:
                Row_max, Row_min = Row_min, Row_max
            if Col_max < Col_min:
                Col_max, Col_min = Col_min, Col_max

            for j in range(len(self.pending)):
                x, y = self.pending[j].pick_up_point
                if Row_min <= x <= Row_max and Col_min <= y <= Col_max:
                    self.serving.append(self.pending.pop(j))
                    break

        points = [self.position]
        for p in self.serving:
            p.status = "wait_pick"
            points.append(p.pick_up_point)

        self.path = self.grid_map.plan_path(points)

    def plan_drop_off_path(self):
        assert len(self.serving) > 0

        self.status = "dropping_off"

        cmp = lambda pa, pb: self.grid_map.dist_between(self.position, pa) < self.grid_map.dist_between(self.position, pb)
        pq = PriorityQueue(cmp)

        """
        Drop passengers according to the distance
        between current position and their destinations.
        """
        for p in self.serving:
            pq.push(p.drop_off_point)

        points = [self.position]
        while len(pq) > 0:
            points.append(pq.top())
            pq.pop()

        self.path = self.grid_map.plan_path(points)

    """
    Move the car to the
    next position on the path.
    """
    def move_to_next_position(self, duration):
        assert self.status != "idle", "Shouldn't move"

        if len(self.path) > 0:
            self.position = self.path.pop(0)

        arrived = []
        for i, passenger in enumerate(self.serving):
            if self.position in (passenger.pick_up_point, passenger.drop_off_point):
                arrived.append(i)

        arrived.reverse() # Loop the index from high to low
        for i in arrived:
            p = self.serving[i]

            if self.status == "picking_up":
                p.status = "picked_up"
                p.waiting_steps = duration
            elif self.status == "dropping_off":
                p.status = "dropped_off"
                self.serving.pop(i)

if __name__ == "__main__":
   pass
