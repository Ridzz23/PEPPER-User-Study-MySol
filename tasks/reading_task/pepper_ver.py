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
def severity_score(error_count, response_time):
    return (
        error_count * 2
        + math.log(response_time + 1)
    )


"""
Converts a numeric severity score into a category.

Rules:
- score > 50  -> CRITICAL incident
- score > 20  -> WARNING incident
- otherwise   -> NORMAL incident

Returns:
- a string representing the incident category
"""
def classify(score):
    if score > 50:
        return "CRITICAL"
    elif score > 20:
        return "WARNING"
    else:
        return "NORMAL"



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
def enrich_incident(incident):

    incident["severity"] = severity_score(
        incident["errors"],
        incident["response_time"]
    )

    incident["category"] = classify(
        incident["severity"]
    )

    return incident



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
def create_report(incidents):

    output = ""

    for incident in incidents:

        output += (
            f"{incident['server']} "
            f"{incident['category']} "
            f"{incident['severity']:.2f}\n"
        )

    return output



# ---------------- Shell Stage 1 ----------------
# Find all log files


log_files = find "./logs" -name "*.log"


# ---------------- Shell Stage 2 ----------------
# Extract ERROR messages


error_logs = log_files $| xargs grep "ERROR"


# ---------------- Python Stage 1 ----------------
# Parse shell output


incidents = []


for line in error_logs.splitlines():

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


    incident = {

        "server": server,

        "errors": 1,

        "response_time": latency

    }


    incidents.append(
        enrich_incident(incident)
    )



# ---------------- Shell Stage 3 ----------------
# Sort generated report


report = create_report(
    incidents
)


sorted_report = report $| sort



# ---------------- Python Stage 2 ----------------
# Convert sorted text back into structured data


final_incidents = []


for line in sorted_report.splitlines():

    server, category, score = line.split()


    final_incidents.append({

        "server": server,

        "category": category,

        "score": float(score)

    })



# ---------------- Shell Stage 4 ----------------
# Generate category summary


summary = sorted_report $| awk "{print $2}" $| sort $| uniq -c



# ---------------- Python Stage 3 ----------------
# Create dashboard


dashboard = {

    "generated":
        str(datetime.now()),


    "total_incidents":
        len(final_incidents),


    "summary":
        summary.splitlines(),


    "incidents":
        final_incidents

}



json_output = json.dumps(
    dashboard,
    indent=4
)



# ---------------- Shell Stage 5 ----------------
# Save and compress report


echo json_output $> "daily_report.json"



"daily_report.json" $| gzip $> "daily_report.json.gz"