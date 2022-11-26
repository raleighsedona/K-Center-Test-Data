""" Author: Raleigh Hansen
    Last Update: 11/25/2022 
    Version: Python 3.8.2
    Purpose: 
        Generate and alter various data-sets for testing
        k-center algorithms. Data is meant to stress test
        a reverse greedy algorithm against a greedy algorithm. 
        
        Details of the reverse greedy algorithm can be found here:
            https://doi.org/10.1016/j.ipl.2020.105941
        
        Details of the greedy algorithm can be found here: 
            https://doi.org/10.1016/0304-3975(85)90224-5
"""

import math
import random
from random import randint


""" write_to_file(data, path: str, mode='w+') 
    params: 
        data: 2D array of data points of any number of dimensions
        path: fullpath to .txt file for writing
        mode: write mode defaults to w+ """
def write_to_file(data: list, path: str, mode='w+'):

    with open(path, mode) as f:
        for i in range(len(data)):
            # write each coordinate of data point
            for j in range (len(data[i])):
                f.write(str(data[i][j]) + " ")
            
            # newline for next data point
            f.write("\n")


# only for 2D data, used in augmentation and sampling
def readData(path: str):
    dataX = []
    dataY = []

    with open(path) as f:
        for line in f.readlines():
            x, y = lineToDatapoint(line.split())
            dataX.append(x)
            dataY.append(y)

    return dataX, dataY


# helper function for converting 2D data from str to float
def lineToDatapoint(line: str):
    return float(line[0]), float(line[1])


# euclidian distance between two points
def distance(p1: list, p2: list):
    tot = 0 
    for i in range(0, len(p1)):
        tot += (p2[i] - p1[i])**2

    return math.sqrt(tot)


""" generate_rand_uniform(n: int, path: str, dimension: int, minval: int, maxval: int, clusters, clusteroff=0, mode='w+', outliers=False)
    params:
        n: desired number of points to be generated
        path: fullpath to .txt file contatining data-set to be output 
        dimension: desired number of dimensions per point 
        minval: minimum value for random number generation
        maxval: maximum value for random number generation 
        clusters: desired number of data point clusters 
        clusteroff: max value for cluster offset 
        mode: write mode defaults to w+
        outliers: boolean value True if outliers are desired, False otherwise
        
    Generates a random uniform distribution of n points with l dimensions and outputs them 
    to a file. If clusters are desired, generates uniform sub-distributions and offsets them away from other clusters.
    Using large offset values is recommended for those who do not want overlapping clusters. If outliers are desired,
    generates 2% of n points to be outliers. """
def generate_rand_uniform(n: int, path: str, dimension: int, minval: int, maxval: int, clusters=0, clusteroff=0, mode='w+', outliers=False):
    point = []
    data = []

    if clusters != 0:
        off = random.uniform(0,clusteroff)
        clust = True
    else:
        off = 0 
        clust = False

    # separate desired number of points into non-outliers and 2% of n outliers
    if outliers:
        outs = round(n * 0.02)
        n = n - outs

    # main generation loop
    for i in range(0, n):
        point = []

        # When a previous cluster has been filled, generate a new random offset
        # for the next cluster. Clusters may overlap.
        if clust and i % round(n/clusters) == 0:
            off = random.uniform(0,clusteroff)

        for j in range(0, dimension):
            point.append(random.uniform(minval + off, maxval + off))
        
        data.append(point)

    if outliers:
        for i in range(0,outs):
            point = []
            for j in range(0, dimension):
                point.append(random.uniform(maxval + abs(maxval), maxval + 2*(abs(maxval))))
            data.append(point)     
    
    write_to_file(data, path, mode)


""" generate_normal_cluster(n: int, path: str) 
    params:
        n: the desired number of data points
        path: fullpath to output data-set file 
    
    Generates a normally distributed cluster of
    points and outputs them to a file. """
def generate_normal_cluster(n: int, path: str):
    point = []
    data = []
    dataX = []
    dataY = []

    for i in range(0, n):
        point = []

        # generate random float seeds for x and y coords 
        x = random.random()
        y = random.random()

        # use seed to place in normal cluster
        point.append(math.sqrt(-2*math.log(x)) * math.cos(2*math.pi*y))
        point.append(math.sqrt(-2*math.log(x)) * math.sin(2*math.pi*y))
        
        data.append(point)
        dataX.append(point[0])
        dataY.append(point[1])
    
    write_to_file(data, path)
    return dataX, dataY


""" sample_data(n: int, findpath: str, storepath: str) 
    params:
        n: the desired number of points to sample
        findpath: fullpath to original data-set for sampling
        storepath: fullpath to store sampled data-set 
        
    Samples 2D points from an existing data-set
    and outputs them to a file. """
def sample_data(n: int, findpath: str, storepath: str):
    dataX, dataY = readData(findpath)
    sampled_data = []

    for i in range(0, n):
        rand_ind = random.randint(0, len(dataX)-1)
        sampled_data.append([dataX[rand_ind], dataY[rand_ind]])
    
    write_to_file(sampled_data, storepath)


""" increase_dimensions(n: int, dimensions, findpath: str, storepath: str) 
    params:
        dimensions: desired number of total dimensions 
        findpath: fullpath to original data-set for augmenting
        storepath: fullpath to store augmented data-set 
    
    Increases the number of dimensions in a 2D dataset. Augments
    along z dimensions by stepping along the max width of the original 
    data-set, adds noise in remaining dimensions (if any). Outputs
    the augmented data-set to a file. """
def increase_dimensions(dimensions: int, findpath: str, storepath: str):
    dataX, dataY = readData(findpath)
    n = len(dataX)
    width = max_dist(dataX, dataY)

    data = []
    for i in range(0, n):
        point = []
        point.append(dataX[i])
        point.append(dataY[i])


        for j in range(0, dimensions):
            # structured augmentation in z dimension
            if j==0:
                point.append(width-((width/n)*i))
            # noise in all other dimensions
            else:
                point.append(random.uniform(0,width))

        data.append(point)

    write_to_file(data, storepath)


# returns the maximum distance between any two points
def max_dist(dataX: list, dataY: list):
    maxdist = 0

    for i in range(0, len(dataX)):
        for j in range(i+1, len(dataY)):
            # convert float to int if not 2D array
            p1 = [dataX[i]] if type(dataX[i]) is float else dataX[i]
            p2 = [dataY[j]] if type(dataY[j]) is float else dataY[j]

            tempdist = distance(p1, p2)
            if tempdist > maxdist:
                maxdist = tempdist

    return maxdist
