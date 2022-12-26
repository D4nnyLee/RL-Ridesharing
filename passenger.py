class Passenger:
    def __init__(self, pick_up_point, drop_off_point):
        self.pick_up_point = pick_up_point
        self.drop_off_point = drop_off_point

        # Possible status:
        # 1. wait_pair
        # 2. wait_pick
        # 3. picked_up
        # 4. dropped_off
        self.status = "wait_pair"

        self.waiting_steps = 0

    def __repr__(self):
        msg = ""
        msg += f"cls: {type(self).__name__}"
        msg += f", id: {hex(id(self))}"
        msg += f", status: {self.status}"
        msg += f", pick_up_point: {str(self.pick_up_point)}"
        msg += f", drop_off_point: {str(self.drop_off_point)}"
        msg += f", waiting_steps: {str(self.waiting_steps)}"

        return msg

if __name__ == "__main__":
    p = Passenger((0,0), (1,0))
    print(p)
