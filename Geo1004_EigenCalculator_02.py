import psycopg2
import csv
import numpy as np
from operator import itemgetter
import pandas as pd
import scipy
from sklearn.neighbors import NearestNeighbors
import time
from numpy import linalg as la


StartTime = int(round(time.time() * 1000))

# Loading the csv into a data frame
TopVoxels = pd.read_csv('topVoxels.csv', names=['X', 'Y', 'Z'], dtype = 'float' )


# Calculating the minimums
MinX = min(TopVoxels['X'])
MinY = min(TopVoxels['Y'])
MinZ = min(TopVoxels['Z'])

# Subtracting the minimum from the column (to move it to 0,0,0)
TopVoxels['X'] = TopVoxels['X'].apply(lambda x: x - MinX)
TopVoxels['Y'] = TopVoxels['Y'].apply(lambda x: x - MinY)
TopVoxels['Z'] = TopVoxels['Z'].apply(lambda x: x - MinZ)

# Creating a 'deep' copy of the TopVoxels to use later because it has the same format and we want that
TopVoxelNormals = TopVoxels.copy(deep=True)

# Distance List
k_value = 10
nbrs = NearestNeighbors(n_neighbors=k_value, algorithm='ball_tree').fit(TopVoxels)
distances, indices = nbrs.kneighbors(TopVoxels)

#Adding normal columns
for index, row in TopVoxels.iterrows():
    vectorMatrix = np.zeros(shape=[3,k_value])
    sum_centroids = np.zeros(shape=[1,3])
    centroid = np.zeros(shape=[1, 3])
    covariance_matrix = np.zeros(shape=[3,3])


    for j in range(k_value):
        vectorMatrix[0,j] = TopVoxels['X'][indices[index][j]]
        vectorMatrix[1,j] = TopVoxels['Y'][indices[index][j]]
        vectorMatrix[2,j] = TopVoxels['Z'][indices[index][j]]

        sum_centroids = np.add(sum_centroids,vectorMatrix[:,j])


    centroid = sum_centroids / k_value

    for j in range(k_value):
        vectorMatrix[0,j] = vectorMatrix[0,j] - centroid[0,0]
        vectorMatrix[1,j] = vectorMatrix[1,j] - centroid[0,1]
        vectorMatrix[2,j] = vectorMatrix[2,j] - centroid[0,2]

    trans_matrix = vectorMatrix.transpose()

    covariance_matrix = np.dot(vectorMatrix,trans_matrix)
    covariance_matrix = covariance_matrix * 1/(k_value-1)

    eigenValue, eigenVector = la.eig(covariance_matrix)

    TopVoxelNormals['X'][index] = eigenVector[2,0]
    TopVoxelNormals['Y'][index] = eigenVector[2,1]
    TopVoxelNormals['Z'][index] = eigenVector[2,2]

# Converts each row into tuples
normalTuples = [tuple(row) for row in TopVoxelNormals.values]
pointTuples = [tuple(row) for row in TopVoxels.values]


print(TopVoxels)
print(normalTuples[:100])
print(pointTuples[:100])


# calculating the spend time
EndTime = int(round(time.time() * 1000))
ElapsedTime = EndTime - StartTime
print "Time Elapsed : " + str(float(ElapsedTime)/1000) + " seconds"


