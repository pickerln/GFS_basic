import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math
import numpy as np

from Fuzzy_Logic_Toolbox.Simple_FISs import split_vector_given


def get_plot_points(fuzzy_system):
    def to_x_y_vectors(centers, widths):
        x_values = []
        y_values = []
        for center, width in zip(centers, widths):
            x_values.extend([[center - width, center, center + width]])
            y_values.extend([[0, 1, 0]])
        return x_values, y_values

    ga_vector = fuzzy_system[-1]
    if fuzzy_system[0] == '2_1':
        split_2_1_vector = split_vector_given(fuzzy_system[3], fuzzy_system[4], 0, ga_vector, 3)
        centers_1, widths_1, centers_2, widths_2, centers_3, widths_3, output_centers, output_widths, rules = split_2_1_vector
    elif fuzzy_system[0] == '3_1':
        split_3_1_vector = split_vector_given(fuzzy_system[4], fuzzy_system[5], fuzzy_system[6], ga_vector, 3)
        centers_1, widths_1, centers_2, widths_2, centers_3, widths_3, output_centers, output_widths, rules = split_3_1_vector

    x_values_1, y_values_1 = to_x_y_vectors(centers_1, widths_1)
    x_values_2, y_values_2 = to_x_y_vectors(centers_2, widths_2)
    x_values_3, y_values_3 = to_x_y_vectors(centers_3, widths_3)
    x_values_out, y_values_out = to_x_y_vectors(output_centers, output_widths)

    return x_values_1, y_values_1, x_values_2, y_values_2, x_values_3, y_values_3, x_values_out, y_values_out, rules


def view_layer_mfs(fuzzy_systems_layer, layer_num):
    """ Populate a figure with all membership function graphs from that layer"""

    def populate_subplot(n_rows, n_cols, i1, i2, x_values, y_values, title, two_one=True):
        """ Add functions to single subplot"""

        def add_formatted_title(title):
            """ Move title to two lines if too long and replace '_' with ' ' """
            title = title.replace("_", " ")
            title = list(title)
            if len(title) > 20:
                title_first = title[:20]
                i = 0
                save_i_to_insert = 0
                for char in title_first[::-1]:
                    if char == ' ':
                        save_i_to_insert = i
                    i += 1
                title.insert(save_i_to_insert, '\n')
            return "".join(title)

        colors = ['g', 'c', 'b', 'm', 'k']
        the_subplot = plt.subplot2grid((n_rows, n_cols), (i1, i2))

        if two_one and i2 == 3:
            the_subplot = plt.subplot2grid((n_rows, n_cols), (i1, 2), colspan=2)
        for x_value, y_value, color in zip(x_values, y_values, colors):
            the_subplot.plot(x_value, y_value, color)
        the_subplot.set_title(add_formatted_title(title), fontsize=9.0)
        the_subplot.set_ylim([0, 1.1])

    n_row = len(fuzzy_systems_layer)
    n_col = 4
    fig = plt.figure(figsize=(n_col * 3, n_row * 2.5))
    fig.suptitle(('Layer ' + str(layer_num) + ' Membership Functions'))
    fig.subplots_adjust(left=.05, right=.95, top=.8, hspace=0.7)
    low_patch = mlines.Line2D([], [], color='g', markersize=15, label='low')
    med_patch = mlines.Line2D([], [], color='c', markersize=15, label='medium')
    hgh_patch = mlines.Line2D([], [], color='b', markersize=15, label='high')


    i = 0
    layer_rule_tables = []
    for fuzzy_system in fuzzy_systems_layer:
        x_values_1, y_values_1, x_values_2, y_values_2, x_values_3, y_values_3, x_values_out, y_values_out, rules = get_plot_points(
            fuzzy_system)

        if fuzzy_system[0] == '2_1':
            layer_rule_tables.append(display_rules_single_fis(rules, fuzzy_system))

        populate_subplot(n_row, n_col, i, 0, x_values_1, y_values_1, fuzzy_system[1])
        populate_subplot(n_row, n_col, i, 1, x_values_2, y_values_2, fuzzy_system[2])
        if x_values_3:
            populate_subplot(n_row, n_col, i, 2, x_values_3, y_values_3, fuzzy_system[3])
            two_one_fuzzy_system = False
        else:
            two_one_fuzzy_system = True
        populate_subplot(n_row, n_col, i, 3, x_values_out, y_values_out, 'Layer output', two_one=two_one_fuzzy_system)
        if i == 0:
            plt.legend(handles=[low_patch, med_patch, hgh_patch], bbox_to_anchor=(0., 1.02, 1., .102), loc='lower center',
                       ncol=3, borderaxespad=1.5)

            #plt.legend(handles=[low_patch, med_patch, hgh_patch], loc='upper left')
        i += 1


    return layer_rule_tables



# Now for the rules - still needs a good amount of work
def display_rules_single_fis(rules, fuzzy_system_descriptors):
    number_of_mfs_in1 = fuzzy_system_descriptors[3]
    number_of_mfs_in2 = fuzzy_system_descriptors[4]
    basic_descriptors = ['low', 'medium', 'high'] #{'3': , '5': ['very low', 'low', 'medium', 'high', 'very high']}

    rule_strings = []
    for rule in rules:
        try:
            rule = basic_descriptors[int(math.ceil(rule) - 1)]
        except IndexError:
            rule = 'high'
        rule_strings.append(rule)

    rule_table = [['mf2: low', 'mf2: medium', 'mf2: high']]
    loc_list = 0
    for i1 in np.arange(0, number_of_mfs_in1):
        rule_table.append(rule_strings[loc_list: loc_list+number_of_mfs_in2])
        loc_list += number_of_mfs_in2

    return rule_table

#
# number_mfs_inord = [['2_1', 'mobility_retail_and_recreation', 'mobility_grocery_and_pharmacy', 3, 3, chromosome[0: 27]],
#                     ['2_1', 'mobility_parks', 'mobility_residential', 3, 3, chromosome[27: 54]],
#                     ['2_1', 'mobility_transit_stations', 'mobility_workplaces', 3, 3, chromosome[54: 81]],
#                     ['3_1', 'lam 1', 'lam 2', 'lam 3', 3, 3, 3, chromosome[81: 132]],
#                     ['2_1', 'lam 4', 'new_confirmed cases', 3, 5, chromosome[132: 169]]]
#
# # Layer 1
# layer_1_rules = view_layer_mfs(number_mfs_inord[0: 3], 1)
# plt.show()
#
# # Layer 2
# view_layer_mfs(number_mfs_inord[3: 4], 2)
# plt.show()
#
# # Layer 3
# view_layer_mfs(number_mfs_inord[4: 5], 3)
# plt.show()

