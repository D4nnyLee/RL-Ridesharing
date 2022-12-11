
from passenger import Passenger

class Car:
    def __init__(self, position, energy):
        self.status = 'idle' # idle, picking_up, dropping_off
        self.position = position
        self.energy = energy
        self.passenger = None
        self.path = []
        self.required_steps = None
        self.travel_distance = 0

    def __repr__(self):
        message = 'cls:' + type(self).__name__ + ', id:' + str(id(self))  + ', status: ' + self.status + \
          ', required_steps:' + str(self.required_steps) + ', position:' + str(self.position) + ', path:' + str(self.path)
        if self.passenger:
            message += ', passenger: ' + str(id(self.passenger))
        else:
            message += ', passenger: None'
        return message

    def pair_passenger(self, passenger):
        self.passenger = passenger
        self.passenger.status = 'wait_pick'
        self.status = 'picking_up'

    def pick_passenger(self):
        self.passenger.status = 'picked_up'
        self.status = 'dropping_off'

    def drop_passenger(self):
        self.passenger.status = 'dropped'
        self.passenger = None
        self.status = 'idle'

    def assign_path(self, path1, path2):
        self.path = (path1 + path2)

    """
    Try to move the car to the next position
    on the path.

    Return False only if the car is out of energy.
    """
    def move(self): # call by environment step
        assert self.status != 'idle', "shouldn't move", "out_of_energy"

        if self.energy <= 0:
            self.status = "out_of_energy"
            return False

        self.energy -= 1

        self.position = self.path.pop(0)
        self.travel_distance += 1

        return True

if __name__ == '__main__':
    c = Car((0,0))
    print(c)
    p = Passenger((0,0), (1,0))
    print(p)
    c.pair_passenger(p)
    print(c)
    print(p)
    c.pick_passenger()
    print(c)
    print(p)
    c.drop_passenger()
    print(c)
    print(p)
