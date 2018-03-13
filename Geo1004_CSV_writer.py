import psycopg2
import csv


with open('PointCloud.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    point_list = []
    for row in reader:
        float_values = []
        for num in row:
            float_values.append(float(num))
        point_list.append(float_values)

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='1234'")

except:
    print ("I am unable to connect to the database")


cur = conn.cursor()

cur.execute('CREATE TABLE PointCloudTable3 (x float, y float, z float);')

query = 'INSERT INTO PointCloudTable3 (x, y, z) VALUES (%s, %s, %s);'

for row in point_list:
    pnt = (row[0],row[1],row[2])
    cur.execute(query, pnt)

conn.commit()
cur.close()
conn.close()
