import random

class SignalGenerator:
    def generate(self, length=20):
        return [random.randint(10, 90) for _ in range(length)]
