#! /usr/bin/python3

from matplotlib_helper import build_bar_graph
import matplotlib.pyplot as plt
import json
import sys
import pprint
pp = pprint.PrettyPrinter()

# Returns ((regular_tcp, wireguard_tcp, openvpn_tcp), (regular_udp, wireguard_udp, openvpn_udp))
# Since this is actually common to both client and server, break it out here for reuse
def parse_out_sorted_results(selected_results):
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

    return ((regular_tcp, wireguard_tcp, openvpn_tcp) , (regular_udp, wireguard_udp, openvpn_udp))
    

# Where selected results is a list containing the elements for Regular, Wireguard, and OpenVPN
def gen_client_summary(selected_results, title_preamble):
    # So we can make use of list comprehensions
    sorted_results_tcp, sorted_results_udp = parse_out_sorted_results(selected_results)
    
    labels = ("Regular", "Wireguard", "OpenVPN")

    

    # throughput_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg MB Sent/sec (Effective)"] for s in sorted_results_tcp], "tcp"),
        ([s["Avg MB Sent/sec (Effective)"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "MB/sec", title_preamble+" Client Throughput", axes)
    plt.savefig(title_preamble+'_client_throughput.png', dpi=300)

    # rtt_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg RTT milliseconds"] for s in sorted_results_tcp], "tcp"),
        # ([s["Avg RTT milliseconds"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "ms", title_preamble + " Client RTT", axes, show_legend=False)
    plt.savefig(title_preamble+'_client_rtt.png', dpi=300)

    # cpu_usage_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg CPU usage"] for s in sorted_results_tcp], "tcp"),
        ([s["Avg CPU usage"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "Percent", title_preamble + " Client CPU Usage", axes)
    plt.savefig(title_preamble+'_client_cpu.png', dpi=300)


# Where selected results is a list containing the elements for Regular, Wireguard, and OpenVPN
def gen_server_summary(selected_results, title_preamble):
    # So we can make use of list comprehensions
    sorted_results_tcp, sorted_results_udp = parse_out_sorted_results(selected_results)
    
    labels = ("Regular", "Wireguard", "OpenVPN")

    # throughput_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg MB Received/sec (Effective)"] for s in sorted_results_tcp], "tcp"),
        ([s["Avg MB Received/sec (Effective)"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "MB/sec", title_preamble + " Server Throughput", axes)
    plt.savefig(title_preamble+'_server_throughput.png', dpi=300)

    # rtt_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg RTT milliseconds"] for s in sorted_results_tcp], "tcp"),
        # ([s["Avg RTT milliseconds"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "ms", title_preamble + " Server RTT", axes, show_legend=False)
    plt.savefig(title_preamble+'_server_rtt.png', dpi=300)

    # cpu_usage_graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg CPU usage"] for s in sorted_results_tcp], "tcp"),
        ([s["Avg CPU usage"] for s in sorted_results_udp], "udp"),
    ]
    build_bar_graph(groups, labels, "Percent", title_preamble + " Server CPU Usage", axes)
    plt.savefig(title_preamble+'_server_cpu.png', dpi=300)

# Where selected results is a list containing the elements for Regular, Wireguard, and OpenVPN
# We only use the TCP results though
def gen_context_metrics(selected_results, title_preamble):
    sorted_results_tcp, sorted_results_udp = parse_out_sorted_results(selected_results)

    labels = ("Regular", "Wireguard", "OpenVPN")

    # Context switch bar graph
    _, axes = plt.subplots()
    groups = [
        ([s["Avg context switches/second"] for s in sorted_results_tcp], "tcp"),
    ]
    build_bar_graph(groups, labels, "Ctx switches/sec", title_preamble + " Server Throughput", axes, show_legend=False)
    plt.savefig(title_preamble+'_context_switches_bar.png', dpi=300)





client_results = None
server_results = None



with open("client_results.json", "r") as f:
    client_results = json.load(f)

with open("server_results.json", "r") as f:
    server_results = json.load(f)

# What a fucking pain. Need to copy the RTT results from the client to server
server_dict = {}
for s in server_results:
    server_dict[s["Test Name"]] = s

for c in client_results:
    server_test_name = c["Test Name"][:-6] + "server"
    server_dict[server_test_name]["Avg RTT milliseconds"] = c["Avg RTT milliseconds"]

pp.pprint(server_results)



##################
# Long Distance
##################

# # Client
# longhaul_results = [e for e in client_results if "long" in e["Test Name"]]
# gen_client_summary(longhaul_results, "Longhaul")

# # Server
# longhaul_results = [e for e in server_results if "long" in e["Test Name"]]
# gen_server_summary(longhaul_results, "Longhaul")

# ###################
# # Short Distance
# # Only need server for this one, since client results are doodoo
# ###################

# # Server
# shorthaul_resuls = [e for e in server_results if "short" in e["Test Name"]]
# gen_server_summary(shorthaul_resuls, "Shorthaul")

##########################
# Local VM - One Core
##########################
# Server
local_vm_one_core = [e for e in server_results if "one_core" in e["Test Name"]]
gen_server_summary(local_vm_one_core, "Local VM - One Core")
gen_context_metrics(local_vm_one_core, "Local VM - One Core")

