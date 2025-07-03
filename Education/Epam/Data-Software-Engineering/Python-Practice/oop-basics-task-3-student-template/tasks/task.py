class Counter:
    def __init__(self, start=0, stop = -1):
        self.start = start
        self.stop = stop

    def get(self):
        return self.start

    def increment(self):
        if self.stop == -1 or self.stop > self.start:
            self.start += 1
        else:
            print("Maximal value is reached.")

if __name__ == "__main__":
    c = Counter(start=42)
    c.increment()
    c.get()

    c = Counter()
    c.increment()
    c.get()
    c.increment()
    c.get()


    c = Counter(start=42, stop=43)
    c.increment()
    c.get()
    c.increment()
    c.get()
