#! /usr/bin/python3


import matplotlib_helper as helper
import json
import sys
import pprint
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter()

SAVE_PATH = "graphs/"

#    ([<data>], label),
def handle_result(item):
    _, axes = plt.subplots()

    helper.build_bar_graph(
        item["group_data"],
        item["x_labels"],
        item["y_label"],
        # item["title"],
        "",
        axes,
        show_legend=item["show_legend"]
    )

    plt.savefig(SAVE_PATH + item["filename"], dpi=300,bbox_inches='tight')

if __name__ == "__main__":
    results = None
    with open(sys.argv[1]) as f:
        results = json.load(f)
    
    pp.pprint(results)

    for result in results:
        handle_result(result)

    

