# This file contains the Membership Functions in Lynn's Fuzzy Toolbox
# Created January 8, 2021

import numpy as np
import math

from FuzzyToolbox import memb_tri as membership_of_triangle


def print_indexes(fuzzy_system_info):
    """ This is a function that prints the indexes for the vector of values from the ga """

    def get_one_index(current_index, mfs_input1, mfs_input2, mfs_output, mfs_input3=0):
        if mfs_input3 == 0:
            common_iterator = mfs_input1 * 2 + mfs_input2 * 2 + mfs_input1 * mfs_input2 + mfs_output * 2
        else:
            common_iterator = mfs_input1 * 2 + mfs_input2 * 2 + mfs_input3 * 2 + mfs_input1 * mfs_input2 * mfs_input3 + mfs_output * 2

        print("[", current_index, ":", current_index + common_iterator, "]")
        return current_index + common_iterator

    start_index = 0
    for fis in fuzzy_system_info:
        try:
            start_index = get_one_index(start_index, fis[1], fis[2], 3, mfs_input3=fis[3])
        except IndexError:
            start_index = get_one_index(start_index, fis[1], fis[2], 3)


def defuzz_coa(y, output_centers, output_widths, rule):
    """ Defuzzification using the center of area"""
    if len(output_centers) > math.ceil(rule) - 1 >= 0:
        output_triangle_index = math.ceil(rule) - 1
    else:
        output_triangle_index = len(output_centers) - 1
    left = output_centers[output_triangle_index] - output_widths[output_triangle_index] / 2
    center = output_centers[output_triangle_index]
    right = output_centers[output_triangle_index] + output_widths[output_triangle_index] / 2
    area = .5 * (right - left)
    # scale the output membership function using rule weight
    scaled_function = center * y * area
    return scaled_function, area


def input_to_membership(input_value, centers, widths):
    """ This function takes the parameters:
    input - one input value
    centers - list of centers for this input
    widths - list of widths for this input
    ______
    centers and widths must be same length, widths must be positive"""
    # Sort the triangle centers from small to large for simplicity
    centers = np.sort(centers)
    memberships = []
    for center, width in zip(centers, widths):
        triangle = [center - width, center, center + width]
        membership = membership_of_triangle(input_value, triangle)
        memberships.append(membership)

    return memberships


def split_vector_given(mfs1_num, mfs2_num, mfs3_num, ga_vector, mfs_out_num):
    """ Split the numbers into the correct lists
    If output membership functions are 0, then the output shapes are fixed, else"""
    # Initialize the vectors we need
    centers_in1, widths_in1, centers_in2, widths_in2, centers_in3, widths_in3 = [], [], [], [], [], []
    centers_out, widths_out, rules_values = [], [], []
    for i, value in enumerate(ga_vector):
        if i < mfs1_num:
            centers_in1.append(value)
        elif i < mfs1_num * 2:
            widths_in1.append(value)
        elif i < mfs1_num * 2 + mfs2_num:
            centers_in2.append(value)
        elif i < mfs1_num * 2 + mfs2_num * 2:
            widths_in2.append(value)
        elif i < mfs1_num * 2 + mfs2_num * 2 + mfs3_num:
            centers_in3.append(value)
        elif i < mfs1_num * 2 + mfs2_num * 2 + mfs3_num * 2:
            widths_in3.append(value)
        # Output mfs
        elif i < mfs1_num * 2 + mfs2_num * 2 + mfs3_num * 2 + mfs_out_num:
            centers_out.append(value)
        elif i < mfs1_num * 2 + mfs2_num * 2 + mfs3_num * 2 + mfs_out_num * 2:
            widths_out.append(value)
        else:
            rules_values.append(value)
    # Sort the centers for ease of understanding system
    centers_in1.sort()
    centers_in2.sort()
    centers_in3.sort()
    centers_out.sort()
    return centers_in1, widths_in1, centers_in2, widths_in2, centers_in3, widths_in3, centers_out, widths_out, rules_values


def fuzzy2_1(input_1, input_1_mfs_num, input_2, input_2_mfs_num, ga_vec, output_mfs_num=0):
    """
    This is the two input one output fuzzy
    -------------------------
    input_1, input 2- input values
    input_1_mfs_num, input_2_mfs_num, output_mfs_num - number of membership functions the input/output spaces have
    ga_vec - the values needed from the ga
    """

    all_vectors = split_vector_given(input_1_mfs_num, input_2_mfs_num, 0, ga_vec, output_mfs_num)
    centers_1, widths_1, centers_2, widths_2, centers_3, widths_3, output_centers, output_widths, rules = all_vectors

    memberships_input_1 = input_to_membership(input_1, centers_1, widths_1)
    memberships_input_2 = input_to_membership(input_2, centers_2, widths_2)

    # Collect all the and rules
    and_rules = []
    for mem_1 in memberships_input_1:
        for mem_2 in memberships_input_2:
            and_rules.append(min(mem_1, mem_2))

    # Defuzzification using the center of area
    lam_numerator = 0
    lam_denominator = 0
    for and_rule, rule in zip(and_rules, rules):
        output_value = defuzz_coa(and_rule, output_centers, output_widths, rule)
        lam_numerator += output_value[0]
        lam_denominator += output_value[1]

    # Check to make sure denominator is not 0
    if lam_denominator == 0:
        lam = 0
    else:
        lam = lam_numerator / lam_denominator

    # return the output of this fis
    return lam


def fuzzy3_1(input_1, input_1_mfs_num, input_2, input_2_mfs_num, input_3, input_3_mfs_num, ga_vec, output_mfs_num=0):
    """
    This is the two input one output fuzzy
    -------------------------
    input_1, input 2- input values
    input_1_mfs_num, input_2_mfs_num, output_mfs_num - number of membership functions the input/output spaces have
    ga_vec - the values needed from the ga
    """

    all_vectors = split_vector_given(input_1_mfs_num, input_2_mfs_num, input_3_mfs_num, ga_vec, output_mfs_num)
    centers_1, widths_1, centers_2, widths_2, centers_3, widths_3, output_centers, output_widths, rules = all_vectors

    memberships_input_1 = input_to_membership(input_1, centers_1, widths_1)
    memberships_input_2 = input_to_membership(input_2, centers_2, widths_2)
    memberships_input_3 = input_to_membership(input_3, centers_3, widths_3)

    # Collect all the and rules
    and_rules = []
    # And rules for 1 with 2 and 3
    for mem_1 in memberships_input_1:
        for mem_2, mem_3 in zip(memberships_input_2, memberships_input_3):
            and_rules.append(min(mem_1, mem_2))
            and_rules.append(min(mem_1, mem_3))
    # And rules for 2 with 3
    for mem_2 in memberships_input_2:
        for mem_3 in memberships_input_3:
            and_rules.append(min(mem_2, mem_3))

    # Defuzzification using the center of area
    lam_numerator = 0
    lam_denominator = 0
    for and_rule, rule in zip(and_rules, rules):
        output_value = defuzz_coa(and_rule, output_centers, output_widths, rule)
        lam_numerator += output_value[0]
        lam_denominator += output_value[1]

    # Check to make sure denominator is not 0
    if lam_denominator == 0:
        lam = 0
    else:
        lam = lam_numerator / lam_denominator

    # return the output of this fis
    return lam


class FuzzySystem:
    def __init__(self,
                 input_1_mfs_number: int,
                 input_2_mfs_number: int,
                 input_3_mfs_number: int,
                 input_4_mfs_number: int,
                 output_1_mfs_number: int,
                 output_2_mfs_number: int):
        self.input_1_mfs_number = input_1_mfs_number
        self.input_2_mfs_number = input_2_mfs_number
        self.input_3_mfs_number = input_3_mfs_number
        self.input_4_mfs_number = input_4_mfs_number
        self.output_1_mfs_number = output_1_mfs_number
        self.output_2_mfs_number = output_2_mfs_number

        # The indexes to split the ga vector each time
        self.rul_num = input_1_mfs_number ** 4
        self.ga_indexes = self.get_ga_vector_indexs()
        self.rul_num = input_1_mfs_number ** 4

    def get_ga_vector_indexs(self):
        """ Get the indexes to split the ga vector for the given system"""
        # Input membership functions first
        centers_in1_idx = 0 + self.input_1_mfs_number
        widths_in1_idx = 0 + self.input_1_mfs_number * 2
        centers_in2_idx = widths_in1_idx + self.input_2_mfs_number
        widths_in2_idx = widths_in1_idx + self.input_2_mfs_number * 2
        centers_in3_idx = widths_in2_idx + self.input_3_mfs_number
        widths_in3_idx = widths_in2_idx + self.input_3_mfs_number * 2
        centers_in4_idx = widths_in3_idx + self.input_4_mfs_number
        widths_in4_idx = widths_in3_idx + self.input_4_mfs_number * 2

        # Output membership functions split next
        centers_out1_idx = widths_in4_idx + self.output_1_mfs_number
        widths_out1_idx = widths_in4_idx + self.output_1_mfs_number * 2
        centers_out2_idx = widths_out1_idx + self.output_2_mfs_number
        widths_out2_idx = widths_out1_idx + self.output_2_mfs_number * 2

        # The rules are whats left
        rules_1_idx = widths_out2_idx + self.rul_num
        idxs = [centers_in1_idx, widths_in1_idx, centers_in2_idx, widths_in2_idx, centers_in3_idx, widths_in3_idx,
                centers_in4_idx, widths_in4_idx, centers_out1_idx, widths_out1_idx, centers_out2_idx, widths_out2_idx,
                rules_1_idx]
        return idxs

    def split_ga_vector(self, ga_chromosome):
        # Inputs
        centers_in1 = ga_chromosome[0: self.ga_indexes[0]]
        widths_in1 = ga_chromosome[self.ga_indexes[0]: self.ga_indexes[1]]
        centers_in2 = ga_chromosome[self.ga_indexes[1]: self.ga_indexes[2]]
        widths_in2 = ga_chromosome[self.ga_indexes[2]: self.ga_indexes[3]]
        centers_in3 = ga_chromosome[self.ga_indexes[3]: self.ga_indexes[4]]
        widths_in3 = ga_chromosome[self.ga_indexes[4]: self.ga_indexes[5]]
        centers_in4 = ga_chromosome[self.ga_indexes[5]: self.ga_indexes[6]]
        widths_in4 = ga_chromosome[self.ga_indexes[6]: self.ga_indexes[7]]
        # Outputs
        centers_out1 = ga_chromosome[self.ga_indexes[7]: self.ga_indexes[8]]
        widths_out1 = ga_chromosome[self.ga_indexes[8]: self.ga_indexes[9]]
        centers_out2 = ga_chromosome[self.ga_indexes[9]: self.ga_indexes[10]]
        widths_out2 = ga_chromosome[self.ga_indexes[10]: self.ga_indexes[11]]
        # Rules
        rules_values1 = ga_chromosome[self.ga_indexes[11]:self.ga_indexes[12]]
        rules_values2 = ga_chromosome[self.ga_indexes[12]:]
        # Sort the centers for ease of understanding system
        centers_in1.sort()
        centers_in2.sort()
        centers_in3.sort()
        centers_in1.sort()
        centers_out1.sort()
        centers_out2.sort()
        return centers_in1, widths_in1, centers_in2, widths_in2, centers_in3, widths_in3, centers_in4, widths_in4, \
               centers_out1, widths_out1, centers_out2, widths_out2, rules_values1, rules_values2

    def fuzzy4_2(self, input_1, input_2, input_3, input_4, ga_vec):
        """
        This is the 4 input 2 output fuzzy
        -------------------------
        ga_vec - the values needed from the ga
        """

        centers_1, widths_1, centers_2, widths_2, centers_3, widths_3, centers_4, widths_4, \
        centers_out1, widths_out1, centers_out2, widths_out2, rules_values1, rules_values2 = self.split_ga_vector(ga_vec)

        memberships_input_1 = input_to_membership(input_1, centers_1, widths_1)
        memberships_input_2 = input_to_membership(input_2, centers_2, widths_2)
        memberships_input_3 = input_to_membership(input_3, centers_3, widths_3)
        memberships_input_4 = input_to_membership(input_4, centers_4, widths_4)

        # Get the and rules - minimum
        and_1_2 = np.minimum(memberships_input_1, memberships_input_2)
        and_1_3 = np.minimum(memberships_input_1, memberships_input_3)
        and_1_4 = np.minimum(memberships_input_1, memberships_input_4)
        and_2_3 = np.minimum(memberships_input_2, memberships_input_3)
        and_2_4 = np.minimum(memberships_input_2, memberships_input_4)
        and_3_4 = np.minimum(memberships_input_3, memberships_input_4)

        # Collect all the and rules
        and_rules = np.concatenate((and_1_2, and_1_3, and_1_4, and_2_3, and_2_4, and_3_4), axis=None)

        # Defuzzification using the center of area
        lam_numerator1 = 0
        lam_denominator1 = 0
        lam_numerator2 = 0
        lam_denominator2 = 0
        for and_rule, rule1, rule2 in zip(and_rules, rules_values1, rules_values2):
            output_value1 = defuzz_coa(and_rule, centers_out1, widths_out1, rule1)
            lam_numerator1 += output_value1[0]
            lam_denominator1 += output_value1[1]

            output_value2 = defuzz_coa(and_rule, centers_out2, widths_out2, rule2)
            lam_numerator2 += output_value2[0]
            lam_denominator2 += output_value2[1]

        # Check to make sure denominator is not 0
        if lam_denominator1 == 0 and lam_denominator2 == 0:
            lam1 = 0
            lam2 = 0
        elif lam_denominator1 == 0:
            lam1 = 0
            lam2 = lam_numerator2 / lam_denominator2
        elif lam_denominator2 == 0:
            lam1 = lam_numerator1 / lam_denominator1
            lam2 = 0
        else:
            lam1 = lam_numerator1 / lam_denominator1
            lam2 = lam_numerator2 / lam_denominator2

        # return the output of this fis
        return lam1, lam2
