//C# Code adapted for Rhino3D and Grasshopper by Pirouz Nourian, Design Informatics, TU Delft, from http://paulbourke.net/papers/triangulate/

//Original code written by Christian Stelzl, based on a paper by Paul Bourke:

// Credit to Paul Bourke (paul.bourke@uwa.edu.au) for the original Fortran 77 Program.
// Check out: http://local.wasp.uwa.edu.au/~pbourke/
// You can use this code however you like providing the above credits remain in tact.
// First converted to a standalone C# 2.0 library by Morten Nielsen (www.iter.dk)
// Performance enhanced C# 2.0 library by Christian Stelzl (www.ceometric.com) Sep. 2008
/// <summary>A 2d Delaunay triangulation class.</summary>
/// <remarks>The triangulation doesn't support multiple points with identical x and y coordinates,
/// nor does it support dublicate points.
/// Vertex-lists with duplicate points may result in strange triangulations with intersecting edges or
/// may cause the algorithm to fail.
/// Uses a simple O(n**2) algorithm based on Paul Bourke's "An Algorithm for Interpolating
/// Irregularly-Spaced Data with Applications in Terrain Modelling".
/// Uses an enhanced incircle-predicate for counterclockwise orientated triangles.</remarks>
/// <summary>Performs the 2d Delaunay triangulation on a set of n vertices in O(n**2) time.</summary>
/// <param name="triangulationPoints">The points to triangulate.</param>
/// <returns>A list of Delaunay-triangles.</returns>
/// <summary>Performs the 2d Delaunay triangulation on a set of n vertices in O(n**2) time.</summary>
/// <param name="triangulationPoints">The points to triangulate.</param>
/// <returns>A list of Delaunay-triangles.</returns>

public List<Triangle> Triangulate(List<Point3d> triangulationPoints)
{
if ( triangulationPoints.Count < 3 ) throw new ArgumentException("Can not triangulate less than three vertices!");

// The triangle list
List<Triangle> triangles = new List<Triangle>(); ;

// The "supertriangle" which encompasses all triangulation points.
// This triangle initializes the algorithm and will be removed later.
Triangle superTriangle = this.SuperTriangle(triangulationPoints);
triangles.Add(superTriangle);

// Include each point one at a time into the existing triangulation
for ( int i = 0; i < triangulationPoints.Count; i++ )
{
  // Initialize the edge buffer.
  List<Edge> EdgeBuffer = new List<Edge>();

  // If the actual vertex lies inside the circumcircle, then the three edges of the
  // triangle are added to the edge buffer and the triangle is removed from list.
  for ( int j = triangles.Count - 1; j >= 0; j-- )
  {
    Triangle t = triangles[j];
    if ( t.ContainsInCircumcircle(triangulationPoints[i]) > 0 )
    {
      EdgeBuffer.Add(new Edge(t.Vertex1, t.Vertex2));
      EdgeBuffer.Add(new Edge(t.Vertex2, t.Vertex3));
      EdgeBuffer.Add(new Edge(t.Vertex3, t.Vertex1));
      triangles.RemoveAt(j);
    }
  }

  // Remove duplicate edges. This leaves the convex hull of the edges.
  // The edges in this convex hull are oriented counterclockwise!
  for ( int j = EdgeBuffer.Count - 2; j >= 0; j-- )
  {
    for ( int k = EdgeBuffer.Count - 1; k >= j + 1; k-- )
    {
      if ( EdgeBuffer[j] == EdgeBuffer[k] )
      {
        EdgeBuffer.RemoveAt(k);
        EdgeBuffer.RemoveAt(j);
        k--;
        continue;
      }
    }
  }

  // Generate new counterclockwise oriented triangles filling the "hole" in
  // the existing triangulation. These triangles all share the actual vertex.
  for ( int j = 0; j < EdgeBuffer.Count; j++ )
  {
    triangles.Add(new Triangle(EdgeBuffer[j].StartPoint, EdgeBuffer[j].EndPoint, triangulationPoints[i]));
  }
}

// We don't want the supertriangle in the triangulation, so
// remove all triangles sharing a vertex with the supertriangle.
for ( int i = triangles.Count - 1; i >= 0; i-- )
{
  if ( triangles[i].SharesVertexWith(superTriangle) ) triangles.RemoveAt(i);
}

// Return the triangles
return triangles;
}

/// <summary>Returns a triangle that encompasses all triangulation points.</summary>
/// <param name="triangulationPoints">A list of triangulation points.</param>
/// <returns>Returns a triangle that encompasses all triangulation points.</returns>
private Triangle SuperTriangle(List<Point3d> triangulationPoints)
{
double M = triangulationPoints[0].X;

// get the extremal x and y coordinates
for ( int i = 1; i < triangulationPoints.Count; i++ )
{
  double xAbs = Math.Abs(triangulationPoints[i].X);
  double yAbs = Math.Abs(triangulationPoints[i].Y);
  if ( xAbs > M ) M = xAbs;
  if ( yAbs > M ) M = yAbs;
}

// make a triangle
Point3d sp1 = new Point3d(10 * M, 0, 0);
Point3d sp2 = new Point3d(0, 10 * M, 0);
Point3d sp3 = new Point3d(-10 * M, -10 * M, 0);

return new Triangle(sp1, sp2, sp3);
}
public class Triangle
{
/// <summary>The first vertex of the triangle.</summary>
public Point3d Vertex1;
/// <summary>The second vertex of the triangle.</summary>
public Point3d Vertex2;
/// <summary>The third vertex of the triangle.</summary>
public Point3d Vertex3;

#region Constructor

/// <summary>Constructs a triangle from three points.</summary>
/// <param name="vertex1">The first vertex of the triangle.</param>
/// <param name="vertex2">The second vertex of the triangle.</param>
/// <param name="vertex3">The third vertex of the triangle.</param>
public Triangle(Point3d vertex1, Point3d vertex2, Point3d vertex3)
{
  this.Vertex1 = vertex1;
  this.Vertex2 = vertex2;
  this.Vertex3 = vertex3;
}

#endregion

#region Methods

/// <summary>Tests if a point lies in the circumcircle of the triangle.</summary>
/// <param name="point">A <see cref="Point3d"/>.</param>
/// <returns>For a counterclockwise order of the vertices of the triangle, this test is
/// <list type ="bullet">
/// <item>positive if <paramref name="point"/> lies inside the circumcircle.</item>
/// <item>zero if <paramref name="point"/> lies on the circumference of the circumcircle.</item>
/// <item>negative if <paramref name="point"/> lies outside the circumcircle.</item></list></returns>
/// <remarks>The vertices of the triangle must be arranged in counterclockwise order or the result
/// of this test will be reversed. This test ignores the z-coordinate of the vertices.</remarks>
public double ContainsInCircumcircle(Point3d point)
{
  double ax = this.Vertex1.X - point.X;
  double ay = this.Vertex1.Y - point.Y;
  double bx = this.Vertex2.X - point.X;
  double by = this.Vertex2.Y - point.Y;
  double cx = this.Vertex3.X - point.X;
  double cy = this.Vertex3.Y - point.Y;

  double det_ab = ax * by - bx * ay;
  double det_bc = bx * cy - cx * by;
  double det_ca = cx * ay - ax * cy;

  double a_squared = ax * ax + ay * ay;
  double b_squared = bx * bx + by * by;
  double c_squared = cx * cx + cy * cy;

  return a_squared * det_bc + b_squared * det_ca + c_squared * det_ab;
}

/// <summary>Tests if two triangles share at least one vertex.</summary>
/// <param name="triangle">A <see cref="Triangle"/>.</param>
/// <returns>Returns true if two triangles share at least one vertex, false otherwise.</returns>
public bool SharesVertexWith(Triangle triangle)
{
  if ( this.Vertex1.X == triangle.Vertex1.X && this.Vertex1.Y == triangle.Vertex1.Y ) return true;
  if ( this.Vertex1.X == triangle.Vertex2.X && this.Vertex1.Y == triangle.Vertex2.Y ) return true;
  if ( this.Vertex1.X == triangle.Vertex3.X && this.Vertex1.Y == triangle.Vertex3.Y ) return true;

  if ( this.Vertex2.X == triangle.Vertex1.X && this.Vertex2.Y == triangle.Vertex1.Y ) return true;
  if ( this.Vertex2.X == triangle.Vertex2.X && this.Vertex2.Y == triangle.Vertex2.Y ) return true;
  if ( this.Vertex2.X == triangle.Vertex3.X && this.Vertex2.Y == triangle.Vertex3.Y ) return true;

  if ( this.Vertex3.X == triangle.Vertex1.X && this.Vertex3.Y == triangle.Vertex1.Y ) return true;
  if ( this.Vertex3.X == triangle.Vertex2.X && this.Vertex3.Y == triangle.Vertex2.Y ) return true;
  if ( this.Vertex3.X == triangle.Vertex3.X && this.Vertex3.Y == triangle.Vertex3.Y ) return true;

  return false;
}

#endregion
}
public class Edge
{
/// <summary>The start point of the edge.</summary>
public Point3d StartPoint;
/// <summary>The end point of the edge.</summary>
public Point3d EndPoint;

#region Constructor

/// <summary>Constructs an edge from two points.</summary>
/// <param name="startPoint">The start point of the edge.</param>
/// <param name="endPoint">The end point of the edge.</param>
public Edge(Point3d startPoint, Point3d endPoint)
{
  this.StartPoint = startPoint;
  this.EndPoint = endPoint;
}

#endregion

#region Operators

/// <summary>A hash code for this edge.</summary>
/// <returns>Returns the hash code for this edge.</returns>
public override int GetHashCode()
{
  return this.StartPoint.GetHashCode() ^ this.EndPoint.GetHashCode();
}

/// <summary>Tests if two edges are considered equal.</summary>
/// <param name="obj">An <see cref="Edge"/> object.</param>
/// <returns>Returns true if two edges are considered equal, false otherwise.</returns>
/// <remarks>Two edges are considered equal if they contain the same points.
/// This is, two equal edges may have interchanged start and end points.</remarks>
public override bool Equals(object obj)
{
  return this == (Edge) obj;
}

/// <summary>Tests if two edges are equal.</summary>
/// <param name="left">A first <see cref="Edge"/>.</param>
/// <param name="right">A second <see cref="Edge"/>.</param>
/// <returns>Returns true if two edges are considered equal, false otherwise.</returns>
/// <remarks>Two edges are considered equal if they contain the same points.
/// This is, two equal edges may have interchanged start and end points.</remarks>
public static bool operator ==(Edge left, Edge right)
{
  if ( ( (object) left ) == ( (object) right ) )
  {
    return true;
  }

  if ( ( ( (object) left ) == null ) || ( ( (object) right ) == null ) )
  {
    return false;
  }

  return ( ( left.StartPoint == right.StartPoint && left.EndPoint == right.EndPoint ) ||
    ( left.StartPoint == right.EndPoint && left.EndPoint == right.StartPoint ) );
}

/// <summary>Tests if two edges are considered equal.</summary>
/// <param name="left">A first <see cref="Edge"/>.</param>
/// <param name="right">A second <see cref="Edge"/>.</param>
/// <returns>Returns false if two edges are considered equal, true otherwise.</returns>
/// <remarks>Two edges are considered equal if they contain the same points.
/// This is, two equal edges may have interchanged start and end points.</remarks>
public static bool operator !=(Edge left, Edge right)
{
  return left != right;
}

#endregion

}
