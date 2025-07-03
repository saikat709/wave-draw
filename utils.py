def get_distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return int(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5)