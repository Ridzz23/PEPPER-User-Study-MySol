# to run: pyExt <file_name>

import csv
import json
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# Helper Functions (Provided)
# ----------------------------------------------------------------------

def cpu_load_score(cpu, memory):
    """
    Computes a weighted server load score.

    Inputs:
        cpu    - CPU utilization percentage
        memory - Memory utilization percentage

    Returns:
        Floating-point load score.
    """
    return cpu * 0.7 + memory * 0.3


def create_bar_chart(server_scores):
    """
    Creates a bar chart showing the load score for each server.

    Input:
        server_scores - list of dictionaries:
            {
                "server": "...",
                "score": ...
            }

    Saves:
        server_load.png
    """

    names = [s["server"] for s in server_scores]
    scores = [s["score"] for s in server_scores]

    plt.figure(figsize=(8,4))
    plt.bar(names, scores)
    plt.xlabel("Server")
    plt.ylabel("Load Score")
    plt.title("Server Load Summary")
    plt.tight_layout()
    plt.savefig("server_load.png")


# ----------------------------------------------------------------------
# Provided Data
# ----------------------------------------------------------------------

servers = [
    {
        "server": "web1",
        "cpu": 91,
        "memory": 72
    },
    {
        "server": "web2",
        "cpu": 24,
        "memory": 43
    },
    {
        "server": "db1",
        "cpu": 87,
        "memory": 81
    },
    {
        "server": "cache1",
        "cpu": 38,
        "memory": 31
    }
]

project_dir = "./server_snapshot"


# ======================================================================
#                     START CODING BELOW THIS LINE
# ======================================================================


# ----------------------------------------------------------------------
# TODO 1
#
# Harden the repository.
#
# Restore permissions:
#
#   *.sh      -> 755
#   *.yaml    -> 600
#   *.env     -> 600
#
# Leave all other files unchanged.
#
# (FS)
# ----------------------------------------------------------------------

sh_files = find "./server_snapshot" -type "f" -name "*.sh"
print(sh_files)
yaml_files = find "./server_snapshot" -type "f" -name "*.yaml"
env_files = find "./server_snapshot" -type "f" -name "*.env"

for sh in sh_files:
    chmod "755" sh

for yaml in yaml_files:
    chmod "600" yaml

for env in env_files:
    chmod "600" env



# ----------------------------------------------------------------------
# TODO 2
#
# The operations team only wants busy servers.
#
# use the "servers" list
#
# Keep only servers where:
#
#     cpu > 80
#
# Sort the server names alphabetically.
# 
# Store the result in:
#
#     busy_servers.txt
# 
# example output: 
# 
# db2
# web1
#
# (DATA)
# ----------------------------------------------------------------------

busy_servers = ""

for serv in servers:
    if serv["cpu"] > 80:
        busy_servers += serv["server"] + "\n"

busy_servers $| sort $> "busy_servers.txt"


# ----------------------------------------------------------------------
# TODO 3
#
# Read disk_usage.csv.
#
#
# For each row, compute
#
#     usage = used / total * 100
#
# Store
#
# disk_stats
#
# as
#
# [
#     {
#         "server": ...,
#          ...
#         "usage": ...
#     }
# ]
#
# (DATA)
# ----------------------------------------------------------------------

disk_stats = cat "disk_usage.csv"

for row in disk_stats:
    row['usage'] = int(row['used']) / int(row['total']) * 100


# ----------------------------------------------------------------------
# TODO 4
#
# Compute a load score for every server in the "servers" list using
#
#     cpu_load_score()
#
# Store the result back into the existing servers list.
#
# Generate:
#
#     server_load.png
#
# using:
#
#     create_bar_chart()
#
# Then create a backup copy of the visualization:
#
#     server_load_backup.png
#
# (DATA + FS)
# ----------------------------------------------------------------------

for serv in servers:
    serv["score"] = cpu_load_score(
        serv["cpu"],
        serv["memory"]
    )

create_bar_chart(servers)

cp "./server_load.png" "./server_load_backup.png"

# ----------------------------------------------------------------------
# TODO 5
#
# Create
#
#     audit_output/
#
# Move
#
#     server_load.png
#
# into the directory.
#
# Verify that no files still have permission 777.
#
# If any remain,
#
# write their paths to
#
#     audit_output/unsafe_files.txt
#
# Otherwise create
#
#     audit_output/success.txt
#
# containing
#
#     Repository successfully secured.
#
# (FS)
# ----------------------------------------------------------------------

mkdir "./audit_output"

mv "./server_load.png" "./audit_output"

unsafe_files = find "./server_snapshot" -type "f" -perm "777"

if unsafe_files:
    for file in unsafe_files:
        echo file $> "audit_output/unsafe_files.txt"

else:
    echo "Repository successfully secured." $> "audit_output/success.txt"






