# Server Incident Analyzer
#
# Goal:
# Analyze server logs and generate incident reports.
#
# PEPPER work here:
# - find log files
# - filter error events
# - transform shell output into Python data
# - sort and aggregate results
# - write final JSON report


import json
import math
from datetime import datetime


# ---------------- Python Functions ----------------


def severity_score(error_count, response_time):
    """
    Calculates how severe an incident is.

    Inputs:
    - error_count: number of errors detected for a server
    - response_time: server response latency in milliseconds

    The formula gives higher severity to:
    - servers with more errors
    - servers with slower response times

    Returns:
    - a numeric severity score
    """

    return (
        error_count * 2
        + math.log(response_time + 1)
    )


def classify(score):
    """
    Converts a numeric severity score into a category.

    Rules:
    - score > 50  -> CRITICAL incident
    - score > 20  -> WARNING incident
    - otherwise   -> NORMAL incident

    Returns:
    - a string representing the incident category
    """

    if score > 50:
        return "CRITICAL"
    elif score > 20:
        return "WARNING"
    else:
        return "NORMAL"



def enrich_incident(incident):
    """
    Adds additional information to an incident.

    Takes a basic incident dictionary containing:
    - server name
    - number of errors
    - response time

    Adds:
    - severity score calculated using severity_score()
    - category calculated using classify()

    Returns:
    - the updated incident dictionary
    """

    incident["severity"] = severity_score(
        incident["errors"],
        incident["response_time"]
    )

    incident["category"] = classify(
        incident["severity"]
    )

    return incident


def create_report(incidents):
    """
    Converts a list of incident dictionaries into
    a formatted text report.

    Example output:

    db1 WARNING 24.52
    api1 CRITICAL 73.12

    Each line contains:
    - server name
    - incident category
    - severity score

    Returns:
    - a string containing the full report
    """

    output = ""

    for incident in incidents:

        output += (
            f"{incident['server']} "
            f"{incident['category']} "
            f"{incident['severity']:.2f}\n"
        )

    return output


def get_category(report):
    """
    Extract the incident category (second column)
    from each report line.

    Input:
        api1 NORMAL 10.41
        db1 WARNING 25.50

    Output:
        NORMAL
        WARNING
    """

    categories = []

    for line in report:
        if line.strip() == "":
            continue

        parts = line.split()

        categories.append(parts[1])

    return "\n".join(categories)


# ---------------- Shell Stage 1 ----------------
# Find all log files


log_files = find "./logs" -name "*.log" 

logs_as_args = " ".join(log_files)

print("log files:\n", log_files)

# ---------------- Shell Stage 2 ----------------
# Extract ERROR messages

error_logs = grep "ERROR" logs_as_args

print("error logs:\n", error_logs)

# ---------------- Python Stage 1 ----------------
# Parse shell output


incidents = []
server_stats = {}


for line in error_logs:

    if line == "":
        continue

    # Example:
    # ERROR server=db1 latency=2500

    parts = line.split()


    server = (
        parts[1]
        .split("=")[1]
    )


    latency = int(
        parts[2]
        .split("=")[1]
    )

    if server not in server_stats:
        server_stats[server] = {
            "errors": 1,
            "response_time": latency
        }


for server, stats in server_stats.items():

    incident = {

        "server": server,

        "errors": stats["errors"],

        "response_time": stats["response_time"]

    }


    incidents.append(
        enrich_incident(incident)
    )

print("Incidents:\n", incidents)
# ---------------- Shell Stage 3 ----------------
# Sort generated report


report = create_report(
    incidents
)


sorted_report = report $| sort


# ---------------- Python Stage 2 ----------------
# Convert sorted text back into structured data


final_incidents = []


for line in sorted_report:

    server, category, score = line.split()


    final_incidents.append({

        "server": server,

        "category": category,

        "score": float(score)

    })

# ---------------- Shell Stage 4 ----------------
# Generate category summary

summary = get_category(sorted_report) $| sort $| uniq -c

# ---------------- Python Stage 3 ----------------
# Create dashboard


dashboard = {

    "generated":
        str(datetime.now()),


    "total_incidents":
        len(final_incidents),


    "summary":
        summary,


    "incidents":
        final_incidents

}



json_output = "'" + json.dumps(
    dashboard,
    indent=4
) + "'"

# ---------------- Shell Stage 5 ----------------
# Save and compress report


echo json_output $> "daily_report.json"

cat "daily_report.json" $| gzip $> "daily_report.json.gz"




