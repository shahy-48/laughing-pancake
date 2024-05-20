import sys
import math
import numpy as np

class NumericalSimilarityCalculator:
    def __init__(self, list1:list, list2:list, method:str = "euclidean_distance") -> None:
        self.list1 = list1
        self.list2 = list2
        self._method = method

    def euclidean_distance(self)->float:
        """
        Description: Measures the straight-line distance between two points in Euclidean space for the whole data set
        Method implications: Sensitive to scale of data; all features contribute equally
        """
        result = 0.0
        for a,b in zip(self.list1,self.list2):
            result += math.pow(np.absolute(a-b),2)
        return round(math.sqrt(result), 2)

    def cosine_similarity(self)->float:
        """
        Description: Measures the cosine of the angle between two vectors, capturing the orientation rather than magnitude
        Method implications: Useful for high-dimensional data; robust to differences in magnitude
        """
        numerator, denominator1, denominator2 = 0.0, 0.0, 0.0
        for a,b in zip(self.list1,self.list2):
            numerator += (a*b)
            denominator1 += math.pow(a,2)
            denominator2 += math.pow(b,2)
        return round(numerator/(math.sqrt(denominator1) * math.sqrt(denominator2)), 2)


    def pearson_correlation(self)->float:
        """
        Description: Measures linear correlation between two sequences
        Implications: Indicates both strength and direction of linear relationship; sensitive to outliers.
        """
        numerator, denominator1, denominator2 = 0.0, 0.0, 0.0
        mean_a, mean_b = np.mean(self.list1), np.mean(self.list2)
        for a,b in zip(self.list1,self.list2):
            numerator += ((a-mean_a)*(b-mean_b))
            denominator1 += math.pow(a-mean_a,2)
            denominator2 += math.pow(b-mean_b,2)
        return round(numerator/(math.sqrt(denominator1) * math.sqrt(denominator2)), 2)

    def calculate(self):
        match self._method:
            case 'euclidean_distance': return self.euclidean_distance()
            case 'cosine_similarity': return self.cosine_similarity()
            case 'pearson_correlation': return self.pearson_correlation()