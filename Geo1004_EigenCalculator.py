import psycopg2
import csv
import numpy
from operator import itemgetter
import pandas
import scipy
import sklearn as sk

# this will connect to the database and extract the csv file 'PointCloudTable3'  with the points as tuple of floats


# this will connect to the database and extract the csv file 'PointCloudTable3'  with the points as tuple of floats

try:

    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()
cur.execute("SELECT * FROM PointCloudTable3;")

fetch = cur.fetchall()

#converting the csv file to a list of tuples
point_tuples = []
for i in fetch:
    point_tuples.append(list(i))

print(point_tuples[:100])



# #print(point_tuples)
# def KNN(points,kValue):
#
#     knn_dict = {}
#
#     for i in range(len(point_tuples)-1):
#         distance_list = []
#         for j in range(len(point_tuples)-1):
#             j = j + 1
#             point1 = numpy.array(point_tuples[i])
#             point2 = numpy.array(point_tuples[j])
#
#             distance = abs(numpy.linalg.norm(point1 - point2))
#
#             distance_tuple = [point_tuples[j],distance]
#             distance_list.append(distance_tuple)
#
#         sorted_distances = sorted(distance_list, key=itemgetter(1))
#         sorted_distances = sorted_distances[1:]
#         sorted_points = []
#         for dis in sorted_distances:
#             sorted_points.append(dis[0])
#
#         knn_dict[str(point_tuples[i])] = sorted_points[:kValue+1]
#
#     return knn_dict
#
#
#
#
# if len(point_tuples) > 3:
#     covMatrix = []
#     neighbours = []
#     centroid = 0
#     for i in range(len(point_tuples)):
#         neighs = KNN(point_tuples,5)[str(point_tuples[i])]
#     print((neighs))






