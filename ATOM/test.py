import Rhino.Geometry as rg
import rhinoscriptsyntax as rs

class Triangle:

     def __init__(self, vertex1, vertex2, vertex3):
         self.Vertex1 = vertex1
         self.Vertex2 = vertex2
         self.Vertex3 = vertex3



def SharesVertexWith(triangle1,triangle2):
    if triangle1.Vertex1.X == triangle2.Vertex1.X and triangle1.Vertex1.Y == triangle2.Vertex1.Y:
        return True
    if triangle1.Vertex1.X == triangle2.Vertex2.X and triangle1.Vertex1.Y== triangle2.Vertex2.Y:
        return True
    if triangle1.Vertex1.X == triangle2.Vertex3.X and triangle1.Vertex1.Y== triangle2.Vertex3.Y:
        return True

    if triangle1.Vertex2.X == triangle2.Vertex1.X and triangle2.Vertex1.Y== triangle2.Vertex1.Y:
        return True
    if triangle1.Vertex2.X == triangle2.Vertex2.X and triangle2.Vertex1.Y== triangle2.Vertex2.Y:
        return True
    if triangle1.Vertex2.X == triangle2.Vertex3.X and triangle2.Vertex1.Y== triangle2.Vertex3.Y:
        return True

    if triangle1.Vertex3.X == triangle2.Vertex1.X and triangle2.Vertex3.Y== triangle2.Vertex1.Y:
        return True
    if triangle1.Vertex3.X == triangle2.Vertex2.X and triangle2.Vertex3.Y== triangle2.Vertex2.Y:
        return True
    if triangle1.Vertex3.X == triangle2.Vertex3.X and triangle2.Vertex3.Y== triangle2.Vertex3.Y:
        return True

    return False


# you would use this to compare if a point lies in the circumcirlce of a triangle
# vertices of the triangle needs to be arranged in a clockwise fashion
# positive if inside
# negative if outside
# zero if on the circle


def ContainsInCircumcircle(triangle, point):
    ax = triangle.Vertex1.X - point.X
    ay = triangle.Vertex1.Y - point.Y
    bx = triangle.Vertex2.X - point.X
    by = triangle.Vertex2.Y - point.Y
    cx = triangle.Vertex3.X - point.X
    cy = triangle.Vertex3.Y - point.Y

    det_ab = ax * by - bx * ay
    det_bc = bx * cy - cx * by
    det_ca = cx * cx - cy * cy

    a_squared = ax * ax + ay * ay
    b_squared = bx * bx + by * by
    c_squared = cx * cx + cy * cy

    return a_squared * det_bc + b_squared * det_ca + c_squared * det_ab

def SuperTriangle(triangulationPoints):
     M = triangulationPoints[0].X

     for i in range(len(triangulationPoints)):
         xAbs = abs(triangulationPoints[i].X)
         yAbs = abs(triangulationPoints[i].Y)

         if xAbs > M:
             M = xAbs
         if yAbs > M:
             M = yAbs

     #making the super triangle with teh extremes
     sp1 = rg.Point3d(10 * M , 0 , 0)
     sp2 = rg.Point3d(0, 10 * M , 0)
     sp3 = rg.Point3d(-10 * M , -10 * M , 0)

     return Triangle(sp1, sp2, sp3)

def Triangulate(triangulationPoints):

    if triangulationPoints < 3:
        Print("I can't triangulate this..")

    triangles = []
    # this is the super triangle that encompasses all the triangulationPoints
    # it will be deleted at the end
    superTriangle = SuperTriangle(triangulationPoints)
    triangles.append(superTriangle)
    #<= range(len(triangles))

    for i in range(len(triangulationPoints)):
        EdgeBuffer = []
        j = (len(triangles))-1
        while j >= 0:
            t = triangles[j]
            if ContainsInCircumcircle(t,triangulationPoints[i]) > 0:
                vertex1 = rg.Point3d(t.Vertex1[0], t.Vertex1[1],t.Vertex1[2])
                vertex2 = rg.Point3d(t.Vertex2[0], t.Vertex2[1],t.Vertex2[2])
                vertex3 = rg.Point3d(t.Vertex3[0], t.Vertex3[1],t.Vertex2[2])
                EdgeBuffer.append(rg.Line(vertex1, vertex2))
                EdgeBuffer.append(rg.Line(vertex2, vertex3))
                EdgeBuffer.append(rg.Line(vertex3, vertex1))
                triangles.pop(j)
            j = j - 1

        e = len(EdgeBuffer)
        while e >= 0:
            k = len(EdgeBuffer)
            while k >= (e + 1):
                if EdgeBuffer[e] == EdgeBuffer[k]:
                    EdgeBuffer.pop(k)
                    EdgeBuffer.pop(e)
                k = k - 1
            e = e - 1

        for j in range(len(EdgeBuffer)):
            if j < len(EdgeBuffer):
                triangles.append(Triangle(EdgeBuffer[j].StartPoint, EdgeBuffer[j].EndPoint, triangulationPoints[i]))

    i = len(triangles)-1
    while i >= 0:
        if SharesVertexWith(triangles[i],superTriangle):
            triangles.pop(i)
        i = i - 1

    return triangles

Triangles = Triangulate(points)

mesh_surface = rg.Mesh()
k = 0
for T in Triangles:
    mesh_surface.Vertices.AddVertices(T.Vertex1,T.Vertex2,T.Vertex3)
    mesh_surface.Faces.AddFace(k,k+1,k+2)
    k = k+3
a = mesh_surface
