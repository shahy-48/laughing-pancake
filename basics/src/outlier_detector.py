import math
import numpy as np

class OutlierDetection:
    """Outlier detection using simple statistics based approach"""
    def __init__(self, data:list) -> None:
        self._data = data
        try:
            self._n = len(data)
            self._mean = np.mean(self._data)
            self._median = np.median(self._data)
            self._variance = 0
            self._sd = 0
            self._mad = 0
            self._z_scores = {}
        except:
            raise TypeError("Please provide a list of numbers as input to the class")

    def calculate_stats(self)->None:
        """Calculates the population variance and standard deviation"""
        temp = []
        for p in self._data:
            self._variance += ((p - self._mean)**2)/self._n
            temp.append(np.absolute(p-self._median))
        self._sd = math.sqrt(self._variance)
        self._mad = np.median(temp)
    
    def calculate_z_scores(self)->None:
        """calculates the z-score for each value in the dataset"""
        self.calculate_stats()
        for p in self._data:
            if p not in self._z_scores:
                self._z_scores[p] = (p - self._mean)/self._sd
    
    def find_outliers_using_z_scores(self, threshold:float = 3.0, metric = "mean")->list:
        outliers = []
        if metric == "mean":
            self.calculate_z_scores()
            for k,v in self._z_scores.items():
                if v >= threshold:
                    outliers.append(k)
        elif metric == "median":
            self.calculate_stats()
            upper_bound = self._median + (self._mad * 2.5)
            lower_bound = self._median - (self._mad * 2.5)
            for p in self._data:
                if p > upper_bound or p < lower_bound:
                    outliers.append(p)
        else:
            raise ValueError("Only mean or median allowed as metric")
        
        return outliers
    
    def find_outliers_using_iqr(self)->list:
        """Finds outliers using inter-quartile range"""
        outliers = []
        q1 = np.percentile(self._data, 25)
        q3 = np.percentile(self._data, 75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        for p in self._data:
            if p < lower_bound or p > upper_bound:
                outliers.append(p)
        return outliers


        

def main():
    my_list = [1, 3, 2, 14, 108, 456, 2, 1, 8, 97, 1, 4, 3, 5, 20000]
    my_list2 = ['cat','mat']
    stats = OutlierDetection(my_list)
    print(stats.find_outliers_using_z_scores(metric="median"))


if __name__ == "__main__":
    main()
        
        


