from kdtree import KDTree

points = [
    ((0, 3), (1)),
    ((1, 3), (2)),
    ((1, 4), (3)),
    ((2, 3), (4)),
    ((3, 1), (5)),
    ((3, 2), (6)),
    ((4, 0), (7)),
    ((4, 3), (8)),
    ((4, 4), (9)),
    ((5, 2), (10)),
    ((5, 3), (11)),
    ((6, 2), (12))
]

tree = KDTree(points)
print(" ".join(map(str, tree.search((1,1), (3,3)))))

tree.insert(((2, 2), 13))
print(" ".join(map(str, tree.search((1,1), (3,3)))))
