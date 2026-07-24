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
# QUESTION 1
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# QUESTION 2
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# QUESTION 3
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# QUESTION 4
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# QUESTION 5
# ----------------------------------------------------------------------



 


