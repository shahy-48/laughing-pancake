from math import sqrt
import pandas as pd


class KnnOd:
    def __init__(self, data:pd.DataFrame) -> None:
        self.data = data
        self.new_data = data.select_dtypes(include='number')
        
    
    def find_minmax(self, col:pd.Series)->tuple:
        """Finds the min and max for each dataframe column"""
        return min(col), max(col)
    
    def standardize(self)-> None:
        """Standardizes data between 0 and 1 using min-max"""
        for col in self.new_data.columns:
            mini, maxi = self.find_minmax(self.new_data[col])
            self.new_data[col] = self.new_data[col].apply(lambda row: (row-mini)/maxi)

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
    
    def find_farthestneighbors(self)->list:
        """Returns the top 3 data points that are the farthest from most other data points in the set"""
        self.standardize()
        outliers = {}
        for id, row in self.new_data.iterrows():
            neighbors = []
            for id2, row2 in self.new_data.iterrows():
                if id != id2:
                    dist = self.euclidean_distance(row2.to_list(), row.to_list())
                    neighbors.append((id2, dist))
            neighbors = sorted(neighbors, key = lambda tup: tup[1], reverse=True)
            for i in range(len(neighbors)//2):
                if neighbors[i][0] not in outliers:
                    outliers[neighbors[i][0]] = 1
                else:
                    outliers[neighbors[i][0]] += 1
        return [k for k,v in sorted(outliers.items(), key = lambda item:item[1], reverse=True)][:3]

def main():       
    dataset = [[2.7810836,2.550537003],
    [1.465489372,2.362125076],
    [3.396561688,4.400293529],
    [1.38807019,1.850220317],
    [3.06407232,3.005305973],
    [7.627531214,2.759262235],
    [5.332441248,2.088626775],
    [6.922596716,1.77106367],
    [8.675418651,-0.242068655],
    [7.673756466,3.508563011]]
    df = pd.DataFrame(data = dataset, columns=['x1','x2'])
    knn_detector = KnnOd(df)
    print(knn_detector.find_farthestneighbors())

if __name__=="__main__":
    main()
        

        
    
