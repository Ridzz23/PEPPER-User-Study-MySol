# Server Incident Analyzer - subprocess version

import json
import math
import subprocess
from datetime import datetime
import gzip


# ---------------- Python Functions ----------------

def severity_score(error_count, response_time):
    return (
        error_count * 2
        + math.log(response_time + 1)
    )


def classify(score):
    if score > 50:
        return "CRITICAL"
    elif score > 20:
        return "WARNING"
    else:
        return "NORMAL"


def enrich_incident(incident):

    incident["severity"] = severity_score(
        incident["errors"],
        incident["response_time"]
    )

    incident["category"] = classify(
        incident["severity"]
    )

    return incident



def format_report(incidents):

    output = ""

    for i in incidents:
        output += (
            f"{i['server']} "
            f"{i['category']} "
            f"{i['severity']:.2f}\n"
        )

    return output



# ---------------- Shell Stage 1 ----------------
# find logs/*.log

find_process = subprocess.Popen(
    [
        "find",
        "logs",
        "-name",
        "*.log"
    ],
    stdout=subprocess.PIPE,
    text=True
)


# ---------------- Shell Stage 2 ----------------
# grep ERROR from files

grep_process = subprocess.Popen(
    [
        "xargs",
        "grep",
        "ERROR"
    ],
    stdin=find_process.stdout,
    stdout=subprocess.PIPE,
    text=True
)


find_process.stdout.close()


error_output, _ = grep_process.communicate()



# ---------------- Python Stage 1 ----------------
# Parse logs and calculate severity


incidents = []


for line in error_output.splitlines():

    # Example:
    #
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
# Sort output

report_lines = format_report(
    incidents
)


sort_process = subprocess.Popen(
    [
        "sort"
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)


sorted_report, _ = sort_process.communicate(
    input=report_lines
)



# ---------------- Python Stage 2 ----------------
# Convert sorted output into JSON


final_report = []


for line in sorted_report.splitlines():

    server, category, score = line.split()

    final_report.append(
        {
            "server": server,
            "category": category,
            "score": float(score)
        }
    )



# ---------------- Shell Stage 4 ----------------
# Count categories with awk + sort + uniq


summary_input = format_report(
    final_report
)


awk_process = subprocess.Popen(
    [
        "awk",
        "{print $2}"
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)


sort_process = subprocess.Popen(
    [
        "sort"
    ],
    stdin=awk_process.stdout,
    stdout=subprocess.PIPE,
    text=True
)


awk_output, _ = awk_process.communicate(
    input=summary_input
)


uniq_process = subprocess.Popen(
    [
        "uniq",
        "-c"
    ],
    stdin=sort_process.stdout,
    stdout=subprocess.PIPE,
    text=True
)


sort_process.stdout.close()


summary, _ = uniq_process.communicate()



# ---------------- Python Stage 3 ----------------
# Create dashboard


dashboard = {

    "generated":
        str(datetime.now()),

    "total_incidents":
        len(final_report),

    "summary":
        summary.splitlines(),

    "incidents":
        final_report
}



json_output = json.dumps(
    dashboard,
    indent=4
)



# ---------------- Shell Stage 5 ----------------
# Write + compress output


with open(
    "daily_report.json",
    "w"
) as f:
    f.write(json_output)



gzip_process = subprocess.Popen(
    [
        "gzip",
        "daily_report.json"
    ]
)


gzip_process.wait()