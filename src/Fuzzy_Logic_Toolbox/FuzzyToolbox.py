# This file contains the Membership Functions in Lynn's Fuzzy Toolbox
# Created September 13, 2019
# Updated December 29, 2020
import numpy as np


def memb_left_sh(x, shoulder):
    """ This function determines the membership value belonging to the user defined left shoulder
    INPUTS
    x - the value
    center - center of user defined left shoulder
    right - right value of user defined left shoulder
    left - left value of user defined left shoulder
    """
    left = shoulder[0]
    center = shoulder[1]
    right = shoulder[2]
    if left <= x < center:
        # Left side of left shoulder
        membership = 1
    elif center <= x <= right:
        # Right side of left shoulder
        membership = (x - right) / (center - right)
    else:
        # not in left shoulder
        membership = 0

    return membership


def memb_tri(x, triangle):
    """This function determines the membership value belonging to the user defined triangle
    INPUTS
    x - the value
    triangle - user defined triangle in order:left, center, right"""
    left = triangle[0]
    center = triangle[1]
    right = triangle[2]

    if left <= x < center:
        # Left side of triangle
        membership = (x - left) / (center - left)
    elif center <= x <= right:
        # Right side of triangle
        if (center - right) == 0:
            membership = 1
        else:
            membership = (x - right) / (center - right)
    else:
        # not in triangle
        membership = 0

    return membership


def memb_right_sh(x, shoulder):
    """This function determines the membership value belonging to the user defined right shoulder.
    INPUTS
    x - the value
    center - center of user defined right shoulder
    right - right value of user defined right shoulder
    left - left value of user defined right shoulder"""
    left = shoulder[0]
    center = shoulder[1]
    right = shoulder[2]
    if left <= x < center:
        # Left side of right shoulder
        membership = (x - left) / (center - left)
    elif center <= x <= right:
        # Right side of right shoulder
        membership = 1
    else:
        # not in right shoulder
        membership = 0

    return membership


def defuzz_coa(y, output_shape):
    """ Defuzzification using the center of area"""
    left = output_shape[0]
    center = output_shape[1]
    right = output_shape[2]
    area = .5 * (right - left)
    # scale the output membership function using rule weight
    scaled_function = center * y * area
    return scaled_function, area


def intersection_pt(triangle_left, triangle_right):
    """ get intersection point of two output triangles"""
    a, b, c = triangle_left[0], triangle_left[1], triangle_left[2]
    d, e, f = triangle_right[0], triangle_right[1], triangle_right[2]
    x = (c * (b - c) - d * (e - d)) / (b - c - e + d)
    y = (e - d) * (x - d)
    return x, y


def overlapping_triangle_areas(triangle_list):
    """ Get total overlapping areas of output triangles
    -----------
    Parameters
    triangle_list - triangles, in order"""
    overlapping_area = 0
    for i in np.arange(0, len(triangle_list) - 1, 1):
        x, y = intersection_pt(triangle_list[i], triangle_list[i + 1])
        overlapping_area += .5 * y * (x - triangle_list[i][2])
        overlapping_area += .5 * y * (triangle_list[i + 1][0] - x)
    return overlapping_area


def defuzz_cog(y, output_shape):
    """Defuzzification using the center of gravity
    INPUTS
    y - the membership value
    output_shape - vector defining the output shape"""
    # Read in the values of the output triangle
    left = output_shape[0]
    center = output_shape[1]
    right = output_shape[2]

    if (center - left) == 0:
        x_left = left
    else:
        # find the corresponding left side value of triangle
        # so that the cut off triangle may be used
        slope_left = 1 / (center - left)
        x_left = y * slope_left + left

    if (center - right) == 0:
        x_right = right
    else:
        # find the corresponding right side value of triangle
        # so that the cut off triangle may be used
        slope_right = 1 / (center - right)
        x_right = (y / slope_right) + right

    # Calculate the centroid of the cut off triangle
    centroid = (left + right + x_left + x_right) / 4
    # Calculate the area of the cut off triangle
    area = y * .5 * ((x_right - x_left) + (right - left))
    if y == 0:
        COG_num = 0
        COG_den = 0
    else:
        COG_num = (area * centroid)  # The numerator contribution
        COG_den = area  # The denomination contribution

    return COG_num, COG_den
