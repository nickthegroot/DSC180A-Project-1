import numpy as np
from bs4 import Tag
from shapely.geometry import Polygon


def tag_to_shape(tag: Tag) -> Polygon:
    poly = tag.find('polygon')
    assert poly != None and 'points' in poly.attrs, "No valid polygon associated with tag"

    points_str = poly['points'].strip().split(' ')
    points = np.array([
        [float(x), float(y)] for x, y in
        (point.split(',') for point in points_str)
    ])
    points = np.round(points)

    return Polygon(points)