import random


class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 200, 0)

    @staticmethod
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    @staticmethod
    def get_random_leaf_color():
        return random.randint(0, 200), random.randint(0, 255), random.randint(0, 30)

    @staticmethod
    def get_random_outline_color():
        return random.randint(0, 40), random.randint(0, 80), random.randint(0, 20)
