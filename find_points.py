from skspatial.objects import Line, Sphere

sphere = Sphere([0, 0, 0], 1)
line = Line([0, 0, 0], [1, 1, 1])

point_a, point_b = sphere.intersect_line(line)
print(point_a)
