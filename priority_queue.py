class PriorityQueue:
    def __init__(self, cmp = lambda x, y: x < y):
        # First element is dummy element
        self.arr = [0]

        # Compare function,
        # default is minimum value on the top
        self.cmp = cmp

    def __repr__(self):
        return str(self.arr[1:])

    def __len__(self):
        return len(self.arr) - 1

    def top(self):
        assert len(self) > 0, "Trying to pop element from empty PriorityQueue"

        return self.arr[1]

    def push(self, val):
        arr = self.arr

        i = len(arr)

        arr.append(val)

        while i > 1 and self.cmp(arr[i], arr[i >> 1]):
            self.swap_element(i, i >> 1)
            i >>= 1

    def pop(self):
        arr = self.arr

        self.swap_element(1, -1)

        arr.pop(-1)

        i = 1
        while i < len(arr):
            mn = i # index of minimum children

            for j in [2 * i, 2 * i + 1]:
                if j < len(arr) and self.cmp(arr[j], arr[mn]):
                    mn = j

            if not self.cmp(arr[mn], arr[i]):
                break

            self.swap_element(i, mn)
            i = mn

    def swap_element(self, i, j):
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i] # swap(arr[i], arr[j])

if __name__ == "__main__":
    import random

    """
    Simple heapsort here
    """

    x = [random.randint(-1000, 1000) for _ in range(100)]
    y = []

    pq = PriorityQueue()
    for xi in x:
        pq.push(xi)

    while len(pq) > 0:
        y.append(pq.top())
        pq.pop()

    print(f"Before: {x}")
    print(f"After:  {y}")

    assert sorted(x) == y

