'''
Author: BlankZhu
Email:  z707310837@gmail.com
'''

import math
import csv
import random
import optparse
import copy

# functions begin here!


# read csv into the program
# param[in]: file path of CSV
# param[out]: dataset a list of points
# param[out]: classes a dict of all the classes with counts
def ReadCSV(file_path):
    dataset = []    
    classes = {}    # for futher use if you want
    with open(file_path) as database:
        for row in csv.reader(database):
            point = []
            for val in row[:-1]:
                point.append(float(val))
            dataset.append(point)
            if row[-1] in classes:
                classes[row[-1]] += 1
            else:
                classes[row[-1]] = 1
    #return dataset, classes
    return dataset


# calculate distance from item1 to item2
# param[in]: item1 1st point
# param[in]: item2 2nd point
# param[out]: sqrt(sum) distanse between item1 & item2
def CalcDist(item1, item2):
    attrs = len(item1)
    sum = 0
    for attr in range(attrs):
        diff = (item1[attr] - item2[attr]) ** 2
        sum += diff
    return math.sqrt(sum)


# calculate average point
# param[in]: cluster a list of points
# param[out]: avg_point a center point of cluster
def CalcAvgPoint(cluster):
    avg_point = []
    attrs = len(cluster[0])
    for attr in range(attrs):
        sum = 0
        for point in cluster:
            sum += point[attr]
        avg_point.append(sum / float(len(cluster)))
    return avg_point


# calculate cluster
# param[in]: dataset a list of all points
# param[in]: k_points k representative points
# param[out]: cluster a list of point list
def CalcCluster(dataset, k_points):
    # there are k clusters
    clusters = []
    for i in range(len(k_points)):
        clusters.append(list())
    for i in range(len(clusters)):
        clusters[i].append(k_points[i])

    for point in dataset:
        # min_dist: a distance list from current 
        #.. point to k_point
        min_dist = []
        # calculate min_dist
        for kpoint in k_points:
            min_dist.append(CalcDist(point, kpoint))

        # get the minimun distance
        i = 0
        j = 0
        min_val = min_dist[0]
        while i < len(min_dist):
            if min_dist[i] < min_val:
                j = i
                min_val = min_dist[i]
            i += 1
        if point not in k_points:
            clusters[j].append(point)

    return clusters


### this function is discarded
# get the distance between all the points
# param[in]: dataset a list of points
# param[out]: res a matrix of distance between all the point pair
def GetAllDist(dataset):
    i = 0
    res = []

    while i < len(dataset):
        j = 0
        while j < len(dataset):
            if i == j:
                res[i].append(0)
            else:
                res[i].append(CalculateDistance(dataset[i], dataset[j]))
    
    return res
            

# generate k points
# param[in]: k number of selected points
# param[in]: dataset dataset of all points
# param[out]: list of selected points
def GenerateKPoints(k, dataset):
    k_points = []
    base_index = random.randint(0, k)

    for _k in range(k):
        k_points.append(dataset[_k + base_index])

    return k_points


# check if two k_point lists(old one and the new one) are the same
# param[in]: old_lt old list of k_points
# param[in]: new_lt new list of k_points
# param[out]: boolean true if same, else false
def CheckSame(old_lt, new_lt):
    if len(old_lt) != len(new_lt):
        return False

    for i in range(len(old_lt)):
        for j in range(len(old_lt[0])):
            if old_lt[i][j] != new_lt[i][j]:
                return False

    return True


# run k-means algorithm
# param[in]: k k kinds of classes
# param[in]: dataset dataset of all points
def run_k_means(k, dataset):
    # 1st: generate the first k points
    k_points = GenerateKPoints(k, dataset)

    # 2nd: get all distance, put them into cluster
    clusters = CalcCluster(dataset, k_points)

    # 3rd
    last_k_points = []
    while not CheckSame(last_k_points, k_points):
        last_k_points = k_points
        k_points = []
        for cluster in clusters:
            if len(cluster) == 0:
                continue
            k_points.append(CalcAvgPoint(cluster))
        clusters = CalcCluster(dataset, k_points)

    # output
    for i in range(len(k_points)):
        print(str(i + 1) + " Clusters")
        print("center point: ", end='')
        print(k_points[i])
        print("cluster: ", end='')
        print(clusters[i])


# main start here
if __name__ == "__main__":
    p = optparse.OptionParser(usage="%prog k_number")
    p.add_option('-k', '--k-number', dest='k', type='int',
        help='K number of k-mean algorithm, default: 2')
    p.set_defaults(k=2)
    p.add_option('-f', '--datafile-path', dest='datapath', type='string',
        help=('File path of CSV data, default: ./data.csv'))
    p.set_defaults(datapath='./data.csv')
    options, args = p.parse_args()
    if options.k < 1:
        p.error('Must provide a valid k!')

    dataset = ReadCSV(options.datapath)
    run_k_means(options.k, dataset)
