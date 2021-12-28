import numpy as np


def get_ga_vector_indexes(mfs_info):
    def get_ga_vector_index(mfs_input1, mfs_input2, mfs_output, the_index, mfs_input3=0):
        """ This is a function that prints the indexes for the vector of values from the ga
        IT is very basic - works if all are the same format, good start"""
        iterator = mfs_input1 * 2 + mfs_input2 * 2 + mfs_input1 * mfs_input2 + mfs_output * 2
        if mfs_input3 > 0:
            iterator = mfs_input1 * 2 + mfs_input2 * 2 + mfs_input3 * 2 + mfs_input1 * mfs_input2 * mfs_input3 + mfs_output * 2
        print("[", the_index, ":", the_index + iterator, "]")
        return iterator

    iterating = 0
    for fis in mfs_info:
        try:
            input3 = fis[3]
        except IndexError:
            input3 = 0
        add = get_ga_vector_index(fis[1], fis[2], 3, iterating, input3)
        iterating += add


def get_upper_bound(number_mfs_in_order):
    """ Get the list of the upper bound values for the ga"""
    upper_bound = []

    for fis in number_mfs_in_order:

        # For the centers of input 1 triangles
        for i in np.arange(fis[1]):
            upper_bound.append(1.1)
        # For the widths of input 1 triangles
        for i in np.arange(fis[1]):
            upper_bound.append(.5)

        # For the centers of input 2 triangles
        for i in np.arange(fis[2]):
            upper_bound.append(1.1)
        # For the widths of input 2 triangles
        for i in np.arange(fis[2]):
            upper_bound.append(.5)

        if fis[0] == '3_1':
            # For the centers of input 3 triangles
            for i in np.arange(fis[3]):
                upper_bound.append(1.1)
            # For the widths of input 3 triangles
            for i in np.arange(fis[3]):
                upper_bound.append(.5)

        # For the output triangles - all same number
        for i in np.arange(3):
            upper_bound.append(1.1)
        # For the widths of output triangles
        for i in np.arange(3):
            upper_bound.append(.5)

        # For the rules
        number_of_rules = fis[1] * fis[2]
        if fis[0] == '3_1':
            number_of_rules = number_of_rules * fis[3]
        for i in np.arange(number_of_rules):
            # The 3 corresponds to the number of output triangles
            upper_bound.append(3)

    return upper_bound


def get_upper_bound_bc(number_mfs_in_order):
    """ Get the list of the upper bound values for the ga"""
    upper_bound = []

    for fis in number_mfs_in_order:

        # For the centers of input 1 triangles
        for i in np.arange(fis[1]):
            upper_bound.append(12)
        # For the widths of input 1 triangles
        for i in np.arange(fis[1]):
            upper_bound.append(8)

        # For the centers of input 2 triangles
        for i in np.arange(fis[2]):
            upper_bound.append(12)
        # For the widths of input 2 triangles
        for i in np.arange(fis[2]):
            upper_bound.append(8)

        if fis[0] == '3_1':
            # For the centers of input 3 triangles
            for i in np.arange(fis[3]):
                upper_bound.append(12)
            # For the widths of input 3 triangles
            for i in np.arange(fis[3]):
                upper_bound.append(8)

        # For the output triangles - all same number
        for i in np.arange(3):
            upper_bound.append(12)
        # For the widths of output triangles
        for i in np.arange(3):
            upper_bound.append(8)

        # For the rules
        number_of_rules = fis[1] * fis[2]
        if fis[0] == '3_1':
            number_of_rules = number_of_rules * fis[3]
        for i in np.arange(number_of_rules):
            # The 3 corresponds to the number of output triangles
            upper_bound.append(3)

    return upper_bound

