#! /usr/bin/python3

from matplotlib_helper import build_bar_graph
import matplotlib.pyplot as plt
import json
import sys
import pprint
pp = pprint.PrettyPrinter()



# Where selected results is a list containing the elements for Regular, Wireguard, and OpenVPN
def gen_client_summary(selected_results):
    wireguard_tcp = None
    regular_tcp = None
    openvpn_tcp = None
    wireguard_udp = None
    regular_udp = None
    openvpn_udp = None
    for r in [s for s in selected_results if s["Protocol"] == "tcp"]:
        if "openvpn" in r["Test Name"]: openvpn_tcp = r
        if "wireguard" in r["Test Name"]: wireguard_tcp = r
        if "regular" in r["Test Name"]: regular_tcp = r

    for r in [s for s in selected_results if s["Protocol"] == "udp"]:
        if "openvpn" in r["Test Name"]: openvpn_udp = r
        if "wireguard" in r["Test Name"]: wireguard_udp = r
        if "regular" in r["Test Name"]: regular_udp = r

    # Error check
    (wireguard_tcp,regular_tcp,openvpn_tcp,wireguard_udp,regular_udp,openvpn_udp,)
    if None in (wireguard_tcp,regular_tcp,openvpn_tcp,wireguard_udp,regular_udp,openvpn_udp,):
        print("One of the cases was not found in the selected results! Giving up")
        pp.pprint(selected_results)
        sys.exit(1)

    # So we can make use of list comprehensions
    sorted_results_tcp = (regular_tcp, wireguard_tcp, openvpn_tcp)
    sorted_results_udp = (regular_udp, wireguard_udp, openvpn_udp)
    
    labels = ("Regular", "Wireguard", "OpenVPN")

    fig, axes = plt.subplots(2,2)

    # throughput_graph
    groups = [
        ([s["Avg MB Sent/sec (Effective)"] for s in sorted_results_tcp], "tcp"),
        # ([s["Avg MB Sent/sec (Effective)"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "MB/sec", "Throughput", axes[0][0])

    # rtt_graph
    # send_overhead_graph
    # cpu_usage_graph
    


    fig.tight_layout()
    plt.show()




client_results = None
with open("client_results.json", "r") as f:
    client_results = json.load(f)

##################
# Long Distance
##################
longhaul_results = [e for e in client_results if "long" in e["Test Name"]]
gen_client_summary(longhaul_results)




    




# fig, axes = plt.subplots(2,2)
# ax = axes[0][0]

# labels = ['Regular', 'Wireguard', 'OpenVPN']
# groups = [
#     ([20, 34, 30], "tcp"),
#     # ([25, 32, 1000], "udp"),
# ]

# build_bar_graph(groups, labels, "MB/sec", "Throughput", ax)

# fig.tight_layout()

# plt.show()