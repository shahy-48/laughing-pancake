from math import sqrt

class KnnOd:
    def __init__(self) -> None:
        ...
    
    def euclidean_distance(self, x1:list, x2:list)->tuple:
        """Find euclidean distance between two points"""
        if len(x1) != len(x2):
            raise ValueError("Please ensure that length of each row is the same")
        if type(x1) != list or type(x2) != list:
            raise TypeError("Please provide lists of numbers as input")
        distance = 0
        for i in range(len(x1)):
            distance += (x1[i]-x2[i])**2
        return sqrt(distance)
