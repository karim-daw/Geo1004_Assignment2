import psycopg2
import csv


# input: is a list of tuples float values for points
# process: converting all values of each tuples in ints: this will essentially put all the points on a grid where each
# cell of this grid is the size of the resolution value which is also the dimension of the voxels
# output: is a list of tuples of ints, representing the centroids of the voxels

def pointPlace(pointCloud,resolution):

    half = resolution / 2
    voxelList = []

    voxelList = []
    for point in pointCloud:
        x = int(point[0] / resolution)
        y = int(point[1] / resolution)
        z = int(point[2] / resolution)
        centerOfVoxel = (x * resolution + half, y * resolution + half, z * resolution + half)
        voxelList.append(centerOfVoxel)
    voxelPoints = voxelList
    uniquePoints = set(voxelPoints)

    # this checks how many repeat points we have after the 'resolution' operator
    count = {}
    for each_value in voxelPoints:
        if each_value in count:
            count[each_value] += 1
        else:
            count[each_value] = 1

    # this adds an int value of the amount of times a point is found in a voxel to the end of each tuple
    listWithWeight = []
    for key, value in count.iteritems():
        temp = list(key)
        temp.append(value)
        listWithWeight.append(temp)

    # this checks how many repeat points we have after the 'resolution' operator
    centroids = []
    for value in listWithWeight:
        proper_point = (value[0], value[1], value[2])
        centroids.append(proper_point)

    return centroids


# ---------------------------------------------------------------------------------------------


# this will connect to the database and extract the csv file 'PointCloudTable3'  with the points as tuple of floats
try:

    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234'")
except:
    print ("I am unable to connect to the database")

cur = conn.cursor()
cur.execute("SELECT * FROM PointCloudTable3;")

fetch = cur.fetchall()

#converting the csv file to a list of tuples
non_tuples = []
for i in fetch:
    non_tuples.append(list(i))

# running the function below will take in the concerted csv file and output the centroids of those points
# we are running this with resolution 1, aka a voxel is 1 by 1 by 1
data = pointPlace(non_tuples,1)


# ---------------------------------------------------------------------------------------------
# this will create table of all the centroids in the database, unless it already exist there
# the table will consist of an ID, x value, y, value, z value
try:
    cur.execute('CREATE TABLE data_model (ID int, i int, j int, k int);')
    query = 'INSERT INTO data_model (ID, i, j, k) VALUES (%s, %s, %s, %s);'
    dummy_list = []
    for i, row in enumerate(data):
        pnt = (i, row[0], row[1], row[2])
        dummy_list.append(pnt)
        cur.execute(query, pnt)
except:
    print ("This table is already on the database!")


# CHECK ME -- need to know exactly how this works
conn.rollback()
cur.execute("SELECT * FROM data_model;")

fetch = cur.fetchall()
print("testing if data is ok:")
print(fetch[:300])
print(len(fetch))


# ---------------------------------------------------------------------------------------------
# this will create a table of all the "top" layer of centroids in the database, unless it already exists there
# the table will consist of an x value, y, value, z value

try:
    cur.execute('CREATE TABLE TopVoxels (u int, v int, w int);')
    print("I just created a table!")
    cur.execute('INSERT INTO TopVoxels (SELECT i,j, max(k) from data_model GROUP BY i,j);')

except:
    print ("This table is already on the database aswell!")


# CHECK ME -- need to know exactly how this works
conn.rollback()
cur.execute('SELECT DISTINCT * FROM TopVoxels;')
data_model_list = cur.fetchall()
print("sample of top layer voxels:")
print(data_model_list[:300])
print("amount of top layer voxels:")
print(len(data_model_list))

conn.commit()
cur.close()
conn.close()

#this will write a csv file to directory - need to figure out a better way to do this
with open('topVoxels.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in data_model_list:
        writer.writerow(line)
    print("You just saved a CSV of the top voxels in your directory!")



