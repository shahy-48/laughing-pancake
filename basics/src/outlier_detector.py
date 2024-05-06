import math
class OutlierDetection:
    def __init__(self, data:list) -> None:
        self._data = data
        try:
            self._n = len(data)
            self._mean = sum(self._data)/self._n
            self._variance = 0
            self._sd = 0
            self._z_scores = {}
        except:
            raise TypeError("Please provide a list of numbers as input to the class")

    def calculate_stats(self)->None:
        """Calculates the population variance and standard deviation"""
        for p in self._data:
            self._variance += ((p - self._mean)**2)/self._n
        self._sd = math.sqrt(self._variance)
    
    def calculate_z_scores(self)->None:
        """calculates the z-score for each value in the dataset"""
        self.calculate_stats()
        for p in self._data:
            if p not in self._z_scores:
                self._z_scores[p] = (p - self._mean)/self._sd
    
    def find_outliers_using_z_scores(self, threshold:float = 3.0)->list:
        self.calculate_z_scores()
        outliers = []
        for k,v in self._z_scores.items():
            if v >= threshold:
                outliers.append(k)
        return outliers

def main():
    my_list = [1, 3, 2, 14, 108, 456, 2, 1, 8, 97, 1, 4, 3, 5]
    my_list2 = ['cat','mat']
    stats = OutlierDetection(my_list2)
    print(stats.find_outliers_using_z_scores())


if __name__ == "__main__":
    main()
        
        


