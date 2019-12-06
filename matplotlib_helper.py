#! /usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import matplotlib




# group_data is a list in the form of:
# [
#    ([<data>], label),
# ]
#    where each <data> list has the same number of elements
def build_bar_graph(
    group_data,
    x_labels,
    y_label,
    title,
    ax,
    bar_width=0.35,
):
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    # First we validate that the data all has the same length
    asserted_length = len(group_data[0][0])
    for d in group_data: 
        if len(d[0]) != asserted_length: 
            print("Data is malformed, need same num data elements across all groups")
            print(d)
            return
    # OK, we're validated
    
    num_groups = len(group_data)
    x = np.arange(len(x_labels))  # the label locations
    total_width = 0.35  # the width of all the bars in a group

    rects = []
    for index, group in enumerate(group_data):
        x_positions = (x + (total_width/num_groups) * index) - total_width/2
        y_positions = group[0]
        new_bar = ax.bar(x_positions, y_positions, total_width/num_groups, label=group[1], align='edge')
        rects.append(new_bar)

    # rects1 = ax.bar(x - width/num_elements_per_group, men_means, width, label='Men')
    # rects2 = ax.bar(x + width/num_elements_per_group, women_means, width, label='Women')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for r in rects: autolabel(r)
    # autolabel(rects1)
    # autolabel(rects2)


if __name__ == "__main__":
    g_plot_nrows = 2
    g_plot_ncols = 2
    g_plot_index = 1

    fig, axes = plt.subplots(2,2)
    ax = axes[0][0]

    labels = ['Regular', 'Wireguard', 'OpenVPN']
    groups = [
        ([20, 34, 30], "tcp"),
        ([25, 32, 1000], "udp"),
    ]
    build_bar_graph(groups, labels, "MB/sec", "Throughput", ax)

    fig.tight_layout()

    plt.show()